from types import FunctionType
from functools import wraps
from typing import Dict, List

from django.utils import timezone
from django.db.models.base import ModelBase

class LazyBackgroundTasks(ModelBase):
    """
    A metaclass that allows for the scheduling and lazy execution of class methods as background tasks.
    Lazy execution means that the background tasks are executed only when triggered.

    Attributes:
        last_update_datetime (datetime): The last time the background tasks were executed.
        background_functions (dict): A dictionary mapping time intervals to lists of functions. Each function is executed
            if the specified time interval has passed since the last execution.

    Methods:
        manually_trigger_background_functions(): Manually triggers the execution of all background tasks.
        background_task(*args, **kwargs): A decorator that marks a function as a background task.
        trigger(func): A decorator that marks a function as a trigger for background tasks.
    """

    last_update_datetime: timezone.datetime = None
    background_functions: Dict[str, List[callable]] = {}

    def __init__(cls, name, bases, attrs):
        """
        Initializes the metaclass. Iterates over the attributes of the class being created, and if any of them are
        functions marked as background tasks or triggers, adds them to the appropriate data structures.
        """
        super().__init__(name, bases, attrs)
        for attr_name, attr_value in attrs.items():
            # if attribute is a function (not method, as this would include classes)
            if callable(attr_value) and isinstance(attr_value, FunctionType):
                if getattr(attr_value, "is_background_task", False):
                    max_frequency = getattr(
                        attr_value.marked_kwargs,
                        "max_frequency",
                        timezone.timedelta(hours=1),
                    )
                    if max_frequency in cls.background_functions:
                        cls.background_functions[max_frequency] += [attr_value]
                    else:
                        cls.background_functions[max_frequency] = [attr_value]
                elif getattr(attr_value, "is_trigger", False):
                    setattr(cls, attr_name, cls.decorator(attr_value))

    @classmethod
    def decorator(cls, func):
        """
        A decorator that triggers the execution of background tasks before calling the decorated function.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            cls.call_background_functions()
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def call_background_functions(cls):
        """
        Executes all background tasks whose time interval has passed since the last execution.
        """
        if cls.last_update_datetime is None:
            for timedelta_key, funcs in cls.background_functions.items():
                for func in funcs:
                    func()
        else:
            timedelta = timezone.now() - cls.last_update_datetime
            for timedelta_key, funcs in cls.background_functions.items():
                if timedelta >= timedelta_key:
                    for func in funcs:
                        func()
        cls.last_update_datetime = timezone.now()

    def manually_trigger_background_functions(cls):
        """
        Manually triggers the execution of all background tasks whose time interval has passed since the last execution.
        """
        cls.call_background_functions()

    # Marks a function as a background task
    # Accepts 'max_frequency' as a kwarg (defaults to 1 hour)
    @staticmethod
    def background_task(*args, **kwargs):
        """
        A decorator that marks a function as a background task.
        Accepts 'max_frequency' as a kwarg (defaults to 1 hour).
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*f_args, **f_kwargs):
                func.is_background_task = True
                func.marked_args = args
                func.marked_kwargs = kwargs
                return func(*f_args, **f_kwargs)

            return wrapper

        return decorator

    # Marks a function as a trigger for background tasks
    @staticmethod
    def trigger(func):
        """
        A decorator that marks a function as a trigger for background tasks.
        """
        func.is_trigger = True
        return func
