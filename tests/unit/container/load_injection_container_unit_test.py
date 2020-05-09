import os

from pytest import fixture
from pytest_mock import MockFixture

from injectable import load_injection_container
from injectable.constants import DEFAULT_NAMESPACE


@fixture
def get_caller_filepath_mock(mocker: MockFixture):
    return mocker.patch(
        "injectable.container.load_injection_container.get_caller_filepath",
    )


@fixture
def injection_container_mock(mocker: MockFixture):
    return mocker.patch(
        "injectable.container.load_injection_container.InjectionContainer"
    )


class TestLoadInjectionContainer:
    def test__load_injection_container__with_defaults(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        filedir = os.path.join("fake", "path")
        filepath = os.path.join(filedir, "file.py")
        get_caller_filepath_mock.return_value = filepath

        # when
        load_injection_container()

        # then
        assert get_caller_filepath_mock.called is True
        load = injection_container_mock.load_dependencies_from
        assert load.called is True
        search_path_arg, default_namespace_arg = load.call_args[0][:2]
        assert search_path_arg == filedir
        assert default_namespace_arg == DEFAULT_NAMESPACE

    def test__load_injection_container__with_absolute_search_path(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        search_path = os.path.join(root, "fake", "path")

        # when
        load_injection_container(search_path)

        # then
        assert get_caller_filepath_mock.called is False
        load = injection_container_mock.load_dependencies_from
        assert load.called is True
        search_path_arg = load.call_args[0][0]
        assert search_path_arg == search_path

    def test__load_injection_container__with_relative_search_path(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        filepath = os.path.join(root, "fake", "path", "file.py")
        get_caller_filepath_mock.return_value = filepath
        search_path = os.path.join("..", "relative", "path")
        expected_path = os.path.join(root, "fake", "relative", "path")

        # when
        load_injection_container(search_path)

        # then
        assert get_caller_filepath_mock.called is True
        load = injection_container_mock.load_dependencies_from
        assert load.called is True
        search_path_arg = load.call_args[0][0]
        assert search_path_arg == expected_path

    def test__load_injection_container__with_explicit_namespace(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        get_caller_filepath_mock.return_value = os.path.join("fake", "path", "file.py")
        default_namespace = "TEST_NAMESPACE"

        # when
        load_injection_container(default_namespace=default_namespace)

        # then
        load = injection_container_mock.load_dependencies_from
        assert load.called is True
        default_namespace_arg = load.call_args[0][1]
        assert default_namespace_arg == default_namespace
