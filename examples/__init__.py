from abc import ABC, abstractmethod


class Example(ABC):
    @abstractmethod
    def run(self):
        ...
