from examples.factory.client_one import ClientOne
from examples.factory.client_two import ClientTwo
from examples.factory.configuration_service import ConfigurationService
from injectable import Autowired, autowired
from injectable.injection.injectable_factory_decorator import injectable_factory


@injectable_factory(qualifier="client")
@autowired
def client_factory(configuration_service: Autowired(ConfigurationService)):
    if configuration_service.client_type == 1:
        return ClientOne(configuration_service.client_endpoint)
    elif configuration_service.client_type == 2:
        return ClientTwo(configuration_service.client_endpoint)
    raise RuntimeError(f"Unknown client_type: {configuration_service.client_type}")
