from examples.service_locator.stateful_repository import StatefulRepository
from injectable import injectable, inject


@injectable(primary=True)
class SampleService:
    def __init__(self):
        self.repository: StatefulRepository = inject(StatefulRepository)

    def set_repository_state(self, state):
        self.repository.state = state

    def get_repository_state(self):
        return self.repository.state
