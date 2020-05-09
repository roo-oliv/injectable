import uuid

from dataclasses import dataclass, field
from typing import Optional

from cached_property import cached_property
from lazy_object_proxy import Proxy


@dataclass(frozen=True)
class Injectable:
    """
    Injectable is the low-level container class in which information regarding an
    injectable dependency is stored for registering in a namespace.

    This class is not meant for direct usage. It should be used in conjunction with
    the :py:mod:`injectable.testing` module utilities for testing purposes only.

    :param constructor: callable to be used as constructor when injecting.
    :param unique_id: (optional) unique identifier for the injectable which prevents
            duplicates of the same injectable to be registered. Defaults to a UUID
            generated at initialization time.
    :param primary: (optional) marks the injectable as primary for resolution in
            ambiguous cases. Defaults to False.
    :param group: (optional) group to be assigned to the injectable. Defaults to None.
    :param singleton: (optional) when True the injectable will be a singleton, i.e. only
            one instance of it will be created and shared globally. Defaults to False.
    """

    constructor: callable = field(compare=False)
    unique_id: str = field(default_factory=lambda: uuid.uuid1().hex)
    primary: bool = False
    group: Optional[str] = None
    singleton: bool = False

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
