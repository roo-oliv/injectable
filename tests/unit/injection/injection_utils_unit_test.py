from unittest.mock import MagicMock

import pytest
from pytest import fixture
from pytest_mock import MockFixture

from injectable import InjectionContainer, Injectable
from injectable.container.namespace import Namespace
from injectable.errors import InjectionError
from injectable.injection.injection_utils import (
    get_namespace_injectables,
    RegistryType,
    filter_by_group,
    resolve_single_injectable,
)


@fixture
def injection_container_mock(mocker: MockFixture):
    return mocker.patch("injectable.injection.injection_utils.InjectionContainer")


class TestGetNamespaceInjectables:
    @pytest.mark.parametrize(
        "registry_type", (RegistryType.CLASS, RegistryType.QUALIFIER)
    )
    def test__get_namespace_injectables(
        self, registry_type: RegistryType, injection_container_mock: InjectionContainer
    ):
        # given
        dependency_name = "TEST"
        namespace_key = "TEST_NAMESPACE"
        namespace = MagicMock(spec=Namespace)()
        injection_container_mock.NAMESPACES = {namespace_key: namespace}

        # when
        injectables = get_namespace_injectables(
            dependency_name, registry_type, namespace_key
        )

        # then
        assert namespace.class_registry.get.called == (
            registry_type is RegistryType.CLASS
        )
        assert namespace.qualifier_registry.get.called == (
            registry_type is RegistryType.QUALIFIER
        )
        registry = (
            namespace.class_registry
            if registry_type is RegistryType.CLASS
            else namespace.qualifier_registry
        )
        assert registry.get.call_args[0][0] is dependency_name
        assert injectables == registry.get.return_value


class TestFilterByGroup:
    def test__filter_by_group__when_exclude_groups_is_none_and_container_groups_is_none(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = None
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables}, group="A", exclude_groups=None)

        # then
        assert len(matches) == 2
        assert all(match in injectables[:2] for match in matches)

    def test__filter_by_group__when_group_is_none_and_container_groups_is_none(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = None
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables}, exclude_groups=["B"])

        # then
        assert len(matches) == 2
        assert all(match in injectables[:2] for match in matches)

    def test__filter_by_group__when_group_and_exclude_groups_are_set_and_container_groups_is_none(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = None
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables}, group="A", exclude_groups=["A"])

        # then
        assert len(matches) == 0

    def test__filter_by_group__when_exclude_groups_is_none_and_container_groups_is_set(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = ["A"]
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables}, group="A")

        # then
        assert len(matches) == 2
        assert all(match in injectables[:2] for match in matches)

    def test__filter_by_group__when_group_is_none_and_container_groups_is_set(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = ["A"]
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables})

        # then
        assert len(matches) == 2

    def test__filter_by_group__when_group_conflicts_with_container_groups(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = ["B"]
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables}, group="A")

        # then
        assert len(matches) == 0

    def test__filter_by_group__when_group_is_none_and_exclude_groups_and_container_groups_are_set(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = ["A"]
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables}, exclude_groups=["B"])

        # then
        assert len(matches) == 2
        assert all(match in injectables[:2] for match in matches)

    def test__filter_by_group__when_group_and_exclude_groups_and_container_groups_are_all_set(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = ["B"]
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables}, group="A", exclude_groups=["A"])

        # then
        assert len(matches) == 0

    def test__filter_by_group__when_all_parameters_are_none(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = None
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables})

        # then
        assert len(matches) == 3
        assert all(match in injectables for match in matches)

    def test__filter_by_group__when_container_groups_allows_all_injectables(
        self, injection_container_mock: InjectionContainer
    ):
        # given
        injection_container_mock.GROUPS = ["A", "B"]
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables})

        # then
        assert len(matches) == 3
        assert all(match in injectables for match in matches)

    def test__filter_by_group__when_exclude_groups_excludes_all_injectables(self):
        # given
        injectables = [MagicMock(group="A"), MagicMock(group="A"), MagicMock(group="B")]

        # when
        matches = filter_by_group({*injectables}, exclude_groups=["A", "B"])

        # then
        assert len(matches) == 0


class TestResolveSingleInjectable:
    def test__resolve_single_injectable__obvious_case(self):
        # given
        expected_injectable = MagicMock(spec=Injectable)()
        matches = {expected_injectable}

        # when
        injectable = resolve_single_injectable("TEST", RegistryType.CLASS, matches)

        # then
        assert injectable == expected_injectable

    def test__resolve_single_injectable__when_there_are_no_primary_injectables(self):
        # given
        matches = {MagicMock(primary=False), MagicMock(primary=False)}

        # then when
        with pytest.raises(InjectionError):
            resolve_single_injectable("TEST", RegistryType.CLASS, matches)

    def test__resolve_single_injectable__when_there_are_multiple_primary_injectables(
        self,
    ):
        # given
        matches = {MagicMock(primary=True), MagicMock(primary=True)}

        # then when
        with pytest.raises(InjectionError):
            resolve_single_injectable("TEST", RegistryType.CLASS, matches)

    def test__resolve_single_injectable__when_there_are_one_primary_injectables(self):
        # given
        primary_injectable = MagicMock(primary=True)
        non_primary_injectable = MagicMock(primary=False)
        matches = {primary_injectable, non_primary_injectable}

        # when
        injectable = resolve_single_injectable("TEST", RegistryType.CLASS, matches)

        # then
        assert injectable is primary_injectable
