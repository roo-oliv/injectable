from injectable import injectable, Autowired, autowired


@injectable(qualifier="A")
class ServiceA:
    @autowired
    def __init__(self, service_b: Autowired("B", lazy=True)):
        self.service_b = service_b
        self.some_property = "some property from A"

    @property
    def get_some_property_from_b(self):
        return self.service_b.some_property
