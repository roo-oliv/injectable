import os
from importlib import import_module

from pycollect import PythonFileCollector, find_module_name

from injectable.testing import reset_injection_container


def contains_example(file_entry: os.DirEntry) -> bool:
    with open(file_entry) as file:
        source = file.read()
    # TODO: Consider the use of ast.parse for this
    return "def run_example():" in source


def pytest_generate_tests(metafunc):
    if "example_file" in metafunc.fixturenames:
        collector = PythonFileCollector()
        example_files = collector.collect(
            os.path.join(os.path.dirname(__file__), "..", "..", "examples")
        )
        examples = [file for file in example_files if contains_example(file)]
        ids = [example.name for example in examples]
        metafunc.parametrize("example_file", examples, ids=ids)


def test_example_case(example_file: os.DirEntry):
    reset_injection_container()
    module_name = find_module_name(os.path.abspath(example_file.path))
    example = import_module(module_name)
    example.run_example()
