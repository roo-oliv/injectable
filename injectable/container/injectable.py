from dataclasses import dataclass, field
from typing import Optional

from cached_property import cached_property
from lazy_object_proxy import Proxy


@dataclass(frozen=True)
class Injectable:
    constructor: callable = field(compare=False)
    unique_id: str
    primary: bool
    group: Optional[str]
    singleton: bool

    @cached_property
    def singleton_instance(self):
        return self.constructor()

    @cached_property
    def factory(self):
        if self.singleton:
            return lambda: self.singleton_instance
        return self.constructor

    def get_instance(self, *, lazy: bool = False):
        if lazy:
            return Proxy(self.factory)
        return self.factory()
