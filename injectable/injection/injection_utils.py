import logging
from enum import Enum
from typing import Sequence, Set, Union, Type, TypeVar

from injectable.container.injection_container import InjectionContainer
from injectable.container.injectable import Injectable
from injectable.errors import InjectionError

T = TypeVar("T")


class RegistryType(Enum):
    CLASS = "class"
    QUALIFIER = "qualifier"


def get_dependency_registry_type(dependency: Union[Type[T], str]) -> RegistryType:
    return RegistryType.QUALIFIER if isinstance(dependency, str) else RegistryType.CLASS


def get_namespace_injectables(
    dependency_name: str, registry_type: RegistryType, namespace: str
) -> Set[Injectable]:
    if len(InjectionContainer.NAMESPACES) == 0:
        logging.warning(
            "Injection Container is empty. Make sure 'load_injection_container'"
            " is being called before any injections are made."
        )
    injection_namespace = InjectionContainer.NAMESPACES.get(namespace)
    if not injection_namespace:
        return set()
    registry = (
        injection_namespace.class_registry
        if registry_type is RegistryType.CLASS
        else injection_namespace.qualifier_registry
    )
    injectables = registry.get(dependency_name)
    return injectables


def filter_by_group(
    matches: Set[Injectable], group: str = None, exclude_groups: Sequence[str] = None,
) -> Set[Injectable]:
    exclude = exclude_groups or []
    matches = {
        inj
        for inj in matches
        if (group is None or inj.group == group) and inj.group not in exclude
    }
    return matches


def resolve_single_injectable(
    dependency_name: str, registry_type: RegistryType, matches: Set[Injectable]
) -> Injectable:
    if len(matches) == 1:
        for injectable in matches:
            return injectable

    primary_matches = [inj for inj in matches if inj.primary]
    if len(primary_matches) == 0:
        raise InjectionError(
            f"No primary injectable registered for {registry_type.value}:"
            f" '{dependency_name}'. Unable to resolve unambiguously: {len(matches)}"
            f" possible matches."
        )
    if len(primary_matches) > 1:
        raise InjectionError(
            f"Found {len(primary_matches)} injectables registered as primary for "
            f"{registry_type.value}: '{dependency_name}'. Unable to resolve"
            f" unambiguously."
        )
    return primary_matches[0]
