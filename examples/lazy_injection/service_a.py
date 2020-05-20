from injectable import injectable


@injectable
class ServiceA:
    def __init__(self):
        print("ServiceA::__init__ called")

    def something(self):
        print("ServiceA::something called")
