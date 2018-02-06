from injectable import injectable


class Model:
    def __init__(self, something: str = "42"):
        self.something = something

    def get_something(self):
        return self.something


class Service:
    @injectable()
    def __init__(self, *, model: Model):
        self.model = model


class Yellow:
    @injectable()
    def __init__(self, *, blue: 'Blue'):
        self.blue = blue
        self.color = "yellow"

    def speak(self) -> str:
        return self.color

    def what_blue_says(self) -> str:
        return self.blue.speak()


class Blue:
    @injectable()
    def __init__(self, *, yellow: 'Yellow'):
        self.yellow = yellow
        self.color = "blue"

    def speak(self) -> str:
        return self.color

    def what_yellow_says(self) -> str:
        return self.yellow.speak()


class TestExamples:

    def test_injectable_init(self):
        service = Service()

        assert service.model.get_something() is "42"

    def test_manual_injection(self):
        model71 = Model(something="71")
        service = Service(model=model71)

        assert service.model.get_something() is "71"

    def test_circular_reference(self):
        yellow = Yellow()

        assert yellow.what_blue_says() is "blue"
