"""
This example demonstrates basic usage of injectables:
 * Injecting a dependency
 * Injecting a dependency which in turns injects some other dependency on it's own
 * Whenever the autowired function is called new instances of the autowired dependencies
        are injected unless for autowired dependencies marked as singletons. See more at
        the `singletons` example)
"""
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
        print(f"SimpleService.counter: {self.simple_service.counter}")
        print(
            f"DependableService.simple_service.counter:"
            f" {self.dependable_service.simple_service.counter}"
        )
        print()
        print(f"SimpleService.add_one() ...")
        self.simple_service.add_one()
        print(f"SimpleService.counter: {self.simple_service.counter}")
        print(
            f"DependableService.simple_service.counter:"
            f" {self.dependable_service.simple_service.counter}"
        )
        print()
        print(f"DependableService.add_two() ...")
        self.dependable_service.add_two()
        print(f"SimpleService.counter: {self.simple_service.counter}")
        print(
            f"DependableService.simple_service.counter:"
            f" {self.dependable_service.simple_service.counter}"
        )


if __name__ == "__main__":
    InjectionContainer.load()
    example = BasicUsage()
    example.run()
