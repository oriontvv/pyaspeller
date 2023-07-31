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


class EncodingError(BaseSpellerError):
    """
    Encoding of the source file differs from the one was set
    """
