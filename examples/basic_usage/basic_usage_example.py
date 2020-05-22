"""
In this example you'll grasp the basic ideas behind this framework.

We will be injecting dependencies into our ``BasicUsage`` class's ``__init__`` method
using the :meth:`@autowired <injectable.autowired>` decorator and the
:class:`Autowired <injectable.Autowired>` type annotation.

We declare the classes ``BasicService`` and ``StatefulRepository`` as injectables with
the :meth:`@injectable <injectable.injectable>` decorator to then inject the
``StatefulRepository`` into the ``BasicService`` which in turn will be injected to the
``BasicUsage`` example class.

In ``BasicUsage::run`` we illustrate how each injected dependency is a completely
independent instance of other injections. We inject two ``BasicService`` instances and
each one will be injected with a ``StatefulService`` instance. Finally, we set the state
of each service's repository to demonstrate how they are completely independent.

.. seealso::

    The :ref:`singleton_example` shows how to make a dependency to be shared for all
    injections instead of having the default behavior of independent instances.
"""
# sphinx-start
from examples import Example
from examples.basic_usage.basic_service import BasicService
from injectable import autowired, Autowired, load_injection_container


class BasicUsage(Example):
    @autowired
    def __init__(
        self,
        basic_service: Autowired(BasicService),
        another_basic_service: Autowired(BasicService),
    ):
        self.basic_service = basic_service
        self.another_basic_service = another_basic_service

    def run(self):
        print(self.basic_service.get_repository_state())
        # None

        print(self.another_basic_service.get_repository_state())
        # None

        self.basic_service.set_repository_state("foo")
        self.another_basic_service.set_repository_state("bar")

        print(self.basic_service.get_repository_state())
        # foo

        print(self.another_basic_service.get_repository_state())
        # bar


def run_example():
    load_injection_container()
    example = BasicUsage()
    example.run()


if __name__ == "__main__":
    run_example()
