from typing import Union, Set

from injectable import InjectionContainer
from injectable.common_utils import get_dependency_name
from injectable.container.injectable import Injectable
from injectable.constants import DEFAULT_NAMESPACE


def clear_injectables(
    dependency: Union[type, str], namespace: str = None
) -> Set[Injectable]:
    """
    Utility function to clear all injectables registered for the dependency in a given
    namespace. Returns a set containing all cleared injectables.

    :param dependency: class or qualifier of the dependency.
    :param namespace: (optional) namespace in which the injectable will be registered.
            Defaults to :const:`injectable.constants.DEFAULT_NAMESPACE`.

    Usage::

      >>> from injectable.testing import clear_injectables
      >>> clear_injectables("foo")

    .. versionadded:: 3.3.0
    """
    namespace = InjectionContainer.NAMESPACES[namespace or DEFAULT_NAMESPACE]
    if isinstance(dependency, str):
        injectables = namespace.qualifier_registry[dependency]
        namespace.qualifier_registry[dependency] = set()
    else:
        dependency_name = get_dependency_name(dependency)
        injectables = namespace.class_registry[dependency_name]
        namespace.class_registry[dependency_name] = set()
    return injectables
