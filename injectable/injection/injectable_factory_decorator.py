from typing import TypeVar, Callable

from injectable.container.injection_container import InjectionContainer
from injectable.errors.injectable_load_error import InjectableLoadError
from injectable.utils import get_caller_filepath

T = TypeVar("T")


def injectable_factory(
    dependency: T = None,
    *,
    qualifier: str = None,
    primary: bool = False,
    namespace: str = None,
    group: str = None,
    singleton: bool = False,
) -> T:
    """
    Function decorator to mark it as a injectable factory for the dependency.

    At least one of ``dependency`` or ``qualifier`` parameters need to be defined. An
    :class:`InjectableLoadError <injectable.errors.InjectableLoadError>` will be raised
    if none are defined.

    .. note::
        This decorator shall be the first decorator of the function since only the
        received function will be registered as an injectable factory

    .. note::
        All files using this decorator will be executed when
        :meth:`InjectionContainer::load <injectable.InjectionContainer.load>` is
        invoked.

    :param dependency: (optional) the dependency class for which the factory will be
            registered to. Defaults to None.
    :param qualifier: (optional) string qualifier for whoch the factory will be
            registered to. Defaults to None.
    :param primary: (optional) marks the facotry as primary for the dependency
            resolution in ambiguous cases. Defaults to False.
    :param namespace: (optional) namespace in which the factory will be registered.
            Defaults to the default namespace specified in
            :meth:`InjectionContainer::load <injectable.InjectionContainer.load>`.
    :param group: (optional) group to be assigned to the factory. Defaults to None.
    :param singleton: (optional) when True the factory will be used to instantiate a
            singleton, i.e. only one call to the factory will be made and the created
            instance will be shared globally. Defaults to False.

    Usage::

      >>> from injectable import injectable_factory
      >>> from foo import Foo
      >>>
      >>> @injectable_factory(Foo)
      ... def foo_factory() -> Foo:
      ...     return Foo(...)
    """

    if not dependency and not qualifier:
        raise InjectableLoadError("No dependency class nor a qualifier were specified")

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        if get_caller_filepath() == InjectionContainer.LOADING_FILEPATH:
            InjectionContainer._register_factory(
                fn, dependency, qualifier, primary, namespace, group, singleton
            )
        return fn

    return decorator
