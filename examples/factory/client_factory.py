import os

from examples.factory.external_client import ExternalClient
from injectable.injection.injectable_factory_decorator import injectable_factory


@injectable_factory(ExternalClient)
def client_factory():
    client_endpoint = os.getenv(
        "CLIENT_ENDPOINT_EXAMPLE_ENV_VAR", "https://dummy/endpoint"
    )
    return ExternalClient(client_endpoint)
