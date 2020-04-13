"""
In this example you'll see how we define dependencies as singletons and demonstrate its
behaviour.
"""
# sphinx-start
from examples import Example
from examples.singletons.services.composite_singleton import CompositeSingleton
from examples.singletons.services.simple_singleton import SimpleSingleton
from injectable import injectable, Autowired, autowired
from injectable.container.injection_container import InjectionContainer


@injectable  # make examples also injectable for testing
class Singletons(Example):
    @autowired
    def __init__(
        self,
        composite_singleton: Autowired(CompositeSingleton),
        simple_singleton: Autowired(SimpleSingleton),
    ):
        self.composite_singleton = composite_singleton
        self.simple_singleton = simple_singleton

    def run(self):
        self.composite_singleton.counter = 10
        print(self.simple_singleton.counter)
        # 10

        self.simple_singleton.counter -= 5
        print(self.composite_singleton.counter)
        # 5


if __name__ == "__main__":
    InjectionContainer.load()
    example = Singletons()
    example.run()
