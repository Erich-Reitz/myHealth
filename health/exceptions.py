class HealthError(Exception):
    """Base Class for Health tool exceptions"""


class UnknownBehavior(HealthError):
    """Raise exception when requesting something unknown"""


class GarminConnectConnectionError(HealthError):
    """Raised when communication ended in error."""


class GarminConnectTooManyRequestsError(HealthError):
    """Raised when rate limit is exceeded."""


class GarminConnectAuthenticationError(HealthError):
    """Raised when authentication is failed."""
