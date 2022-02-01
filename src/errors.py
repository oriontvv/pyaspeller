"""
Contains all custom Exceptions
"""


class BaseSpellerError(Exception):
    """
        Basic error wrapper
    """


class BadArgumentError(BaseSpellerError):
    """
        Invalid argument was given
    """
