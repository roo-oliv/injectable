from injectable import injectable


@injectable(singleton=True)
class SingletonClient:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
