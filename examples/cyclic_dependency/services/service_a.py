from injectable import injectable, Autowired, autowired


@injectable(qualifier="A")
class ServiceA:
    @autowired
    def __init__(self, service_b: Autowired("B", lazy=True)):
        self.service_b = service_b
        self.message = "ServiceA.message"

    @property
    def message_b(self):
        return self.service_b.message
