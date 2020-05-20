from examples.dependencies_precedence.abstract_service import AbstractService
from injectable import injectable


@injectable(qualifier="sum", primary=True)
class SumService(AbstractService):
    def combine(self, a, b):
        print(f"{a} + {b} = {a + b}")
