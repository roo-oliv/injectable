"""
This is an example of how one can use the testing utility functions
:meth:`clear_injectables <injectable.testing.clear_injectables>` and
:meth:`register_injectables <injectable.testing.register_injectables>` for mocking
a dependency for tests.
"""
# sphinx-start
from unittest.mock import Mock

from examples import Example
from injectable import (
    injectable,
    autowired,
    Autowired,
    Injectable,
    load_injection_container,
)
from injectable.testing import clear_injectables, register_injectables


@injectable
class RealDep:
    @staticmethod
    def print():
        print("RealDep")


class InjectableMocking(Example):
    def __init__(self):
        clear_injectables(RealDep)
        mocked_dep = Mock(wraps=RealDep)
        mocked_dep.print = Mock(side_effect=lambda: print("MockedDep"))
        mocked_injectable = Injectable(lambda: mocked_dep)
        register_injectables({mocked_injectable}, RealDep)

    @autowired
    def run(self, dep: Autowired(RealDep)):
        dep.print()
        # MockedDep
        dep.print.assert_called()


def run_example():
    load_injection_container()
    example = InjectableMocking()
    example.run()


if __name__ == "__main__":
    run_example()
