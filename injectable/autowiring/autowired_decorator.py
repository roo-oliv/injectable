import inspect
from functools import wraps
from typing import TypeVar, Callable, Any

from injectable.autowiring.autowired_type import _Autowired
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

    Before attempting to call an autowired function make sure
    :meth:`InjectionContainer::load <injectable.InjectionContainer.load>` was invoked.

    .. note::
      This decorator can be applied to any function, not only an `__init__` method.

    .. note::
      This decorator accepts no arguments and must be used without trailing parenthesis.

    Usage::

      >>> from injectable import Autowired, autowired
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
        if parameter.kind is parameter.VAR_POSITIONAL:
            raise AutowiringError(f"Autowired parameter is of kind {parameter.kind}")
        autowired_parameters.append(parameter)

    if len(autowired_parameters) == 0:
        raise AutowiringError(f"No parameter is typed with 'Autowired'")

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_arguments = signature.bind_partial(*args, **kwargs).arguments
        args = list(args)
        for parameter in autowired_parameters:
            if parameter.name in bound_arguments:
                continue
            dependency = parameter.annotation.inject()
            if parameter.kind is parameter.KEYWORD_ONLY:
                kwargs[parameter.name] = dependency
            else:
                args.append(dependency)

        return func(*args, **kwargs)

    return wrapper
