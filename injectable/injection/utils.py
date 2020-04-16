from typing import List, Tuple, Sequence

from injectable.container.injection_container import InjectionContainer
from injectable.container.injectable import Injectable
from injectable.errors import (
    InjectionContainerNotLoadedError,
    InjectionError,
)


def get_namespace_injectables(
    dependency: Injectable, namespace: str
) -> Tuple[List[Injectable], str, str]:
    if len(InjectionContainer.CONTEXT) == 0:
        raise InjectionContainerNotLoadedError(
            "InjectionContainer::load was not invoked"
        )
    injection_namespace = InjectionContainer.CONTEXT[
        namespace or InjectionContainer.DEFAULT_NAMESPACE
    ]
    if isinstance(dependency, str):
        registry = injection_namespace.qualifier_registry
        lookup_key = dependency
        lookup_type = "qualifier"
    else:
        registry = injection_namespace.class_registry
        lookup_key = dependency.__qualname__
        lookup_type = "class"

    injectables = registry.get(lookup_key)
    return injectables, lookup_key, lookup_type


def filter_by_group(
    matches: Sequence[Injectable],
    *,
    lookup_key: str,
    lookup_type: str,
    group: str = None,
    exclude_groups: Sequence[str] = None,
) -> List[Injectable]:
    exclude = exclude_groups or []
    matches = [
        inj
        for inj in matches
        if (group is None or inj.group == group) and inj.group not in exclude
    ]
    return matches


def resolve_single_injectable(lookup_key, lookup_type, matches) -> Injectable:
    if len(matches) == 1:
        injectable = matches[0]
    else:
        primary_matches = [inj for inj in matches if inj.primary]
        if len(primary_matches) == 0:
            raise InjectionError(
                f"No primary injectable registered for {lookup_type}: '{lookup_key}'. "
                f"Unable to resolve unambiguously: {len(matches)} possible matches."
            )
        if len(primary_matches) > 1:
            raise InjectionError(
                f"Found {len(primary_matches)} injectables registered as primary for "
                f"{lookup_type}: '{lookup_key}'. Unable to resolve unambiguously."
            )
        injectable = primary_matches[0]
    return injectable
