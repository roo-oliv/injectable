import sys
from unittest.mock import MagicMock, call

from pytest import fixture
from pytest_mock import MockFixture

from injectable import InjectionContainer, Injectable
from injectable.container.namespace import Namespace
from injectable.constants import DEFAULT_NAMESPACE
from injectable.testing import clear_injectables


@fixture(autouse=True)
def fix_getitem_call_chaining():
    """This is a fix for: https://bugs.python.org/issue37972"""
    if sys.version_info[:3] >= (3, 8, 0):
        return

    def __getattribute__(self, attr):
        if attr == "__getitem__":
            raise AttributeError
        return tuple.__getattribute__(self, attr)

    call.__class__.__getattribute__ = __getattribute__  # call.__class__ is _Call


@fixture
def get_dependency_name_mock(mocker: MockFixture):
    return mocker.patch("injectable.testing.clear_injectables_util.get_dependency_name")


class TestClearInjectables:
    def test__clear_injectables__with_class_dependency(self, get_dependency_name_mock):
        # given
        expected_injectables = [MagicMock(spec=Injectable)()]
        namespace_key = "TEST_NAMESPACE"
        namespace = MagicMock(spec=Namespace)()
        namespace.class_registry.__getitem__.return_value = expected_injectables
        InjectionContainer.NAMESPACES[namespace_key] = namespace
        dependency_name = "TEST"
        get_dependency_name_mock.return_value = dependency_name

        # when
        cleared_injectables = clear_injectables(MagicMock, namespace_key)

        # then
        assert call.class_registry.__getitem__(dependency_name) in namespace.mock_calls
        assert (
            call.class_registry.__setitem__(dependency_name, set())
            in namespace.mock_calls
        )
        assert namespace.qualifier_registry.__getitem__.called is False
        assert cleared_injectables is expected_injectables

    def test__clear_injectables__with_qualifier_dependency(self):
        # given
        expected_injectables = [MagicMock(spec=Injectable)()]
        namespace_key = "TEST_NAMESPACE"
        namespace = MagicMock(spec=Namespace)()
        namespace.qualifier_registry.__getitem__.return_value = expected_injectables
        InjectionContainer.NAMESPACES[namespace_key] = namespace
        qualifier = "TEST"

        # when
        cleared_injectables = clear_injectables(qualifier, namespace_key)

        # then
        assert call.qualifier_registry.__getitem__(qualifier) in namespace.mock_calls
        assert (
            call.qualifier_registry.__setitem__(qualifier, set())
            in namespace.mock_calls
        )
        assert namespace.class_registry.__getitem__.called is False
        assert cleared_injectables is expected_injectables

    def test__clear_injectables__with_default_namespace(self):
        # given
        expected_injectables = [MagicMock(spec=Injectable)()]
        default_namespace_key = DEFAULT_NAMESPACE
        namespace = MagicMock(spec=Namespace)()
        namespace.qualifier_registry.__getitem__.return_value = expected_injectables
        InjectionContainer.NAMESPACES[default_namespace_key] = namespace
        qualifier = "TEST"

        # when
        cleared_injectables = clear_injectables(qualifier)

        # then
        assert call.qualifier_registry.__getitem__(qualifier) in namespace.mock_calls
        assert (
            call.qualifier_registry.__setitem__(qualifier, set())
            in namespace.mock_calls
        )
        assert namespace.class_registry.__getitem__.called is False
        assert cleared_injectables is expected_injectables
