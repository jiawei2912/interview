def binary_search(key, keys):
    lo, hi = 0, len(keys)
    while lo < hi:
        mid = (lo + hi) // 2
        if keys[mid] < key: 
            lo = mid + 1
        elif keys[mid] > key: 
            hi = mid
        else:
            return mid
    return lo


def sorted_list_manager():
    keys = []
    values = []
    def set_var(key, value):
        index = binary_search(key, keys)
        if index != len(keys) and keys[index] == key:
            values[index] = value
        else:
            keys.insert(index, key)
            values.insert(index, value)
    def get_var(key, default=None):
        index = binary_search(key, keys)
        if index != len(keys) and keys[index] == key:
            return values[index]
        return default
    def get_keys():
        return keys
    return set_var, get_var, get_keys
        
