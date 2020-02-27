from examples.qualifier_overloading.services.sender_service import SenderService
from injectable import injectable


@injectable
class SmsSenderService(SenderService):
    def send(self, message, recipient):
        print(f"Sending SMS to {recipient}: {message}")
