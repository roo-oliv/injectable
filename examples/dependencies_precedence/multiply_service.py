from examples.dependencies_precedence.abstract_service import AbstractService
from injectable import injectable


@injectable(qualifier="multiply")
class MultiplyService(AbstractService):
    def combine(self, a, b):
        print(f"{a} * {b} = {a * b}")
