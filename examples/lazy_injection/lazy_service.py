from injectable import injectable


@injectable
class LazyService:
    def __init__(self):
        print("LazyService::__init__ called")

    def something(self):
        print("LazyService::something called")
