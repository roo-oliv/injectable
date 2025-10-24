"""
In this example you'll learn different ways to select which injectables are
eligible to satisfy a dependency at injection time.

We will use the following selection mechanisms:

1. Groups on injectables: we assign a `group` label when declaring an
   `@injectable` so that it can be included or excluded when autowiring.
2. Excluding groups when injecting: we use the `exclude_groups` parameter on
   `Autowired` to filter out unwanted injectables.
3. Including groups when loading: we call
   :meth:`load_injection_container <injectable.load_injection_container>` with the
   `groups` argument so only injectables declared with those groups (plus those
   without any group) are loaded for resolution across the whole application.

We declare an abstract base class `Processor` and three implementations:
`DefaultProcessor` (no group), `NewProcessor` (group "new"), and `OldProcessor`
(group "old"). In the example we:

- Load the injection container including only the "new" group globally.
- Inject a single `Processor` by selecting the "new" group explicitly.
- Inject all `Processor` implementations without any per-injection filter to show
  the effect of the global "include groups" selection ("old" is filtered out).
- Inject all `Processor` implementations while excluding the "old" group to show
  how per-injection filtering works as well.

.. note::

    When loading with `groups=[...]`, injectables with `group=None` are still
    eligible for injection. The global list works as an allowlist for labeled
    groups but keeps unlabeled injectables available.
"""

# sphinx-start
from typing import Annotated, List
from abc import ABC, abstractmethod

from examples import Example
from injectable import injectable, autowired, Autowired, load_injection_container


class Processor(ABC):
    @abstractmethod
    def process(self, value: int) -> int: ...


@injectable  # no group -> always eligible
class DefaultProcessor(Processor):
    def process(self, value: int) -> int:
        print("DefaultProcessor processing")
        return value + 1


@injectable(group="new")
class NewProcessor(Processor):
    def process(self, value: int) -> int:
        print("NewProcessor processing")
        return value * 2


@injectable(group="old")
class OldProcessor(Processor):
    def process(self, value: int) -> int:
        print("OldProcessor processing")
        return value - 1

@injectable
class UnrelatedClass:
    def run(self):
        print("UnrelatedClass running")


class SelectingDependencies(Example):
    @autowired
    def __init__(
        self,
        # Explicitly pick the "new" group for a single instance
        preferred: Annotated[Processor, Autowired(group="new")],
        # Get all processors; global groups will filter out "old"
        all_allowed: Annotated[List[Processor], Autowired],
        # Per-injection filtering using exclude_groups
        all_but_old: Annotated[List[Processor], Autowired(exclude_groups=["old"])],
        # Unrelated injectable, not affected by the selection
        unrelated: Annotated[UnrelatedClass, Autowired],
    ):
        self.preferred = preferred
        self.all_allowed = all_allowed
        self.all_but_old = all_but_old
        self.unrelated = unrelated

    def run(self):
        print(self.preferred.process(3))
        # NewProcessor processing
        # 6

        print([type(p).__name__ for p in self.all_allowed])
        # ['DefaultProcessor', 'NewProcessor']

        print([type(p).__name__ for p in self.all_but_old])
        # ['DefaultProcessor', 'NewProcessor']

        self.unrelated.run()
        # UnrelatedClass running


def run_example():
    # Only injectables with group "new" (and with no group) will be considered
    # across the whole application. This demonstrates the global selection toggle.
    load_injection_container(groups=["new"])
    example = SelectingDependencies()
    example.run()


if __name__ == "__main__":
    run_example()
