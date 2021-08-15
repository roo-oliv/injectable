from injectable import injectable
from .bar import Bar
from ..utils import some_util


@injectable(qualifier="foo")
class Foo:
    def __init__(self):
        Bar().do_something()
        some_util.some_util()

    def is_ok(self):
        return True
