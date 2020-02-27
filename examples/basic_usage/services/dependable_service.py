from examples.basic_usage.services.simple_service import SimpleService
from injectable import injectable, autowired, Autowired


@injectable
class DependableService:
    @autowired
    def __init__(self, simple_service: Autowired(SimpleService)):
        self.simple_service = simple_service

    def add_two(self):
        self.simple_service.counter += 2
