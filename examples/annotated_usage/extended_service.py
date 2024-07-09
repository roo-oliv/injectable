from examples.annotated_usage.simple_service import SimpleService
from injectable import injectable


@injectable
class ExtendedService(SimpleService):
    @property
    def _name(self):
        return "Extended Service"
