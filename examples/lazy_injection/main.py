"""
In this example you'll see how to declare an injection as lazy.
"""
# sphinx-start
from examples import Example
from examples.lazy_injection.lazy_service import LazyService
from injectable import autowired, Autowired, injectable, load_injection_container


@injectable  # make examples also injectable for testing
class LazyInjection(Example):
    @autowired
    def __init__(
        self, lazy_service: Autowired(LazyService, lazy=True),
    ):
        self.lazy_service = lazy_service
        print("finished injecting")
        # finished injecting

    def run(self):
        print("running")
        # running
        self.lazy_service.something()
        # LazyService::__init__ called
        # LazyService::something called


if __name__ == "__main__":
    load_injection_container()
    example = LazyInjection()
    example.run()
