from unittest.mock import MagicMock

import pytest
from pytest import fixture
from pytest_mock import MockFixture

from injectable import inject, Injectable, inject_multiple
from injectable.errors import InjectionError
from injectable.constants import DEFAULT_NAMESPACE
from injectable.injection.injection_utils import RegistryType


@fixture
def get_dependency_name_mock(mocker: MockFixture):
    return mocker.patch("injectable.injection.inject.get_dependency_name")


@fixture
def get_dependency_registry_type_mock(mocker: MockFixture):
    return mocker.patch("injectable.injection.inject.get_dependency_registry_type")


@fixture
def get_namespace_injectables_mock(mocker: MockFixture):
    return mocker.patch("injectable.injection.inject.get_namespace_injectables")


@fixture
def filter_by_group_mock(mocker: MockFixture):
    return mocker.patch("injectable.injection.inject.filter_by_group")


@fixture
def resolve_single_injectable_mock(mocker: MockFixture):
    return mocker.patch("injectable.injection.inject.resolve_single_injectable")


class TestInject:
    def test__inject__with_default_values(
        self,
        get_dependency_name_mock,
        get_dependency_registry_type_mock,
        get_namespace_injectables_mock,
        filter_by_group_mock,
        resolve_single_injectable_mock,
    ):
        # given
        expected_instance = MagicMock
        injectable = MagicMock(spec=Injectable)
        injectable.get_instance.return_value = expected_instance
        matches = {injectable}
        dependency_name = "TEST"
        get_dependency_name_mock.return_value = dependency_name
        registry_type = RegistryType.CLASS
        get_dependency_registry_type_mock.return_value = registry_type
        get_namespace_injectables_mock.return_value = matches
        resolve_single_injectable_mock.return_value = injectable
        dependency = "TEST"

        # when
        instance = inject(dependency)

        # then
        assert get_namespace_injectables_mock.called is True
        (
            dependency_name_arg,
            registry_type_arg,
            namespace_arg,
        ) = get_namespace_injectables_mock.call_args[0]
        assert dependency_name_arg is dependency_name
        assert registry_type_arg is registry_type
        assert namespace_arg is DEFAULT_NAMESPACE
        assert filter_by_group_mock.called is False
        assert resolve_single_injectable_mock.called is True
        (
            dependency_name_arg,
            registry_type_arg,
            matches_arg,
        ) = resolve_single_injectable_mock.call_args[0]
        assert dependency_name_arg == dependency_name
        assert registry_type_arg == registry_type
        assert matches_arg == matches
        assert injectable.get_instance.called is True
        assert injectable.get_instance.call_args[1]["lazy"] is False
        assert instance == expected_instance

    def test__inject__with_no_matches_for_dependency_when_non_optional(
        self,
        get_dependency_name_mock,
        get_dependency_registry_type_mock,
        get_namespace_injectables_mock,
        filter_by_group_mock,
        resolve_single_injectable_mock,
    ):
        # given
        matches = {}
        dependency_name = "TEST"
        get_dependency_name_mock.return_value = dependency_name
        registry_type = RegistryType.CLASS
        get_dependency_registry_type_mock.return_value = registry_type
        get_namespace_injectables_mock.return_value = matches
        dependency = "TEST"

        # when
        with pytest.raises(InjectionError):
            inject(dependency)

        # then
        assert get_namespace_injectables_mock.called is True
        assert filter_by_group_mock.called is False
        assert resolve_single_injectable_mock.called is False

    def test__inject__with_no_matches_for_dependency_when_optional(
        self,
        get_dependency_name_mock,
        get_dependency_registry_type_mock,
        get_namespace_injectables_mock,
        filter_by_group_mock,
        resolve_single_injectable_mock,
    ):
        # given
        matches = {}
        dependency_name = "TEST"
        get_dependency_name_mock.return_value = dependency_name
        registry_type = RegistryType.CLASS
        get_dependency_registry_type_mock.return_value = registry_type
        get_namespace_injectables_mock.return_value = matches
        dependency = "TEST"

        # when
        instance = inject(dependency, optional=True)

        # then
        assert get_namespace_injectables_mock.called is True
        assert filter_by_group_mock.called is False
        assert resolve_single_injectable_mock.called is False
        assert instance is None

    def test__inject__with_no_matches_for_group_when_non_optional(
        self,
        get_namespace_injectables_mock,
        filter_by_group_mock,
        resolve_single_injectable_mock,
    ):
        # given
        matches = {MagicMock(spec=Injectable)}
        lookup_key = "TEST"
        lookup_type = "class"
        get_namespace_injectables_mock.return_value = [matches, lookup_key, lookup_type]
        filter_by_group_mock.return_value = {}
        dependency = "TEST"

        # when
        with pytest.raises(InjectionError):
            inject(dependency, group="TEST_GROUP")

        # then
        assert get_namespace_injectables_mock.called is True
        assert filter_by_group_mock.called is True
        assert resolve_single_injectable_mock.called is False

    def test__inject__with_no_matches_for_group_when_optional(
        self,
        get_namespace_injectables_mock,
        filter_by_group_mock,
        resolve_single_injectable_mock,
    ):
        # given
        matches = {MagicMock(spec=Injectable)}
        lookup_key = "TEST"
        lookup_type = "class"
        get_namespace_injectables_mock.return_value = [matches, lookup_key, lookup_type]
        filter_by_group_mock.return_value = {}
        dependency = "TEST"

        # when
        instance = inject(dependency, group="TEST_GROUP", optional=True)

        # then
        assert get_namespace_injectables_mock.called is True
        assert filter_by_group_mock.called is True
        assert resolve_single_injectable_mock.called is False
        assert instance is None

    def test__inject__with_explicit_values(
        self,
        get_dependency_name_mock,
        get_dependency_registry_type_mock,
        get_namespace_injectables_mock,
        filter_by_group_mock,
        resolve_single_injectable_mock,
    ):
        # given
        expected_instance = MagicMock
        primary_injectable = MagicMock(spec=Injectable)
        primary_injectable.get_instance.return_value = expected_instance
        non_primary_injectable = MagicMock(spec=Injectable)
        matches = {
            primary_injectable,
            non_primary_injectable,
            MagicMock(spec=Injectable),
        }
        dependency_name = "TEST"
        get_dependency_name_mock.return_value = dependency_name
        registry_type = RegistryType.CLASS
        get_dependency_registry_type_mock.return_value = registry_type
        get_namespace_injectables_mock.return_value = matches
        filtered_matches = {primary_injectable, non_primary_injectable}
        filter_by_group_mock.return_value = filtered_matches
        resolve_single_injectable_mock.return_value = primary_injectable
        dependency = "TEST"
        namespace = "TEST_NAMESPACE"
        group = "TEST_GROUP"
        exclude_groups = ["A", "B"]

        # when
        instance = inject(
            dependency,
            namespace=namespace,
            group=group,
            exclude_groups=exclude_groups,
            lazy=True,
            optional=False,
        )

        # then
        assert get_namespace_injectables_mock.called is True
        (
            dependency_name_arg,
            registry_type_arg,
            namespace_arg,
        ) = get_namespace_injectables_mock.call_args[0]
        assert dependency_name_arg is dependency_name
        assert registry_type_arg is registry_type
        assert namespace_arg is namespace
        assert filter_by_group_mock.called is True
        matches_arg, group_arg, exclude_groups_arg = filter_by_group_mock.call_args[0]
        assert matches_arg == matches
        assert group_arg == group
        assert exclude_groups_arg == exclude_groups
        assert resolve_single_injectable_mock.called is True
        (
            dependency_name_arg,
            registry_type_arg,
            matches_arg,
        ) = resolve_single_injectable_mock.call_args[0]
        assert dependency_name_arg == dependency_name
        assert registry_type_arg == registry_type
        assert matches_arg == filtered_matches
        assert primary_injectable.get_instance.called is True
        assert non_primary_injectable.get_instance.called is False
        assert primary_injectable.get_instance.call_args[1]["lazy"] is True
        assert instance == expected_instance


class TestInjectMultiple:
    def test__inject_multiple__with_default_values(
        self,
        get_dependency_name_mock,
        get_dependency_registry_type_mock,
        get_namespace_injectables_mock,
        filter_by_group_mock,
    ):
        # given
        expected_instances = [MagicMock(), MagicMock()]
        injectables = [MagicMock(spec=Injectable), MagicMock(spec=Injectable)]
        for i in range(len(expected_instances)):
            injectables[i].get_instance.return_value = expected_instances[i]
        matches = {*injectables}
        dependency_name = "TEST"
        get_dependency_name_mock.return_value = dependency_name
        registry_type = RegistryType.CLASS
        get_dependency_registry_type_mock.return_value = registry_type
        get_namespace_injectables_mock.return_value = matches
        dependency = "TEST"

        # when
        instances = inject_multiple(dependency)

        # then
        assert get_namespace_injectables_mock.called is True
        (
            dependency_name_arg,
            registry_type_arg,
            namespace_arg,
        ) = get_namespace_injectables_mock.call_args[0]
        assert dependency_name_arg is dependency
        assert registry_type_arg is registry_type
        assert namespace_arg is DEFAULT_NAMESPACE
        assert filter_by_group_mock.called is False
        assert all(injectable.get_instance.called is True for injectable in injectables)
        assert all(
            injectable.get_instance.call_args[1]["lazy"] is False
            for injectable in injectables
        )
        assert len(instances) == len(expected_instances)
        assert all(instance in expected_instances for instance in instances)

    def test__inject_multiple__with_no_matches_for_dependency_when_non_optional(
        self,
        get_dependency_name_mock,
        get_dependency_registry_type_mock,
        get_namespace_injectables_mock,
        filter_by_group_mock,
    ):
        # given
        matches = {}
        dependency_name = "TEST"
        get_dependency_name_mock.return_value = dependency_name
        registry_type = RegistryType.CLASS
        get_dependency_registry_type_mock.return_value = registry_type
        get_namespace_injectables_mock.return_value = matches
        dependency = "TEST"

        # when
        with pytest.raises(InjectionError):
            inject_multiple(dependency)

        # then
        assert get_namespace_injectables_mock.called is True
        assert filter_by_group_mock.called is False

    def test__inject_multiple__with_no_matches_for_dependency_when_optional(
        self,
        get_dependency_name_mock,
        get_dependency_registry_type_mock,
        get_namespace_injectables_mock,
        filter_by_group_mock,
    ):
        # given
        matches = {}
        dependency_name = "TEST"
        get_dependency_name_mock.return_value = dependency_name
        registry_type = RegistryType.CLASS
        get_dependency_registry_type_mock.return_value = registry_type
        get_namespace_injectables_mock.return_value = matches
        dependency = "TEST"

        # when
        instances = inject_multiple(dependency, optional=True)

        # then
        assert get_namespace_injectables_mock.called is True
        assert filter_by_group_mock.called is False
        assert instances == []

    def test__inject_multiple__with_no_matches_for_group_when_non_optional(
        self,
        get_namespace_injectables_mock,
        filter_by_group_mock,
    ):
        # given
        matches = {MagicMock(spec=Injectable), MagicMock(spec=Injectable)}
        lookup_key = "TEST"
        lookup_type = "class"
        get_namespace_injectables_mock.return_value = [matches, lookup_key, lookup_type]
        filter_by_group_mock.return_value = {}
        dependency = "TEST"

        # when
        with pytest.raises(InjectionError):
            inject_multiple(dependency, group="TEST_GROUP")

        # then
        assert get_namespace_injectables_mock.called is True
        assert filter_by_group_mock.called is True

    def test__inject_multiple__with_no_matches_for_group_when_optional(
        self,
        get_namespace_injectables_mock,
        filter_by_group_mock,
    ):
        # given
        matches = {MagicMock(spec=Injectable), MagicMock(spec=Injectable)}
        lookup_key = "TEST"
        lookup_type = "class"
        get_namespace_injectables_mock.return_value = [matches, lookup_key, lookup_type]
        filter_by_group_mock.return_value = {}
        dependency = "TEST"

        # when
        instances = inject_multiple(dependency, group="TEST_GROUP", optional=True)

        # then
        assert get_namespace_injectables_mock.called is True
        assert filter_by_group_mock.called is True
        assert instances == []

    def test__inject_multiple__with_explicit_values(
        self,
        get_dependency_name_mock,
        get_dependency_registry_type_mock,
        get_namespace_injectables_mock,
        filter_by_group_mock,
    ):
        # given
        expected_instances = [MagicMock(), MagicMock()]
        injectables = [
            MagicMock(spec=Injectable),
            MagicMock(spec=Injectable),
            MagicMock(spec=Injectable),
        ]
        for i in range(len(expected_instances)):
            injectables[i].get_instance.return_value = expected_instances[i]
        matches = {*injectables}
        dependency_name = "TEST"
        get_dependency_name_mock.return_value = dependency_name
        registry_type = RegistryType.CLASS
        get_dependency_registry_type_mock.return_value = registry_type
        get_namespace_injectables_mock.return_value = matches
        filtered_matches = {*injectables[:2]}
        filter_by_group_mock.return_value = filtered_matches
        dependency = "TEST"
        namespace = "TEST_NAMESPACE"
        group = "TEST_GROUP"
        exclude_groups = ["A", "B"]

        # when
        instances = inject_multiple(
            dependency,
            namespace=namespace,
            group=group,
            exclude_groups=exclude_groups,
            lazy=True,
            optional=False,
        )

        # then
        assert get_namespace_injectables_mock.called is True
        (
            dependency_name_arg,
            registry_type_arg,
            namespace_arg,
        ) = get_namespace_injectables_mock.call_args[0]
        assert dependency_name_arg is dependency_name
        assert registry_type_arg is registry_type
        assert namespace_arg is namespace
        assert filter_by_group_mock.called is True
        matches_arg, group_arg, exclude_groups_arg = filter_by_group_mock.call_args[0]
        assert matches_arg == matches
        assert group_arg == group
        assert exclude_groups_arg == exclude_groups
        assert injectables[0].get_instance.called is True
        assert injectables[1].get_instance.called is True
        assert injectables[2].get_instance.called is False
        assert all(
            injectable.get_instance.call_args[1]["lazy"] is True
            for injectable in injectables[:2]
        )
        assert len(instances) == len(expected_instances)
        assert all(instance in expected_instances for instance in instances)
