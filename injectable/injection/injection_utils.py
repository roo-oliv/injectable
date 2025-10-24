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
    matches: Set[Injectable],
    group: str = None,
    exclude_groups: Sequence[str] = None,
) -> Set[Injectable]:
    matches = _filter_by_container_groups(matches)
    matches = _filter_by_group_and_exclude(matches, group, exclude_groups)

    return matches


def _filter_by_container_groups(matches: Set[Injectable]) -> Set[Injectable]:
    container_groups = InjectionContainer.GROUPS or []
    if not container_groups or not any(
        [i for i in matches if i.group in container_groups]
    ):
        return matches

    container_matches = {
        inj for inj in matches if inj.group is None or inj.group in container_groups
    }

    return container_matches


def _filter_by_group_and_exclude(matches, group, exclude_groups):
    exclude = exclude_groups or []
    return {
        inj
        for inj in matches
        if (group is None or inj.group == group) and inj.group not in exclude
    }


def resolve_single_injectable(
    dependency_name: str, registry_type: RegistryType, matches: Set[Injectable]
) -> Injectable:
    if len(matches) == 1:
        for injectable in matches:
            return injectable

    primary_matches = [inj for inj in matches if inj.primary]
    if len(primary_matches) != 1:
        raise InjectionError(registry_type.value, dependency_name, matches)
    return primary_matches[0]
