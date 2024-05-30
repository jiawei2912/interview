class VerifiedEmail(models.Model, metaclass=LazyBackgroundTasks):
    email = models.EmailField(primary_key=True)
    expiry_date = models.DateTimeField(default=timezone.now)
    OTP = models.CharField(max_length=6)

    @LazyBackgroundTasks.trigger
    def isVerifiedEmail(email: str) -> bool:
        try:
            verifiedEmail = VerifiedEmail.objects.get(email=email)
            if verifiedEmail.expiry_date >= timezone.now():
                return True
        except ObjectDoesNotExist:
            pass
        return False

    @LazyBackgroundTasks.trigger
    def refreshVerifiedEmail(email: str) -> None:
        verifiedEmail = VerifiedEmail.objects.get(email=email)
        verifiedEmail.expiry_date = timezone.now() + timezone.timedelta(days=30)
        verifiedEmail.save()

    @LazyBackgroundTasks.trigger
    def createEmailOTP(email: str) -> str:
        verifiedEmail = None
        try:
            verifiedEmail = VerifiedEmail.objects.get(email=email)
        except ObjectDoesNotExist:
            verifiedEmail = VerifiedEmail(
                email=email, expiry_date=timezone.now() - timezone.timedelta(days=5)
            )
        OTP = []
        for _ in range(6):
            OTP.append(str(random.randint(0, 9)))
        OTP: str = "".join(OTP)
        verifiedEmail.OTP = OTP
        verifiedEmail.save()
        return OTP

    @LazyBackgroundTasks.trigger
    def verifyOTP(email: str, otp: str) -> bool:
        if otp is None or email is None:
            return False
        if type(otp) != type(""):
            return False
        if len(otp) != 6:
            return False
        verifiedEmail = None
        try:
            verifiedEmail = VerifiedEmail.objects.get(email=email)
        except ObjectDoesNotExist:
            return False
        if otp != verifiedEmail.OTP:
            return False
        verifiedEmail.OTP == ""
        verifiedEmail.save()
        VerifiedEmail.refreshVerifiedEmail(email)
        return True

    @LazyBackgroundTasks.background_task(
        max_frequency=timezone.timedelta(
            minutes=settings.USER_EXPIRED_VERIFIED_EMAILS_CHECK_PERIOD
        )
    )
    def pruneExpiredEmails():
        cutoffDate = timezone.now() - timezone.timedelta(
            minutes=settings.VERIFIED_EMAIL_CACHE_DURATION
        )
        VerifiedEmail.objects.filter(expiry_date__lte=cutoffDate).delete()