import inspect
from asyncio import gather
from functools import wraps
from typing import TypeVar, Callable, Any

from injectable.autowiring.autowired_type import _Autowired
from injectable.autowiring.autowiring_utils import coroutine_wrapper
from injectable.errors import AutowiringError

T = TypeVar("T", bound=Callable[..., Any])


def autowired(func: T) -> T:
    """
    Function decorator to setup dependency injection autowiring.

    Only parameters annotated with :class:`Autowired <injectable.Autowired>` will be
    autowired for injection.

    If no parameter is annotated with :class:`Autowired <injectable.Autowired>` an
    :class:`AutowiringError <injectable.errors.AutowiringError>` will be raised.

    An :class:`AutowiringError <injectable.errors.AutowiringError>` will also be raised
    if a parameter annotated with :class:`Autowired <injectable.Autowired>` is given a
    default value or if a non Autowired-annotated positional parameter is placed after
    an Autowired-annotated positional parameter.

    When used in an async function it will automatically asynchronously wait for all
    injectables that happen to be coroutines.

    Before attempting to call an autowired function make sure
    :meth:`load_injection_container <injectable.load_injection_container>` was invoked.

    .. note::
      This decorator can be applied to any function, not only an `__init__` method.

    .. note::
      This decorator accepts no arguments and must be used without trailing parenthesis.

    Usage::

      >>> from injectable import Autowired, autowired
      >>>
      >>> @autowired
      ... def foo(dep: Autowired(...)):
      ...     ...
    """
    signature = inspect.signature(func)
    autowired_parameters = []
    for index, parameter in enumerate(signature.parameters.values()):
        if not isinstance(parameter.annotation, _Autowired):
            if len(autowired_parameters) == 0 or parameter.kind in [
                parameter.KEYWORD_ONLY,
                parameter.VAR_KEYWORD,
            ]:
                continue
            raise AutowiringError(
                "Non-Autowired positional parameter follows Autowired parameter"
            )
        if parameter.default is not parameter.empty:
            raise AutowiringError("Default value assigned to Autowired parameter")
        if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            raise AutowiringError(f"Autowired parameter is of kind {parameter.kind}")
        autowired_parameters.append(parameter)

    if len(autowired_parameters) == 0:
        raise AutowiringError("No parameter is typed with 'Autowired'")

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        bound_arguments = signature.bind_partial(*args, **kwargs).arguments
        args = list(args)
        for parameter in autowired_parameters:
            if parameter.name in bound_arguments:
                continue
            dependency = parameter.annotation.inject()
            if parameter.kind is parameter.POSITIONAL_ONLY:
                args.append(dependency)
            else:
                kwargs[parameter.name] = dependency

        return func(*args, **kwargs)

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        bound_arguments = signature.bind_partial(*args, **kwargs).arguments
        args = list(args)
        args_tasks = []
        kwargs_tasks = []
        kwargs_names = []
        for parameter in autowired_parameters:
            if parameter.name in bound_arguments:
                continue
            dependency = parameter.annotation.inject()
            if parameter.annotation.multiple:
                task = gather(*[coroutine_wrapper(o) for o in dependency])
            else:
                task = coroutine_wrapper(dependency)
            if parameter.kind is parameter.POSITIONAL_ONLY:
                args_tasks.append(task)
            else:
                kwargs_tasks.append(task)
                kwargs_names.append(parameter.name)

        awaited_args, awaited_kwargs = await gather(
            gather(*args_tasks), gather(*kwargs_tasks)
        )
        args.extend(awaited_args)
        for k, v in zip(kwargs_names, awaited_kwargs):
            kwargs[k] = v

        return await func(*args, **kwargs)

    return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
