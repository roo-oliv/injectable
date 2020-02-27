from injectable import injectable


@injectable(qualifier="counter", namespace="odd")
class OddCounterService:
    def __init__(self):
        self.counter = 1

    def add(self):
        self.counter += 2
