"""
In this example you'll see how to declare an injection as optional using
:class:`typing.Optional`.
"""
# sphinx-start
from typing import Optional, List

from examples import Example
from injectable import autowired, Autowired, injectable, InjectionContainer


@injectable  # make examples also injectable for testing
class OptionalInjection(Example):
    @autowired
    def __init__(
        self,
        some_service: Autowired(Optional["foo"]),
        bunch_of_services: Autowired(Optional[List["bar"]]),
    ):
        self.some_service = some_service
        self.bunch_of_services = bunch_of_services

    def run(self):
        print(self.some_service)
        # None

        print(self.bunch_of_services)
        # []


if __name__ == "__main__":
    InjectionContainer.load()
    example = OptionalInjection()
    example.run()
