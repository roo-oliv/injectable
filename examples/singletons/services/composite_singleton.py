from examples.singletons.services.simple_singleton import SimpleSingleton
from injectable import injectable, autowired, Autowired


@injectable(singleton=True)
class CompositeSingleton:
    @autowired
    def __init__(self, simple_singleton: Autowired(SimpleSingleton)):
        self.simple_singleton = simple_singleton

    @property
    def counter(self):
        return self.simple_singleton.counter

    @counter.setter
    def counter(self, value):
        self.simple_singleton.counter = value
