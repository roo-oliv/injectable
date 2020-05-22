"""
In this example you'll learn about overloading qualifiers/classes for injection and how
to take advantage of that to inject multiple dependencies as a list of instances.

Overloading happens when two or more injectables are declared for a same qualifier
or class.

In this example we create a abstract base class ``SenderService`` and implement it in
other three classes, ``EmailSenderService``, ``SmsSenderService``, and
``FaxSenderService``. All the three concrete services are declared as injectables and
as injection declared class propagates to base classes we end up with three injectables
declared for the ``SenderService`` class.

In our ``QualifierOverloading`` example class we inject a list with all injectables
declared for the ``SenderService`` by using the :class:`typing.List` type. We also use
the ``exclude_groups`` parameter to filter out injectables that were declared with the
``"old"`` group label.

.. seealso::

    The :ref:`dependencies_precedence_example` shows how dependency resolution works in
    regards to precedence when a qualifier or class are resolved by multiple
    injectables and you're injecting a single instance and not all matching injectables.
"""
# sphinx-start
from typing import List

from examples import Example
from examples.qualifier_overloading.sender_service import SenderService
from injectable import autowired, Autowired, load_injection_container


class QualifierOverloading(Example):
    @autowired
    def __init__(
        self, sender_services: Autowired(List[SenderService], exclude_groups=["old"]),
    ):
        self.sender_services = sender_services

    def send_message(self, message: str, recipient: str):
        for sender_service in self.sender_services:
            sender_service.send(message, recipient)

    def run(self):
        self.send_message(message="Hello!", recipient="World")
        # Sending Email to World: Hello!
        # Sending SMS to World: Hello!


def run_example():
    load_injection_container()
    example = QualifierOverloading()
    example.run()


if __name__ == "__main__":
    run_example()
