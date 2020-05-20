from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    def combine(self, a, b):
        ...
