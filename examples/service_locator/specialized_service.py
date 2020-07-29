from examples.service_locator.sample_service import SampleService
from injectable import injectable


@injectable
class SpecializedService(SampleService):
    pass
