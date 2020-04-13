from injectable import injectable


@injectable
class ConfigurationService:
    def __init__(self):
        self.client_endpoint = "https://client.endpoint/"
        self.client_type = 1
