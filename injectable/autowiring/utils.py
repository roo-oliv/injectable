import sys

if sys.version_info[:3] >= (3, 7, 0):  # PEP 560
    from typing import Union, ForwardRef
else:
    from typing import Union, _ForwardRef as ForwardRef


def sanitize_if_forward_ref(subscripted_type: type) -> Union[type, str]:
    # TODO: Use typing_inspect.is_forward_ref and typing_inspect.get_forward_arg
    #   once they are released.
    #   https://github.com/ilevkivskyi/typing_inspect/pull/57
    if isinstance(subscripted_type, ForwardRef):
        return subscripted_type.__forward_arg__
    return subscripted_type
