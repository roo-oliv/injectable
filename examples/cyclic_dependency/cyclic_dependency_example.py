"""
In this example you'll learn how the injectable framework can make it easier to deal
with circular references.

We use qualifiers to register ours cyclic-dependent services which will enable us to
refer to these dependencies by their qualifier string when injecting the services into
our ``CyclicDependency`` example class instead of having to import them and possibly
falling into a cyclic import loop.

For each of the services we inject the other one with a lazy modifier which will prevent
us from falling into an instantiation loop as lazy dependencies are only instantiated
when its attributes are accessed or its methods are invoked.

.. seealso::

    The :ref:`lazy_injection_example` details how lazy injection works.
"""
# sphinx-start
from examples import Example
from injectable import Autowired, autowired, load_injection_container


class CyclicDependency(Example):
    @autowired
    def __init__(self, service_a: Autowired("A"), service_b: Autowired("B")):
        self.service_a = service_a
        self.service_b = service_b

    def run(self):
        print(self.service_a.get_some_property_from_b)
        # some property from B

        print(self.service_b.get_some_property_from_a)
        # some property from A


def run_example():
    load_injection_container()
    example = CyclicDependency()
    example.run()


if __name__ == "__main__":
    run_example()
