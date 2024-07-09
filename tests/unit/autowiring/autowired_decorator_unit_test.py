from typing import Annotated, Optional
from unittest.mock import MagicMock

import pytest
from injectable import autowired, Autowired
from injectable.autowiring.autowired_type import _Autowired
from injectable.errors import AutowiringError, InjectionError
from pytest_mock import MockFixture


class TestAutowiredDecorator:
    def test__autowired__without_arguments_raises(self):
        # given
        def f(): ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__without_autowired_arguments_raises(self):
        # given
        def f(a, b): ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_autowired_arg_given_default_value_raises(self):
        # given
        def f(a: Autowired("A") = None): ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_non_autowired_positional_arg_after_autowired_arg_raises(
        self,
    ):
        # given
        def f(a: Autowired("A"), b): ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_non_autowired_var_arg_after_autowired_arg_raises(self):
        # given
        def f(a: Autowired("A"), *b): ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_autowired_variadic_positional_arg_raises(self):
        # given
        def f(*a: Autowired("A")): ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_autowired_variadic_keyword_arg_raises(self):
        # given
        def f(**a: Autowired("A")): ...

        # then
        with pytest.raises(AutowiringError):
            autowired(f)

    def test__autowired__with_autowired_positional_arg_does_not_raise(self):
        # given
        def f(a: Autowired("A")): ...

        # then
        autowired(f)

    def test__autowired__with_autowired_positional_arg_following_others_does_not_raise(
        self,
    ):
        # given
        def f(a, b: Autowired("B")): ...

        # then
        autowired(f)

    def test__autowired__with_kwonly_arg_after_autowired_positional_arg_does_not_raise(
        self,
    ):
        # given
        def f(a: Autowired("A"), *, k): ...

        # then
        autowired(f)

    def test__autowired__with_var_kw_arg_after_autowired_positional_arg_does_not_raise(
        self,
    ):
        # given
        def f(a: Autowired("A"), **k): ...

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

    def test__autowired__with_one_autowired_in_annotated(self):
        # given
        AutowiredMock = MagicMock(spec=_Autowired)
        AutowiredMock.dependency = "dependency"

        @autowired
        def f(a: Annotated[type, AutowiredMock]):
            return {"a": a}

        # when
        parameters = f()

        # then
        assert AutowiredMock.inject.called is True
        assert parameters["a"] is AutowiredMock.inject()

    def test__autowired__with_two_autowired_in_annotation_raises(self):
        # given
        AutowiredMockA = MagicMock(spec=_Autowired)
        AutowiredMockA.dependency = "dependency"
        AutowiredMockB = MagicMock(spec=_Autowired)
        AutowiredMockB.dependency = "dependency"

        # then
        with pytest.raises(AutowiringError):

            @autowired
            def f(a: Annotated[type, AutowiredMockA, AutowiredMockB]):
                return {"a": a}

    def test__autowired_with_no_autowire_in_annotation_continues(self):
        # given
        AutowiredMock = MagicMock(spec=_Autowired)
        AutowiredMock.dependency = "dependency"

        @autowired
        def f(a: Annotated[str, str], b: Annotated[type, AutowiredMock]):
            return {"a": a, "b": b}

        # when
        parameters = f("test")

        # then
        assert AutowiredMock.inject.called is True
        assert parameters["a"] == "test"
        assert parameters["b"] is AutowiredMock.inject()

    def test__autowired_with_no_autowire_but_with_annotated_raises(self):
        with pytest.raises(AutowiringError):

            @autowired
            def f(a: Annotated[str, str], b: Annotated[type, "foo"]):
                return {"a": a, "b": b}

    def test__autowired__w_annotated_n_no_dep_explicit_declaration_tries_to_inject_class(
        self,
    ):
        # given
        @autowired
        def f(a: Annotated[type, Autowired]):
            return {"a": a}

        # when
        with pytest.raises(InjectionError) as e:
            f()

        # then
        assert e.value.registry_type == "class"
        assert e.value.dependency_name == "type"

    def test__autowired__w_annotated_n_no_dep_explicit_declaration_tries_to_inject_qual(
        self,
    ):
        # given
        @autowired
        def f(a: Annotated["type", Autowired]):
            return {"a": a}

        # when
        with pytest.raises(InjectionError) as e:
            f()

        # then
        assert e.value.registry_type == "qualifier"
        assert e.value.dependency_name == "type"

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

    def test__inject__with_list_class_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        autowired = Autowired(list[TestAutowiredDecorator])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == TestAutowiredDecorator

    def test__inject__with_list_qualifier_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        expected = "Expected"
        autowired = Autowired(list[expected])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == expected

    def test__inject__with_optional_list_class_dependency(self, mocker: MockFixture):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        autowired = Autowired(Optional[list[TestAutowiredDecorator]])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == TestAutowiredDecorator
        assert kwargs["optional"] is True

    def test__inject__with_optional_list_qualifier_dependency(
        self, mocker: MockFixture
    ):
        # given
        mocked_inject = mocker.patch("injectable.autowiring.autowired_type.inject")
        mocked_inject_multiple = mocker.patch(
            "injectable.autowiring.autowired_type.inject_multiple"
        )
        expected = "Expected"
        autowired = Autowired(Optional[list[expected]])

        # when
        autowired.inject()

        # then
        assert mocked_inject.call_count == 0
        assert mocked_inject_multiple.call_count == 1
        args, kwargs = mocked_inject_multiple.call_args
        assert args[0] == expected
        assert kwargs["optional"] is True
