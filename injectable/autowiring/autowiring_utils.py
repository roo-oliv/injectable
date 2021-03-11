import collections.abc

from typing import Union, List, Tuple, Sequence, Iterable

from typing_inspect import is_forward_ref, get_forward_arg


def sanitize_if_forward_ref(subscripted_type: type) -> Union[type, str]:
    if is_forward_ref(subscripted_type):
        return get_forward_arg(subscripted_type)
    return subscripted_type


def is_sequence(tp):
    return tp in [
        list,
        tuple,
        collections.abc.Sequence,
        collections.abc.Iterable,
        List,
        Tuple,
        Sequence,
        Iterable,
    ]


def is_raw_sequence(dependency):
    return type(dependency) in [
        list,
        tuple,
    ]
