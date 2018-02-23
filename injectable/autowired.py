from functools import wraps
import inspect
import logging

from lazy_object_proxy import Proxy
from typing import Iterable

from injectable.util import get_class, is_injectable, is_lazy


def autowired(injectable_kwargs: Iterable[str] = None, *, lazy: bool = False):
    """
    Returns a function decorated for injection. The caller can
    explicitly pass into the function wanted dependencies. Any
    dependency not injected by the caller will be automatically
    autowired.
    
    This decorator can be used with or without parenthesis.
    
    >>> class Dependency:
    ...     def __init__(self):
    ...         self.msg = "dependency initialized"
    ...
    >>> @autowired
    ... def foo(*, dep: Dependency):
    ...     return dep.msg
    ...
    >>> foo()
    'dependency initialized'
    
    :param injectable_kwargs: explicit list of which arguments to autowire
    :param lazy: flag to force lazy initialization of all dependencies
    :return: the function with all injectable arguments autowired
    """
    f = None
    if callable(injectable_kwargs):
        f = injectable_kwargs
        injectable_kwargs = None

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
                                " '@autowired' but no arguments that"
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
            logging.warning("@autowired decorator is set to always lazy"
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
                         " lazy: ... {argument}: lazy('YourClass') ..."
                         .format(argument=kwarg))

            if issue is None and not inspect.isclass(cls):
                issue = ("Injectable arguments must be annotated with a"
                         " class type")

            if issue is None:
                cls_spec = inspect.getfullargspec(cls)
                required_args = (len(cls_spec.args)
                                 - (len(cls_spec.defaults)
                                    if cls_spec.defaults is not None
                                    else 0))
                if required_args != 0 and cls_spec.args[0] in ('self', 'cls'):
                    required_args -= 1
                required_kwargs = (len(cls_spec.kwonlyargs)
                                   - (len(cls_spec.kwonlydefaults)
                                      if cls_spec.kwonlydefaults is not None
                                      else 0))
                if required_args == 0 and required_kwargs == 0:
                    continue

                args_issue = (
                    "{n} positional arguments".format(n=required_args)
                    if required_args != 0 else "")
                kwargs_issue = (
                    (" and " if args_issue else "")
                    + "{n} named arguments".format(n=required_kwargs)
                ) if required_kwargs != 0 else ""
                expectancy = args_issue + kwargs_issue
                issue = ("Injectable dependencies must provide a default"
                         " constructor with no required arguments but"
                         " {cls} expects {expectancy}"
                         .format(cls=cls.__name__, expectancy=expectancy))

            raise TypeError(
                "Argument '{argument}' in function '{function}' cannot"
                " be autowired: {reason}"
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

    if f is not None:
        return decorator(f)

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
