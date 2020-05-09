from unittest.mock import MagicMock

from injectable import Injectable


class TestInjectable:
    def test__init__defaults(self):
        # given
        constructor = MagicMock()

        # when
        injectable = Injectable(constructor)

        # then
        assert injectable.constructor == constructor
        assert injectable.unique_id is not None
        assert injectable.primary is False
        assert injectable.group is None
        assert injectable.singleton is False

    def test__eq__with_different_injectables(self):
        # given
        injectable_a = Injectable(None)
        injectable_b = Injectable(None)

        # then
        assert injectable_a != injectable_b

    def test__eq__with_equal_injectables(self):
        # given
        injectable_a = Injectable(MagicMock(), unique_id="0")
        injectable_b = Injectable(MagicMock(), unique_id="0")

        # then
        assert injectable_a.constructor != injectable_b.constructor
        assert injectable_a == injectable_b

    def test__get_instance__with_singleton_injectable(self):
        # given
        constructor = MagicMock(side_effect=["call_0", "call_1"])
        injectable = Injectable(constructor, singleton=True)

        # when
        instance_0 = injectable.get_instance()
        instance_1 = injectable.get_instance()

        # then
        assert constructor.call_count == 1
        assert instance_0 == instance_1

    def test__get_instance__with_non_singleton_injectable(self):
        # given
        constructor = MagicMock(side_effect=["call_0", "call_1"])
        injectable = Injectable(constructor, singleton=False)

        # when
        instance_0 = injectable.get_instance()
        instance_1 = injectable.get_instance()

        # then
        assert constructor.call_count == 2
        assert instance_0 != instance_1

    def test__get_instance__with_lazy_instance(self):
        # given
        constructor = MagicMock()
        injectable = Injectable(constructor)

        # when
        instance = injectable.get_instance(lazy=True)

        # then
        assert constructor.called is False

        # and when
        instance.anything()

        # then
        assert constructor.called is True
