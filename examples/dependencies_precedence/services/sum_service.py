from examples.dependencies_precedence.services.abstract_service import AbstractService
from injectable import injectable


@injectable(qualifier="sum", primary=True)
class SumService(AbstractService):
    def combine(self, a, b):
        return a + b
