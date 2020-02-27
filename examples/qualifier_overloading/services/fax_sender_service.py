from examples.qualifier_overloading.services.sender_service import SenderService
from injectable import injectable


@injectable(group="old")
class FaxSenderService(SenderService):
    def send(self, message, recipient):
        print(f"Sending Fax to {recipient}: {message}")
