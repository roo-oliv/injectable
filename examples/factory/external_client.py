class ExternalClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def connect(self):
        return f"ExternalClient connected to {self.endpoint}"
