from injectable import injectable


@injectable
class ServiceB:
    def __init__(self):
        print("ServiceB::__init__ called")

    def something(self):
        print("ServiceB::something called")
