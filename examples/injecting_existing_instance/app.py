from injectable import injectable_factory


class Application:
    def __init__(self, number):
        self.number = number


app = Application(42)
...

injectable_factory(Application)(lambda: app)
