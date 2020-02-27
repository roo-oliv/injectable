from injectable import injectable, autowired, Autowired


@injectable(qualifier="B")
class ServiceB:
    @autowired
    def __init__(self, service_a: Autowired("A")):
        self.service_a = service_a
        self.message = "ServiceB.message"

    @property
    def message_a(self):
        return self.service_a.message
