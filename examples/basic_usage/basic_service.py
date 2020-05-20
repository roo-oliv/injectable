from examples.basic_usage.stateful_repository import StatefulRepository
from injectable import injectable, autowired, Autowired


@injectable
class BasicService:
    @autowired
    def __init__(self, repository: Autowired(StatefulRepository)):
        self.repository = repository

    def set_repository_state(self, state):
        self.repository.state = state

    def get_repository_state(self):
        return self.repository.state
