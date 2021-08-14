"""
In this example you'll see how to supply an already-initialized instance as injectable.

For whatever reason we have already initialized an instance of ``Application`` and
assigned it to the ``app`` variable so we use the
:meth:`injectable_factory <injectable.injectable_factory>` decorator in a lambda which
in turn just returns the existing ``app``.

Now our ``InjectingExistingInstance`` example class can be injected with our existing
``Application`` instance.

.. seealso::

    The :meth:`injectable_factory <injectable.injectable_factory>` decorator can also be
    used in regular functions and not just in lambdas. The :ref:`factory_example` shows
    how to use it.
"""
# sphinx-start
from examples import Example
from examples.injecting_existing_instance.app import Application
from injectable import autowired, Autowired, load_injection_container


class InjectingExistingInstance(Example):
    @autowired
    def __init__(
        self,
        app: Autowired(Application),
    ):
        self.app = app

    def run(self):
        print(self.app.number)
        # 42


def run_example():
    load_injection_container()
    example = InjectingExistingInstance()
    example.run()


if __name__ == "__main__":
    run_example()
