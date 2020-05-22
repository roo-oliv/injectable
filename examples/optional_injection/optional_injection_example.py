"""
In this example you'll see how to declare an injection as optional using
:class:`typing.Optional`.

When a dependency is not found for injection you'll receive an
:exc:`injectable.InjectionError`. This may not be what you want if it is expected and OK
that in some situations the dependency simply won't be present.

In our ``OptionalInjection`` example class we optionally autowire the ``some_service``
argument with the ``"foo"`` qualifier and we optionally autowire the
``bunch_of_services`` argument with a list of all injectables that satisfy the ``"bar"``
qualifier.

In this example, both qualifiers, ``"foo"`` and ``"bar"``, aren't declared by any
injectable though as we declared both injections as optional, the ``__init__`` method
won't fail and instead will inject the value ``None`` to ``some_service`` and an empty
list ``[]`` to ``bunch_of_services``.

.. note::

    The :class:`typing.Optional` type shall be the outermost declared type, so
    ``Autowired(Optional[List[...]])`` will work while
    ``Autowired(List[Optional[...]])`` won't.

.. seealso::

    The :ref:`qualifier_overloading_example` shows how to use :class:`typing.List` to
    get all instances which resolves a dependency instead of just the primary one.
"""
# sphinx-start
from typing import Optional, List

from examples import Example
from injectable import autowired, Autowired, load_injection_container


class OptionalInjection(Example):
    @autowired
    def __init__(
        self,
        some_service: Autowired(Optional["foo"]),
        bunch_of_services: Autowired(Optional[List["bar"]]),
    ):
        self.some_service = some_service
        self.bunch_of_services = bunch_of_services

    def run(self):
        print(self.some_service)
        # None

        print(self.bunch_of_services)
        # []


def run_example():
    load_injection_container()
    example = OptionalInjection()
    example.run()


if __name__ == "__main__":
    run_example()
