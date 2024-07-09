from __future__ import annotations
from typing import Set

import injectable


class InjectionError(RuntimeError):
    """
    Error indicating dependency injection failed.
    """

    def __init__(
        self,
        registry_type: str,
        dependency_name: str,
        matches: Set[injectable.Injectable] = None,
    ):
        message = f"No injectable matches {registry_type} '{dependency_name}'."
        if matches:
            primary_matches = [inj for inj in matches if inj.primary]
            if len(primary_matches) == 0:
                message = (
                    f"No primary injectable registered for {registry_type}:"
                    f" '{dependency_name}'. Unable to resolve unambiguously:"
                    f" {len(primary_matches)} possible matches."
                )
            if len(primary_matches) > 1:
                message = (
                    f"Found {len(primary_matches)} injectables registered as primary"
                    f" for {registry_type}: '{dependency_name}'. Unable to resolve"
                    f" unambiguously."
                )
        self.registry_type = registry_type
        self.dependency_name = dependency_name
        self.matches = matches
        super().__init__(message)
