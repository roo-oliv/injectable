from injectable import injectable
from injectable.util import lazy


class Model:
    def __init__(self, something: str = "42"):
        self.something = something

    def get_something(self):
        return self.something


class Service:
    @injectable()
    def __init__(self, *, model: Model):
        self.model = model


def test_injectable_init():
    service = Service()

    assert service.model.get_something() is "42"


def test_manual_injection():
    model71 = Model(something="71")
    service = Service(model=model71)

    assert service.model.get_something() is "71"


class CircularDependant1:
    @injectable()
    def __init__(self, *, dep: lazy('CircularDependant2')):
        self.dep = dep
        self.color = "yellow"

    def speak(self) -> str:
        return self.color

    def what_dep_says(self) -> str:
        return self.dep.speak()


class CircularDependant2:
    @injectable()
    def __init__(self, *, dep: lazy(CircularDependant1)):
        self.dep = dep
        self.color = "blue"

    def speak(self) -> str:
        return self.color

    def what_dep_says(self) -> str:
        return self.dep.speak()


def test_circular_dependency():
    yellow = CircularDependant1()
    blue = CircularDependant2()

    assert yellow.what_dep_says() is "blue"
    assert blue.what_dep_says() is "yellow"
    assert blue.dep.dep.dep.what_dep_says() is "blue"


class Umbrella:
    @injectable(lazy=True)
    def __init__(self, *, dep1: CircularDependant1, dep2: CircularDependant2):
        self.dep1 = dep1
        self.dep2 = dep2


def test_mutually_dependant_dependencies():
    umbrella = Umbrella()

    assert umbrella.dep1.what_dep_says() is "blue"
    assert umbrella.dep2.what_dep_says() is "yellow"
