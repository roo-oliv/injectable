from injectable import injectable
from tests.fixes.issue_30.test_module.utils import some_util


@injectable(qualifier="foo")
class Foo:
    def __init__(self):
        some_util.some_util()
