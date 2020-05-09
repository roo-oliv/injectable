"""
This is an illustrative example of basic usage of the injectable framework in a single
Python file.
"""
# sphinx-start
from examples import Example
from injectable import injectable, autowired, Autowired, load_injection_container


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
    load_injection_container()
    example = IllustrativeExample()
    example.run()
