from unittest.mock import MagicMock

from injectable import autowired
from injectable.autowiring.autowired_type import _Autowired


class TestAutowiredDecoratorPy38:
    def test__autowired__with_positional_only_args(self):
        # given
        AutowiredMockA = MagicMock(spec=_Autowired)
        AutowiredMockB = MagicMock(spec=_Autowired)
        AutowiredMockC = MagicMock(spec=_Autowired)

        @autowired
        def f(
            a: AutowiredMockA,
            /,  # noqa: E999, E225
            b: AutowiredMockB,
            c: AutowiredMockC,
        ):
            return {"a": a, "b": b, "c": c}

        # when
        parameters = f(b=None)

        # then
        assert AutowiredMockA.inject.called is True
        assert AutowiredMockB.inject.called is False
        assert AutowiredMockC.inject.called is True
        assert parameters["a"] is AutowiredMockA.inject()
        assert parameters["b"] is None
        assert parameters["c"] is AutowiredMockC.inject()
