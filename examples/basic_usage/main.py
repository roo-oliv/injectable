"""
In this example you'll grasp the basic ideas behind the framework.

We will be injecting dependencies into our ``BasicUsage`` class's ``__init__`` method
using the ``@autowired`` decorator and the ``Autowired`` type annotation.

We declare classes ``SimpleService`` and ``DependableService`` as injectables with the
``@injectable`` decorator and we also inject the ``SimpleService`` into the
``DependableService``.

In ``BasicUsage::run`` we illustrate how each injected ``SimpleService`` is a completely
independent instance of other injections.
"""
# sphinx-start
from examples import Example
from examples.basic_usage.services.dependable_service import DependableService
from examples.basic_usage.services.simple_service import SimpleService
from injectable import autowired, Autowired, injectable, InjectionContainer


@injectable  # make examples also injectable for testing
class BasicUsage(Example):
    @autowired
    def __init__(
        self,
        simple_service: Autowired(SimpleService),
        dependable_service: Autowired(DependableService),
    ):
        self.simple_service = simple_service
        self.dependable_service = dependable_service

    def run(self):
        print(self.simple_service.counter)
        # 0

        print(self.dependable_service.simple_service.counter)
        # 0

        self.simple_service.add_one()
        print(self.simple_service.counter)
        # 1

        print(self.dependable_service.simple_service.counter)
        # 0

        self.dependable_service.add_two()
        print(self.simple_service.counter)
        # 1

        print(self.dependable_service.simple_service.counter)
        # 2


if __name__ == "__main__":
    InjectionContainer.load()
    example = BasicUsage()
    example.run()
