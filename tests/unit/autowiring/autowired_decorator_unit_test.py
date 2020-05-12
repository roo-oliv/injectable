from unittest.mock import MagicMock

import pytest
from injectable import autowired, Autowired
from injectable.autowiring.autowired_type import _Autowired
from injectable.errors import AutowiringError


class TestAutowiredDecorator:
    def test__autowired__without_arguments_raises(self):
        # given
        def f():
            ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__without_autowired_arguments_raises(self):
        # given
        def f(a, b):
            ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_autowired_arg_given_default_value_raises(self):
        # given
        def f(a: Autowired("A") = None):
            ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_non_autowired_positional_arg_after_autowired_arg_raises(
        self,
    ):
        # given
        def f(a: Autowired("A"), b):
            ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_non_autowired_var_arg_after_autowired_arg_raises(self):
        # given
        def f(a: Autowired("A"), *b):
            ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_autowired_variadic_positional_arg_raises(self):
        # given
        def f(*a: Autowired("A")):
            ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_autowired_variadic_keyword_arg_raises(self):
        # given
        def f(**a: Autowired("A")):
            ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_autowired_positional_arg_does_not_raise(self):
        # given
        def f(a: Autowired("A")):
            ...

        # then
        autowired(f)

    def test__autowired__with_autowired_positional_arg_following_others_does_not_raise(
        self,
    ):
        # given
        def f(a, b: Autowired("B")):
            ...

        # then
        autowired(f)

    def test__autowired__with_kwonly_arg_after_autowired_positional_arg_does_not_raise(
        self,
    ):
        # given
        def f(a: Autowired("A"), *, k):
            ...

        # then
        autowired(f)

    def test__autowired__with_var_kw_arg_after_autowired_positional_arg_does_not_raise(
        self,
    ):
        # given
        def f(a: Autowired("A"), **k):
            ...

        # then
        autowired(f)

    def test__autowired__inject_autowired_arg(self):
        # given
        AutowiredMock = MagicMock(spec=_Autowired)

        @autowired
        def f(a: AutowiredMock):
            return {"a": a}

        # when
        parameters = f()

        # then
        assert AutowiredMock.inject.called is True
        assert parameters["a"] is AutowiredMock.inject()

    def test__autowired__inject_only_autowired_arg(self):
        # given
        AutowiredMockA = MagicMock(spec=_Autowired)
        AutowiredMockC = MagicMock(spec=_Autowired)

        @autowired
        def f(a: AutowiredMockA, *, b=None, c: AutowiredMockC):
            return {"a": a, "b": b, "c": c}

        # when
        parameters = f()

        # then
        assert AutowiredMockA.inject.call_count == 1
        assert AutowiredMockC.inject.call_count == 1
        assert parameters["a"] is AutowiredMockA.inject()
        assert parameters["b"] is None
        assert parameters["c"] is AutowiredMockC.inject()

    def test__autowired__does_not_inject_autowired_args_defined_by_the_caller(self):
        # given
        AutowiredMockA = MagicMock(spec=_Autowired)
        AutowiredMockB = MagicMock(spec=_Autowired)
        AutowiredMockC = MagicMock(spec=_Autowired)

        @autowired
        def f(a: AutowiredMockA, b: AutowiredMockB, c: AutowiredMockC):
            return {"a": a, "b": b, "c": c}

        # when
        parameters = f(None, c=None)

        # then
        assert AutowiredMockA.inject.called is False
        assert AutowiredMockB.inject.called is True
        assert AutowiredMockC.inject.called is False
        assert parameters["a"] is None
        assert parameters["b"] is AutowiredMockB.inject()
        assert parameters["c"] is None

    def test__autowired__with_named_args_defined_by_the_caller(self):
        # given
        AutowiredMockA = MagicMock(spec=_Autowired)
        AutowiredMockB = MagicMock(spec=_Autowired)
        AutowiredMockC = MagicMock(spec=_Autowired)

        @autowired
        def f(a: AutowiredMockA, b: AutowiredMockB, c: AutowiredMockC):
            return {"a": a, "b": b, "c": c}

        # when
        parameters = f(None, b=None)

        # then
        assert AutowiredMockA.inject.called is False
        assert AutowiredMockB.inject.called is False
        assert AutowiredMockC.inject.called is True
        assert parameters["a"] is None
        assert parameters["b"] is None
        assert parameters["c"] is AutowiredMockC.inject()
