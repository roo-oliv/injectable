from abc import ABC, abstractmethod


class SenderService(ABC):
    @abstractmethod
    def send(self, message, recipient):
        ...
