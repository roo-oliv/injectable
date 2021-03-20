from unittest.mock import MagicMock, call

import pytest

from injectable import InjectionContainer, Injectable
from injectable.constants import DEFAULT_NAMESPACE
from injectable.container.namespace import Namespace
from injectable.testing import register_injectables


class TestRegisterInjectables:
    def test__register_injectables__with_no_class_or_qualifier(self):
        with pytest.raises(ValueError):
            register_injectables([MagicMock(spec=Injectable)()])

    def test__register_injectables__with_no_class_and_propagate(self):
        with pytest.raises(ValueError):
            register_injectables(
                [MagicMock(spec=Injectable)()], qualifier="TEST", propagate=True
            )

    def test__register_injectables__with_class_and_default_values(self):
        # given
        default_namespace_key = DEFAULT_NAMESPACE
        namespace = MagicMock(spec=Namespace)()
        InjectionContainer.NAMESPACES[default_namespace_key] = namespace
        injectables = [MagicMock(spec=Injectable)(), MagicMock(spec=Injectable)()]
        klass = MagicMock

        # when
        register_injectables(injectables, klass)

        # then
        assert all(
            call.register_injectable(inj, klass, None, False) in namespace.mock_calls
            for inj in injectables
        )

    def test__register_injectables__with_qualifier_and_default_values(self):
        # given
        default_namespace_key = DEFAULT_NAMESPACE
        namespace = MagicMock(spec=Namespace)()
        InjectionContainer.NAMESPACES[default_namespace_key] = namespace
        injectables = [MagicMock(spec=Injectable)(), MagicMock(spec=Injectable)()]
        qualifier = "TEST"

        # when
        register_injectables(injectables, qualifier=qualifier)

        # then
        assert all(
            call.register_injectable(inj, None, qualifier, False)
            in namespace.mock_calls
            for inj in injectables
        )

    def test__register_injectables__with_explicit_values(self):
        # given
        namespace_key = "TEST_NAMESPACE"
        namespace = MagicMock(spec=Namespace)()
        InjectionContainer.NAMESPACES[namespace_key] = namespace
        injectables = [MagicMock(spec=Injectable)(), MagicMock(spec=Injectable)()]
        klass = MagicMock
        qualifier = "TEST"

        # when
        register_injectables(
            injectables, klass, qualifier, namespace_key, propagate=True
        )

        # then
        assert all(
            call.register_injectable(inj, klass, qualifier, True)
            in namespace.mock_calls
            for inj in injectables
        )

    def test__register_injectables__with_empty_injection_container(self):
        # given
        InjectionContainer.NAMESPACES = {}
        namespace = MagicMock(spec=Namespace)()
        InjectionContainer._get_namespace_entry = MagicMock(return_value=namespace)
        injectables = [MagicMock(spec=Injectable)(), MagicMock(spec=Injectable)()]
        klass = MagicMock
        qualifier = "TEST"

        # when
        register_injectables(injectables, klass, qualifier)

        # then
        assert all(
            call.register_injectable(inj, klass, qualifier, False)
            in namespace.mock_calls
            for inj in injectables
        )
