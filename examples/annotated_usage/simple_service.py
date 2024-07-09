from injectable import injectable


@injectable(primary=True)
class SimpleService:
    def __init__(self):
        self._statement = "says: Hello!"

    @property
    def _name(self):
        return "Simple Service"

    def speak(self):
        print(f"{self._name} {self._statement}")
