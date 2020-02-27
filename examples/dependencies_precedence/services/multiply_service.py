from examples.dependencies_precedence.services.abstract_service import AbstractService
from injectable import injectable


@injectable(qualifier="multiply")
class MultiplyService(AbstractService):
    def combine(self, a, b):
        return a * b
