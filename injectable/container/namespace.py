import inspect
from typing import Dict, List, Optional

from injectable.container.injectable import Injectable


class Namespace:
    def __init__(self):
        self.class_registry: Dict[str, List[Injectable]] = {}
        self.qualifier_registry: Dict[str, List[Injectable]] = {}

    def register_injectable(
        self,
        injectable: Injectable,
        klass: Optional[type] = None,
        qualifier: Optional[str] = None,
    ):
        if qualifier:
            self._register_to_qualifier(qualifier, injectable)
        if klass:
            self._register_to_class(klass, injectable)
            for base_class in klass.__bases__:
                if inspect.isbuiltin(base_class):
                    continue
                self.register_injectable(injectable, base_class)

    def _register_to_class(
        self, klass: type, injectable: Injectable,
    ):
        qualified_name = klass.__qualname__
        if qualified_name not in self.class_registry:
            self.class_registry[qualified_name] = []
        self.class_registry[qualified_name].append(injectable)

    def _register_to_qualifier(
        self, qualifier: str, injectable: Injectable,
    ):
        if qualifier not in self.qualifier_registry:
            self.qualifier_registry[qualifier] = []
        self.qualifier_registry[qualifier].append(injectable)
