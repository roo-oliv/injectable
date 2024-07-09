"""
In this example you'll see how the :class:`Autowired <injectable.Autowired>` type
annotation can be used with the ``typing.Annotated`` type annotation to separate metadata
from type hints and comply with linters.

.. note::

    When using ``typing.Annotated`` it is possible to omit the dependency type parameter
    in the :class:`Autowired <injectable.Autowired>`. In this case, the first type
    declared in ``typing.Annotated`` will be used. For convenience, one can use
    ``Autowired`` without parenthesis in these situations.

.. seealso::

    The :class:`Autowired <injectable.Autowired>` type annotation can also be used
    directly without using the ``typing.Annotated`` type annotation. The
    :ref:`basic_usage_example` shows how to use it like so.

.. seealso::

    The :ref:`qualifier_overloading_example` details how overloading an injectable
    works by using class inheritance.

.. seealso::

    The :ref:`namespaces_example` details how namespaces work.
"""
# sphinx-start
from typing import Annotated
from examples import Example
from examples.annotated_usage.extended_service import ExtendedService
from examples.annotated_usage.simple_service import SimpleService
from injectable import autowired, Autowired, load_injection_container


class AnnotatedUsage(Example):
    @autowired
    def __init__(
        self,
        simple_service: Annotated[SimpleService, Autowired],
        extended_service: Annotated[SimpleService, Autowired(ExtendedService)],
        fallback_service: Annotated[SimpleService, Autowired(namespace="fallback")],
    ):
        self.simple_service = simple_service
        self.extended_service = extended_service
        self.fallback_service = fallback_service

    def run(self):
        self.simple_service.speak()
        # Simple Service says: Hello!

        self.extended_service.speak()
        # Extended Service says: Hello!

        self.fallback_service.speak()
        # Fallback Service says: Hello!


def run_example():
    load_injection_container()
    example = AnnotatedUsage()
    example.run()


if __name__ == "__main__":
    run_example()
