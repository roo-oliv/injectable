from typing import Dict, Optional, Set

from injectable.container.injectable import Injectable
from injectable.common_utils import get_dependency_name


class Namespace:
    def __init__(self):
        self.class_registry: Dict[str, Set[Injectable]] = {}
        self.qualifier_registry: Dict[str, Set[Injectable]] = {}

    def register_injectable(
        self,
        injectable: Injectable,
        klass: Optional[type] = None,
        qualifier: Optional[str] = None,
        propagate: bool = True,
    ):
        if qualifier:
            self._register_to_qualifier(qualifier, injectable)
        if klass:
            self._register_to_class(klass, injectable)
            if not propagate:
                return
            for base_class in klass.__bases__:
                self.register_injectable(injectable, base_class, propagate=propagate)

    def _register_to_class(
        self, klass: type, injectable: Injectable,
    ):
        qualified_name = get_dependency_name(klass)
        if qualified_name not in self.class_registry:
            self.class_registry[qualified_name] = set()
        self.class_registry[qualified_name].add(injectable)

    def _register_to_qualifier(
        self, qualifier: str, injectable: Injectable,
    ):
        if qualifier not in self.qualifier_registry:
            self.qualifier_registry[qualifier] = set()
        self.qualifier_registry[qualifier].add(injectable)
