"""
This is an example of how one can use the testing utility function
:meth:`reset_injection_container <injectable.testing.reset_injection_container>` to
clear all state from the injection container including all registered injectables and
namespaces.
"""
# sphinx-start
from examples import Example
from injectable import (
    injectable,
    autowired,
    Autowired,
    load_injection_container,
)
from injectable.testing import reset_injection_container


@injectable
class Foo:
    def do_something(self):
        print("doing something")


@injectable  # make examples also injectable for testing
class InjectionContainerResetting(Example):
    def run(self):
        self.bar()
        # doing something

        reset_injection_container()

        try:
            self.bar()
            # WARNING:root:Injection Container is empty. Make sure \
            # 'load_injection_container' is being called before any injections are made.
        except KeyError as e:
            print(e.__doc__)
            # Mapping key not found.

    @autowired
    def bar(self, foo: Autowired(Foo)):
        foo.do_something()


if __name__ == "__main__":
    load_injection_container()
    example = InjectionContainerResetting()
    example.run()
