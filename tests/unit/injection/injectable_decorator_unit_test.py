import os
from unittest.mock import MagicMock

from pytest import fixture
from pytest_mock import MockFixture

from injectable import injectable


@fixture
def get_caller_filepath_mock(mocker: MockFixture):
    return mocker.patch("injectable.injection.injectable_decorator.get_caller_filepath")


@fixture
def injection_container_mock(mocker: MockFixture):
    return mocker.patch("injectable.injection.injectable_decorator.InjectionContainer")


class TestInjectableDecorator:
    def test__injectable__preserves_original_class(self, get_caller_filepath_mock):
        # given
        klass = MagicMock

        # when
        decorated_class = injectable(klass)

        # then
        assert decorated_class is klass

    def test__injectable__direct_call(self, get_caller_filepath_mock):
        # given
        klass = MagicMock

        # when
        injectable(klass)

        # then
        assert get_caller_filepath_mock.called is True
        assert get_caller_filepath_mock.call_args[0][0] == 3

    def test__injectable__indirect_call(self, get_caller_filepath_mock):
        # given
        klass = MagicMock

        # when
        injectable()(klass)

        # then
        assert get_caller_filepath_mock.called is True
        assert get_caller_filepath_mock.call_args[0][0] == 2

    def test__injectable__when_caller_filepath_does_not_match_loading_filepath(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        caller_filepath = os.path.join(root, "fake", "path", "caller_file.py")
        loading_filepath = os.path.join(root, "fake", "path", "loading_file.py")
        get_caller_filepath_mock.return_value = caller_filepath
        injection_container_mock.LOADING_FILEPATH = loading_filepath
        klass = MagicMock

        # when
        injectable(klass)

        # then
        assert injection_container_mock._register_injectable.called is False

    def test__injectable__when_caller_filepath_matches_loading_filepath(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        caller_filepath = os.path.join(root, "fake", "path", "caller_file.py")
        get_caller_filepath_mock.return_value = caller_filepath
        injection_container_mock.LOADING_FILEPATH = caller_filepath
        klass = MagicMock

        # when
        injectable(klass)

        # then
        assert injection_container_mock._register_injectable.called is True
        (
            klass_arg,
            caller_filepath_arg,
            qualifier_arg,
            primary_arg,
            namespace_arg,
            group_arg,
            singleton_arg,
        ) = injection_container_mock._register_injectable.call_args[0]
        assert klass_arg is klass
        assert caller_filepath_arg is caller_filepath
        assert qualifier_arg is None
        assert primary_arg is False
        assert namespace_arg is None
        assert group_arg is None
        assert singleton_arg is False

    def test__injectable__with_explicit_args(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        caller_filepath = os.path.join(root, "fake", "path", "caller_file.py")
        get_caller_filepath_mock.return_value = caller_filepath
        injection_container_mock.LOADING_FILEPATH = caller_filepath
        klass = MagicMock
        qualifier = "TEST_QUALIFIER"
        namespace = "TEST_NAMESPACE"
        group = "TEST_GROUP"

        # when
        injectable(
            qualifier=qualifier,
            primary=True,
            namespace=namespace,
            group=group,
            singleton=True,
        )(klass)

        # then
        assert injection_container_mock._register_injectable.called is True
        (
            klass_arg,
            caller_filepath_arg,
            qualifier_arg,
            primary_arg,
            namespace_arg,
            group_arg,
            singleton_arg,
        ) = injection_container_mock._register_injectable.call_args[0]
        assert klass_arg is klass
        assert caller_filepath_arg is caller_filepath
        assert qualifier_arg is qualifier
        assert primary_arg is True
        assert namespace_arg is namespace
        assert group_arg is group
        assert singleton_arg is True
