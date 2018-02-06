import inspect
from functools import wraps
from typing import Iterable

import logging

from injectable.lazy import Lazy
from injectable.util import get_class


def injectable(injectable_kwargs: Iterable[str] = None):
    """
    Returns a functions decorated for injection. The caller can
    explicitly pass into the function wanted dependencies. Any
    dependency not injected by the caller will be automatically
    injected.
    
    >>> class Dependency:
    ...     def __init__(self):
    ...         self.msg = "dependency initialized"
    ...
    >>> def foo(*, dep: Dependency):
    ...     return dep.msg
    ...
    >>> injectable()(foo)()
    'dependency initialized'
    
    :param injectable_kwargs: explicit list of which arguments to inject 
    :return: the function with all injectable arguments initialized
    """
    def decorator(func: callable):
        func_module = inspect.getmodule(func).__dict__
        specs = inspect.getfullargspec(func)

        if injectable_kwargs is None:
            injectables = {
                kwarg: specs.annotations.get(kwarg)
                for kwarg in specs.kwonlyargs
                if (kwarg not in (specs.kwonlydefaults or [])
                    and (inspect.isclass(specs.annotations.get(kwarg))
                         or isinstance(specs.annotations.get(kwarg), str)))
            }
            if len(injectables) is 0:
                logging.warning("Function '{function}' is annotated with"
                                " '@injectable' but no arguments that"
                                " qualify as injectable were found"
                                .format(function=func.__name__))
        else:
            injectables = {
                kwarg: specs.annotations.get(kwarg)
                for kwarg in injectable_kwargs
            }

        for kwarg, ref in injectables.items():
            if not isinstance(ref, str):
                continue

            cls = get_class(ref, func_module)
            if cls is None:
                continue

            injectables[kwarg] = cls

        for kwarg, cls in injectables.items():
            if isinstance(cls, str):
                continue

            issue = None
            if kwarg not in specs.kwonlyargs:
                issue = "Injectable arguments must be keyword arguments only"
            elif not inspect.isclass(cls):
                issue = ("Injectable arguments must be annotated with a"
                         " class type")
            else:
                try:
                    cls()
                except Exception as e:
                    issue = ("Injectable arguments must be able to be"
                             " instantiated through a default constructor"
                             " but if attempted to be instantiated the"
                             " {cls}'s constructor will raise: {exception}"
                             .format(cls=cls.__name__, exception=e))

            if issue is not None:
                raise TypeError(
                    "Argument '{argument}' in function '{function}' cannot"
                    " be injected: {reason}"
                    .format(argument=kwarg, function=func.__name__,
                            reason=issue))

        @wraps(func)
        def wrapper(*args, **kwargs):
            for kwarg, cls in injectables.items():
                if kwarg in kwargs:
                    continue
                if isinstance(cls, str):
                    injected = Lazy(cls, func_module)
                else:
                    injected = cls()
                kwargs[kwarg] = injected
            return func(*args, **kwargs)
        return wrapper

    return decorator
