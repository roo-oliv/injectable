from injectable import injectable, autowired, Autowired


@injectable(qualifier="B")
class ServiceB:
    @autowired
    def __init__(self, service_a: Autowired("A", lazy=True)):
        self.service_a = service_a
        self.some_property = "some property from B"

    @property
    def get_some_property_from_a(self):
        return self.service_a.some_property
