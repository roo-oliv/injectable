"""
In this example you'll see how to declare an injection as lazy and how does it work.

We declare classes ``ServiceA`` and ``ServiceB`` which both print when they are being
instantiated and also when their method ``something`` is invoked.

In our ``LazyInjection`` example class we inject the ``ServiceA`` lazily by
specifying the parameter ``lazy=True`` to :class:`Autowired <injectable.Autowired>` and
we also inject the ``ServiceB`` the default way (not lazy).

You can see that at the ``LazyInjection::__init__`` method the ``ServiceB::__init__``
method is called right at injection time while we do not see the same for ``ServiceA``.

Now, in the ``LazyInjection::run`` method we can see that ``ServiceA::__init__`` is only
called when actually needed, i.e., when we invoke ``ServiceA::something``.

.. seealso::

    The :ref:`cyclic_dependency_example` details how to leverage lazy injection to deal
    with circular references.
"""
# sphinx-start
from examples import Example
from examples.lazy_injection.service_a import ServiceA
from examples.lazy_injection.service_b import ServiceB
from injectable import autowired, Autowired, load_injection_container


class LazyInjection(Example):
    @autowired
    def __init__(
        self, service_a: Autowired(ServiceA, lazy=True), service_b: Autowired(ServiceB)
    ):
        # ServiceB::__init__ called
        print("example init started")
        # example init started
        self.service_a = service_a
        self.service_b = service_b
        print("example init finished")
        # example init finished

    def run(self):
        print("running")
        # running

        self.service_a.something()
        # ServiceA::__init__ called
        # ServiceA::something called

        self.service_b.something()
        # ServiceB::something called


def run_example():
    load_injection_container()
    example = LazyInjection()
    example.run()


if __name__ == "__main__":
    run_example()
