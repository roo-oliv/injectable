import collections
import inspect

from typing import Union, List, Tuple, Sequence, Iterable, Awaitable, Coroutine, \
    AsyncIterable, AsyncIterator

from typing_inspect import is_forward_ref, get_forward_arg


def sanitize_if_forward_ref(subscripted_type: type) -> Union[type, str]:
    if is_forward_ref(subscripted_type):
        return get_forward_arg(subscripted_type)
    return subscripted_type


def is_sequence(tp):
    return tp in [
        list,
        tuple,
        collections.Sequence,
        collections.Iterable,
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


def is_awaitable(tp):
    return tp in [
        Awaitable,
        Coroutine,
        AsyncIterable,
        AsyncIterator,
    ]


async def coroutine_wrapper(obj):
    return await obj if inspect.iscoroutine(obj) else obj
