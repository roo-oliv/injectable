"""
This is an illustrative example of basic usage of the injectable framework in a single
Python file.
"""
# sphinx-start
from examples import Example
from injectable import injectable, InjectionContainer, autowired, Autowired


@injectable
class Dep:
    def __init__(self):
        self.foo = "foo"


@injectable  # make examples also injectable for testing
class IllustrativeExample(Example):
    @autowired
    def __init__(self, dep: Autowired(Dep)):
        self.dep = dep

    def run(self):
        print(self.dep.foo)
        # foo


if __name__ == "__main__":
    InjectionContainer.load()
    example = IllustrativeExample()
    example.run()
