from typing import Optional

from cached_property import cached_property
from lazy_object_proxy import Proxy


class Injectable:
    def __init__(
        self,
        constructor: callable,
        primary: bool,
        group: Optional[str],
        singleton: bool,
    ):
        self._constructor = constructor
        self.primary = primary
        self.group = group
        self.singleton = singleton
        self._factory = constructor if not singleton else lambda: self.get_singleton

    @cached_property
    def get_singleton(self):
        return self._constructor()

    def get_instance(self, *, lazy: bool = False):
        return self._factory() if not lazy else Proxy(self._factory)
