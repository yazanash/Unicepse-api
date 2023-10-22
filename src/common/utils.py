import pyotp
from uuid import uuid4
from threading import Lock


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class OtpHelper(metaclass=SingletonMeta):
    """Helper class to Handle OTP creation and validation"""

    totp = pyotp.TOTP('base32secret3232', interval=60)

    def generate_otp(self):
        """This method generates otp on demand"""
        return self.totp.now()

    def validate_otp(self, otp):
        return self.totp.verify(otp)


class TokenGenerator(metaclass=SingletonMeta):
    """Token generator Based on uuid4 Algorithm"""

    @classmethod
    def generate_token(cls):
        """Generates Unique 32-hex-string UUID (Token)"""
        return str(uuid4())
