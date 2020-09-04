"""
In this example you'll see how to use the low-level Service Locator API of this
framework.

We will be injecting dependencies inside our ``ServiceLocator`` class's ``__init__``
method by directly using the :meth:`injectable.inject` and
:meth:`injectable.inject_multiple` service locator methods.

We declare the classes ``SampleService``, ``SpecializedService``, and
``StatefulRepository`` as injectables with the
:meth:`@injectable <injectable.injectable>` decorator to then inject the
``StatefulRepository`` into the ``SampleService`` classes which in turn will be injected
to the ``ServiceLocator`` example class.

In ``ServiceLocator::run`` we illustrate how the :meth:`injectable.inject` and
:meth:`injectable.inject_multiple` methods work.

.. note::

    The high-level API, which uses decorators and annotations, is preferred over the
    low-level API.

.. seealso::

    The :ref:`basic_usage_example` describes the high-level API of this framework which
    is based on annotations and decorators.

.. seealso::

    The :ref:`qualifier_overloading_example` details how overloading an injectable
    works by using class inheritance.
"""
# sphinx-start
from examples import Example
from examples.service_locator.sample_service import SampleService
from injectable import load_injection_container, inject, inject_multiple


class ServiceLocator(Example):
    def __init__(
        self,
    ):
        self.primary_basic_service = inject(SampleService)
        self.all_basic_service_implementations = inject_multiple(SampleService)

    def run(self):
        print(self.primary_basic_service.get_repository_state())
        # None

        for service in self.all_basic_service_implementations:
            print(service.get_repository_state())
            # None
            # None

        for service in self.all_basic_service_implementations:
            service.set_repository_state(0)
            print(service.get_repository_state())
            # 0
            # 0

        self.primary_basic_service.set_repository_state(1)

        for service in self.all_basic_service_implementations:
            print(service.get_repository_state())
            # 1
            # 0

        for service in self.all_basic_service_implementations:
            service.set_repository_state(service.get_repository_state() + 1)
            print(service.get_repository_state())
            # 2
            # 1


def run_example():
    load_injection_container()
    example = ServiceLocator()
    example.run()


if __name__ == "__main__":
    run_example()
