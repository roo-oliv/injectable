from injectable import injectable


@injectable(qualifier="counter")
class EvenCounterService:
    def __init__(self):
        self.counter = 0

    def add(self):
        self.counter += 2
