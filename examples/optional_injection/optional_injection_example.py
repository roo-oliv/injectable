"""
In this example you'll see how to declare an injection as optional using
:class:`typing.Optional`.

When a dependency is not found for injection you'll receive an
:exc:`injectable.InjectionError`. This may not be what you want if it is expected and OK
that in some situations the dependency simply won't be present.

In our ``OptionalInjection`` example class we optionally autowire ``ServiceXYZ`` and we
optionally autowire a list of all ``ServiceXYZ`` injectables. We declare the
``ServiceXYZ`` as injectable but in the ``"XYZ"`` namespace.

In this example, both autowirings, ``optional_service`` and
``bunch_of_optional_services``, aren't satisfied by any injectable since there are no
``ServiceXYZ`` declared in the default namespace. But since we declared both injections
as optional, the ``__init__`` method won't fail and instead will inject the value
``None`` to ``optional_service`` and an empty list ``[]`` to
``bunch_of_optional_services``.

.. note::

    The :class:`typing.Optional` type shall be the outermost declared type, so
    ``Autowired(Optional[List[...]])`` will work while
    ``Autowired(List[Optional[...]])`` won't.

.. seealso::

    The :ref:`qualifier_overloading_example` shows how to use :class:`typing.List` to
    get all instances which resolves a dependency instead of just the primary one.
"""

# sphinx-start
from typing import Annotated, Optional, List

from examples import Example
from examples.optional_injection.service_xyz import ServiceXYZ
from injectable import autowired, Autowired, load_injection_container


class OptionalInjection(Example):
    @autowired
    def __init__(
        self,
        optional_service: Annotated[Optional[ServiceXYZ], Autowired],
        bunch_of_optional_services: Annotated[Optional[List[ServiceXYZ]], Autowired],
    ):
        self.optional_service = optional_service
        self.bunch_of_optional_services = bunch_of_optional_services

    def run(self):
        print(self.optional_service)
        # None

        print(self.bunch_of_optional_services)
        # []


def run_example():
    load_injection_container()
    example = OptionalInjection()
    example.run()


if __name__ == "__main__":
    run_example()
