import inspect
import os
from typing import AnyStr


def get_caller_filepath(steps_back: int = 2) -> AnyStr:
    """
    Utility function to get the caller's filepath using inspection.

    :param steps_back: (optional) 1 step back in the call stack would return the file of
        the caller of this function. Defaults to 2, i.e. the path of the file of the
        caller of this function's caller.
    """
    frame_info = inspect.stack()[steps_back]
    filepath = frame_info.filename
    del frame_info
    return os.path.abspath(filepath)
