from functools import wraps
import inspect
import logging

from lazy_object_proxy import Proxy
from typing import Iterable

from injectable.util import get_class, is_injectable, is_lazy


def injectable(injectable_kwargs: Iterable[str] = None, *, lazy: bool = False):
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
    :param lazy: flag to force lazy initialization of all dependencies
    :return: the function with all injectable arguments initialized
    """
    def decorator(func: callable):
        func_module = inspect.getmodule(func).__dict__
        specs = inspect.getfullargspec(func)

        if injectable_kwargs is None:
            injectables = {
                kwarg: specs.annotations.get(kwarg)
                for kwarg in specs.kwonlyargs if is_injectable(kwarg, specs)
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

        redundant_lazy_use = False
        for kwarg, ref in injectables.items():
            if is_lazy(ref):
                redundant_lazy_use = lazy
                continue

            if not isinstance(ref, str):
                continue

            cls = get_class(ref, func_module)
            if cls is None:
                continue

            injectables[kwarg] = cls

        if redundant_lazy_use:
            logging.warning("@injectable decorator is set to always lazy"
                            " initialize dependencies. Usage of 'lazy'"
                            " function to mark dependencies as lazy is"
                            " redundant")

        for kwarg, cls in injectables.items():
            issue = None
            if kwarg not in specs.kwonlyargs:
                issue = "Injectable arguments must be keyword arguments only"

            if issue is None and (lazy or is_lazy(cls)):
                continue

            if isinstance(cls, str):
                cls = get_class(cls, func_module)

            if issue is None and cls is None:
                issue = ("Unable to find a reference to the annotated class."
                         " You may want to try marking this dependency as"
                         " lazy: ... {argument}: lazy('YourClass') ...")

            if issue is None and not inspect.isclass(cls):
                issue = ("Injectable arguments must be annotated with a"
                         " class type")

            if issue is None:
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
            for kwarg, reference in injectables.items():
                if kwarg in kwargs:
                    continue
                kwargs[kwarg] = get_instance(reference, func_module, lazy)
            return func(*args, **kwargs)
        return wrapper

    return decorator


def get_instance(reference, func_module, force_lazy):
    if isinstance(reference, str):
        if force_lazy:
            return Proxy(lambda: get_class(reference, func_module)())

        return get_class(reference, func_module)()

    if is_lazy(reference):
        if isinstance(reference(), str):
            r = reference()
            return Proxy(lambda: get_class(r, func_module)())

        return Proxy(reference())

    if force_lazy:
        return Proxy(reference)

    return reference()
