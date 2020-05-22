"""
In this example you'll see how we define dependencies as singletons and how they behave.

A singleton injectable is instantiated only once and then this same instance is used
whenever an injection is made.

In our ``Singleton`` example class we inject two parameters, ``client1`` and ``client2``
both with the ``SingletonClient`` class, which in turn, was declared as singleton.

When we run our example we can see that, as there is only one instance being shared
between injections a change to its state is then reflected to every other place injected
with it.
"""
# sphinx-start
from examples import Example
from examples.singletons.singleton_client import SingletonClient
from injectable import Autowired, autowired, load_injection_container


class Singletons(Example):
    @autowired
    def __init__(
        self, client1: Autowired(SingletonClient), client2: Autowired(SingletonClient),
    ):
        self.client1 = client1
        self.client2 = client2

    def run(self):
        print(self.client1.connected)
        # False

        print(self.client2.connected)
        # False

        self.client1.connect()
        print(self.client1.connected)
        # True

        print(self.client2.connected)
        # True


def run_example():
    load_injection_container()
    example = Singletons()
    example.run()


if __name__ == "__main__":
    run_example()
