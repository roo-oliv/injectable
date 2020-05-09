import os
from typing import Optional
from unittest.mock import MagicMock

import pytest
from pytest import fixture
from pytest_mock import MockFixture

from injectable import injectable_factory
from injectable.errors.injectable_load_error import InjectableLoadError


@fixture
def get_caller_filepath_mock(mocker: MockFixture):
    return mocker.patch(
        "injectable.injection.injectable_factory_decorator.get_caller_filepath"
    )


@fixture
def injection_container_mock(mocker: MockFixture):
    return mocker.patch(
        "injectable.injection.injectable_factory_decorator.InjectionContainer"
    )


class TestInjectableFactoryDecorator:
    def test__injectable_factory__preserves_original_function(
        self, get_caller_filepath_mock
    ):
        # given
        factory = MagicMock

        # when
        decorated_function = injectable_factory(qualifier="any")(factory)

        # then
        assert decorated_function is factory

    def test__injectable_factory__when_neither_dependency_or_qualifier_are_present(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        factory = MagicMock

        # when
        with pytest.raises(InjectableLoadError):
            injectable_factory()(factory)

        # then
        assert get_caller_filepath_mock.get_caller_filepath.called is False
        assert injection_container_mock._register_factory.called is False

    def test__injectable_factory__when_caller_filepath_does_not_match_loading_filepath(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        caller_filepath = os.path.join(root, "fake", "path", "caller_file.py")
        loading_filepath = os.path.join(root, "fake", "path", "loading_file.py")
        get_caller_filepath_mock.return_value = caller_filepath
        injection_container_mock.LOADING_FILEPATH = loading_filepath
        factory = MagicMock

        # when
        injectable_factory(qualifier="any")(factory)

        # then
        assert get_caller_filepath_mock.get_caller_filepath.called is False
        assert injection_container_mock._register_factory.called is False

    @pytest.mark.parametrize(
        "qualifier, dependency", [("TEST_QUALIFIER", None), (None, MagicMock)]
    )
    def test__injectable_factory__when_caller_filepath_matches_loading_filepath(
        self,
        qualifier: Optional[str],
        dependency: Optional[type],
        get_caller_filepath_mock,
        injection_container_mock,
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        caller_filepath = os.path.join(root, "fake", "path", "caller_file.py")
        get_caller_filepath_mock.return_value = caller_filepath
        injection_container_mock.LOADING_FILEPATH = caller_filepath
        factory = MagicMock

        # when
        injectable_factory(dependency, qualifier=qualifier)(factory)

        # then
        assert injection_container_mock._register_factory.called is True
        (
            factory_arg,
            caller_filepath_arg,
            dependency_arg,
            qualifier_arg,
            primary_arg,
            namespace_arg,
            group_arg,
            singleton_arg,
        ) = injection_container_mock._register_factory.call_args[0]
        assert factory_arg is factory
        assert caller_filepath_arg is caller_filepath
        assert qualifier_arg is qualifier
        assert dependency_arg is dependency
        assert primary_arg is False
        assert namespace_arg is None
        assert group_arg is None
        assert singleton_arg is False

    def test__injectable_factory__with_explicit_args(
        self, get_caller_filepath_mock, injection_container_mock
    ):
        # given
        root = "/" if os.name != "nt" else "C:\\"
        caller_filepath = os.path.join(root, "fake", "path", "caller_file.py")
        get_caller_filepath_mock.return_value = caller_filepath
        injection_container_mock.LOADING_FILEPATH = caller_filepath
        factory = MagicMock
        qualifier = "TEST_QUALIFIER"
        dependency = MagicMock
        namespace = "TEST_NAMESPACE"
        group = "TEST_GROUP"

        # when
        injectable_factory(
            dependency,
            qualifier=qualifier,
            primary=True,
            namespace=namespace,
            group=group,
            singleton=True,
        )(factory)

        # then
        assert injection_container_mock._register_factory.called is True
        (
            factory_arg,
            caller_filepath_arg,
            dependency_arg,
            qualifier_arg,
            primary_arg,
            namespace_arg,
            group_arg,
            singleton_arg,
        ) = injection_container_mock._register_factory.call_args[0]
        assert factory_arg is factory
        assert caller_filepath_arg is caller_filepath
        assert qualifier_arg is qualifier
        assert dependency_arg is dependency
        assert primary_arg is True
        assert namespace_arg is namespace
        assert group_arg is group
        assert singleton_arg is True
