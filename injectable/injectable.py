import inspect
from functools import wraps
from typing import Iterable

import logging


def injectable(injectable_kwargs: Iterable[str] = None):
    """
    Returns a functions decorated for injection. The caller can
    explicitly pass into the function wanted dependencies. Any
    dependency not injected by the caller will be automatically
    injected.
    
    >>> try:
    ...     class Dependency:
    ...         def __init__(self):
    ...             self.msg = "dependency initialized"
    ...    
    ...     def foo(*, dep: Dependency):
    ...         return dep.msg
    ...
    ... finally:
    ...     injectable()(foo)()
    'dependency initialized'
    
    :param injectable_kwargs: 
    :return: 
    """
    def decorator(func: callable):
        specs = inspect.getfullargspec(func)

        if injectable_kwargs is None:
            injectables = {
                kwarg: specs.annotations.get(kwarg)
                for kwarg in specs.kwonlyargs
                if (kwarg not in (specs.kwonlydefaults or [])
                    and inspect.isclass(specs.annotations.get(kwarg)))
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

        for kwarg, cls in injectables.items():
            issue = None
            if kwarg not in specs.kwonlyargs:
                issue = ("Injectable arguments must be keyword arguments"
                         " only")
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
                kwargs[kwarg] = cls()
            return func(*args, **kwargs)
        return wrapper

    return decorator
