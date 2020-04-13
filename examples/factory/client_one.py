class ClientOne:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def connect(self):
        return f"ClientOne connected to {self.endpoint}"
