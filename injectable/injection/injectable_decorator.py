from typing import TypeVar

from injectable.container.injection_container import InjectionContainer
from injectable.utils import get_caller_filepath

T = TypeVar("T")


def injectable(
    cls: T = None,
    *,
    qualifier: str = None,
    primary: bool = False,
    namespace: str = None,
    group: str = None,
    singleton: bool = False,
) -> T:
    """
    Class decorator to mark it as an injectable dependency.

    This decorator accepts customization parameters but can be invoked without the
    parenthesis when no parameter will be specified.

    .. note::
        All files using this decorator will be executed when
        :meth:`InjectionContainer::load <injectable.InjectionContainer.load>` is
        invoked.

    :param cls: (cannot be explicitly passed) the decorated class. This will be
            automatically passed to the decorator by Python magic.
    :param qualifier: (optional) string qualifier for the injectable to be registered
            with. Defaults to None.
    :param primary: (optional) marks the injectable as primary for resolution in
            ambiguous cases. Defaults to False.
    :param namespace: (optional) namespace in which the injectable will be registered.
            Defaults to the default namespace specified in
            :meth:`InjectionContainer::load <injectable.InjectionContainer.load>`.
    :param group: (optional) group to be assigned to the injectable. Defaults to None.
    :param singleton: (optional) when True the injectable will be a singleton, i.e. only
            one instance of it will be created and shared globally. Defaults to False.

    Usage::

      >>> from injectable import injectable
      >>>
      >>> @injectable
      ... class Foo:
      ...     ...
    """

    def decorator(klass: T, direct_call: bool = False) -> T:
        steps_back = 3 if direct_call else 2
        if get_caller_filepath(steps_back) == InjectionContainer.LOADING_FILEPATH:
            InjectionContainer._register_injectable(
                klass, qualifier, primary, namespace, group, singleton
            )
        return klass

    return decorator(cls, True) if cls is not None else decorator
