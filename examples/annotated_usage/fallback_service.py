from examples.annotated_usage.simple_service import SimpleService
from injectable import injectable


@injectable(namespace="fallback")
class FallbackService(SimpleService):
    @property
    def _name(self):
        return "Fallback Service"
