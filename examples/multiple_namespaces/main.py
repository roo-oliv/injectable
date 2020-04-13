"""
In this example you'll see how we can use multiple namespaces for dependency injection.
"""
# sphinx-start
from examples import Example
from injectable import Autowired, autowired, injectable, InjectionContainer


@injectable  # make examples also injectable for testing
class MultipleNamespaces(Example):
    @autowired
    def __init__(
        self,
        even_counter: Autowired("counter"),
        odd_counter: Autowired("counter", namespace="odd"),
    ):
        self.even_counter = even_counter
        self.odd_counter = odd_counter

    def run(self):
        self.even_counter.add()
        self.odd_counter.add()
        print(self.even_counter.counter)
        # 2

        print(self.odd_counter.counter)
        # 3


if __name__ == "__main__":
    InjectionContainer.load()
    example = MultipleNamespaces()
    example.run()
