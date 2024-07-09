from unittest.mock import MagicMock

from injectable import Injectable
from injectable.container.namespace import Namespace


class TestNamespace:
    def test__init__(self):
        # when
        namespace = Namespace()

        # then
        assert namespace.class_registry == {}
        assert namespace.qualifier_registry == {}

    def test__register_injectable__with_class_only(self):
        # given
        injectable = MagicMock(spec=Injectable)
        namespace = Namespace()
        klass = TestNamespace
        class_lookup_key = klass.__qualname__

        # when
        namespace.register_injectable(injectable, klass)

        # then
        assert namespace.class_registry[class_lookup_key] == {injectable}

    def test__register_injectable__with_qualifier_only(self):
        # given
        injectable = MagicMock(spec=Injectable)
        qualifier = "qualifier"
        namespace = Namespace()

        # when
        namespace.register_injectable(injectable, qualifier=qualifier)

        # then
        assert namespace.qualifier_registry[qualifier] == {injectable}

    def test__register_injectable__with_class_and_qualifier(self):
        # given
        injectable = MagicMock(spec=Injectable)
        klass = TestNamespace
        class_lookup_key = klass.__qualname__
        qualifier = "qualifier"
        namespace = Namespace()

        # when
        namespace.register_injectable(injectable, klass, qualifier)

        # then
        assert namespace.class_registry[class_lookup_key] == {injectable}
        assert namespace.qualifier_registry[qualifier] == {injectable}

    def test__register_injectable__propagation_to_base_classes(self):
        # given
        injectable = MagicMock(spec=Injectable)
        base_class = TestNamespace
        base_class_lookup_key = base_class.__qualname__

        class Child(base_class): ...

        child_class = Child
        child_class_lookup_key = child_class.__qualname__
        namespace = Namespace()

        # when
        namespace.register_injectable(injectable, child_class)

        # then
        assert namespace.class_registry[child_class_lookup_key] == {injectable}
        assert namespace.class_registry[base_class_lookup_key] == {injectable}

    def test__register_injectable__with_propagation_disabled(self):
        # given
        injectable = MagicMock(spec=Injectable)
        base_class = TestNamespace
        base_class_lookup_key = base_class.__qualname__

        class Child(base_class): ...

        child_class = Child
        child_class_lookup_key = child_class.__qualname__
        namespace = Namespace()

        # when
        namespace.register_injectable(injectable, child_class, propagate=False)

        # then
        assert namespace.class_registry[child_class_lookup_key] == {injectable}
        assert base_class_lookup_key not in namespace.class_registry

    def test__register_injectable__class_and_qualifier_overloading(self):
        # given
        injectable = MagicMock(spec=Injectable)
        overloading_injectable = MagicMock(spec=Injectable)
        klass = TestNamespace
        class_lookup_key = klass.__qualname__
        qualifier = "qualifier"
        namespace = Namespace()
        namespace.register_injectable(injectable, klass, qualifier)

        # when
        namespace.register_injectable(overloading_injectable, klass, qualifier)

        # then
        assert namespace.class_registry[class_lookup_key] == {
            injectable,
            overloading_injectable,
        }
        assert namespace.qualifier_registry[qualifier] == {
            injectable,
            overloading_injectable,
        }
