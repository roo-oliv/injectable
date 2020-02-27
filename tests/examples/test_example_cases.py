from examples import Example
from injectable import InjectionContainer, inject_multiple


def pytest_generate_tests(metafunc):
    if "example" in metafunc.fixturenames:
        InjectionContainer.load("../../examples")
        examples = inject_multiple(Example)
        ids = [example.__class__.__qualname__ for example in examples]
        metafunc.parametrize("example", examples, ids=ids)


def test_example_case(example: Example):
    example.run()
