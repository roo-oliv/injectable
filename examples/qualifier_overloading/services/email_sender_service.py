from examples.qualifier_overloading.services.sender_service import SenderService
from injectable import injectable


@injectable
class EmailSenderService(SenderService):
    def send(self, message, recipient):
        print(f"Sending Email to {recipient}: {message}")
