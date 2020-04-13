class ClientTwo:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def connect(self):
        return f"ClientTwo connected to {self.endpoint}"
