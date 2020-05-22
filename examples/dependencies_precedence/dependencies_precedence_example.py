"""
In this example you'll see the use of declaring an injectable as primary and the use
of explicitly declared qualifiers.

We declare an abstract base class ``AbstractService`` which exposes an abstract
``combine`` method. The classes ``SumService`` and ``MultiplyService`` both implement
``AbstractService`` and are declared as injectable though we specify different
qualifiers for each and also declare ``SumService`` as primary.

Now, when we inject an ``AbstractService`` into our ``DependenciesPrecedence`` example
class we will get an instance of the ``SumService`` class since we declared it as
primary. We inject a ``MultipleService`` instance as well by using the explicit
qualifier attributed to it.

.. note::

    If ``SumService`` wasn't declared as primary then injecting ``AbstractService``
    would have failed and raised an error indicating there was ambiguity in resolving
    the specified dependency.

.. seealso::

    The :ref:`qualifier_overloading_example` shows how to get all instances which
    resolves a dependency instead of just the primary one.
"""
# sphinx-start
from examples import Example
from examples.dependencies_precedence.abstract_service import AbstractService
from injectable import (
    autowired,
    Autowired,
    load_injection_container,
)


class DependenciesPrecedence(Example):
    @autowired
    def __init__(
        self,
        abstract_service_1: Autowired(AbstractService),
        abstract_service_2: Autowired("multiply"),
    ):
        self.abstract_service_1 = abstract_service_1
        self.abstract_service_2 = abstract_service_2

    def run(self):
        self.abstract_service_1.combine(4, 2)
        # 4 + 2 = 6

        self.abstract_service_2.combine(4, 2)
        # 4 * 2 = 8


def run_example():
    load_injection_container()
    example = DependenciesPrecedence()
    example.run()


if __name__ == "__main__":
    run_example()
