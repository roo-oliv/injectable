from injectable import injectable


@injectable
class SimpleService:
    def __init__(self):
        self.counter = 0

    def add_one(self):
        self.counter += 1
