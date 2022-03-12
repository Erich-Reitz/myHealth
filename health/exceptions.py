class HealthError(Exception):
    """Base Class for Health tool exceptions"""

    pass


class UnknownBehavior(HealthError):
    """Raise exception when requesting something unknown"""

    pass
