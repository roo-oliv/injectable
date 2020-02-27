from injectable import injectable


@injectable(singleton=True)
class SimpleSingleton:
    def __init__(self):
        self.counter = 0
