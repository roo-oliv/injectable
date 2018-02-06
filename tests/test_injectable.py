from lazy_object_proxy import Proxy
import pytest

from injectable import injectable
from injectable import lazy


class DummyClass(object):
    def dummy_method(self):
        return 42


class NoDefaultConstructorClass(object):
    def __init__(self, something):
        pass


def bar(*args, x: DummyClass = None, f: callable):
    return args, {'x': x, 'f': f}


def foo(a,
        b: int,
        c,
        *,
        w=42,
        x: str = None,
        y: 'bool',
        z: DummyClass,
        f: callable,
        l: lazy(DummyClass),
        s: lazy('DummyClass'),
        **kwargs):
    kwargs.update({
        'w': w,
        'x': x,
        'y': y,
        'z': z,
        'f': f,
        'l': l,
        's': s,
    })
    return (a, b, c), kwargs


def baz(*, nope: 'NoDefaultConstructorClass'):
    return nope


def qux(*, nope: NoDefaultConstructorClass):
    return nope


def quux(*, definetly_nope: 'nonsense'):
    return definetly_nope


class TestInjectableAnnotation(object):

    def test_ineffective_use_of_annotation_logs_warning(self, log_capture):
        injectable()(bar)

        log_capture.check(
            ('root', 'WARNING',
             "Function 'bar' is annotated with '@injectable' but no arguments"
             " that qualify as injectable were found"))

    def test_positional_arg_as_injectable_raises_type_error(self):
        with pytest.raises(TypeError):
            injectable(['b'])(foo)

    def test_injectable_kwarg_with_no_class_annotation_raises_type_error(self):
        with pytest.raises(TypeError):
            injectable(['f'])(foo)

    def test_missing_positional_arguments_raises_type_error(self):
        with pytest.raises(TypeError):
            injectable()(foo)()

    def test_missing_kwonly_args_raises_type_error(self):
        with pytest.raises(TypeError):
            injectable()(foo)(a=None, b=10, c='')

    def test_caller_defined_arguments_are_not_overridden(self):
        caller_args = (True, 80, [])
        caller_kwargs = {
            'w': {},
            'x': "string",
            'y': True,
            'z': None,
            'f': lambda x: print(x),
            'l': 42,
            's': '42',
            'extra': True,
        }

        args, kwargs = injectable()(foo)(*caller_args, **caller_kwargs)

        assert args == caller_args
        assert kwargs == caller_kwargs

    def test_injectables_initialization_when_not_injected(self):
        caller_args = (False, None, True)
        caller_kwargs = {
            'w': {},
            'x': "string",
            'f': lambda x: print(x),
            'kwargs': {'extra': True},
        }

        _, kwargs = injectable()(foo)(*caller_args, **caller_kwargs)

        assert isinstance(kwargs['y'], bool)
        assert isinstance(kwargs['z'], DummyClass)
        assert isinstance(kwargs['l'], DummyClass)
        assert isinstance(kwargs['s'], DummyClass)

    def test_injectable_lazy_initialization(self):
        caller_args = (False, None, True)
        caller_kwargs = {
            'w': {},
            'x': "string",
            'f': lambda x: print(x),
            'kwargs': {'extra': True},
        }

        _, kwargs = injectable()(foo)(*caller_args, **caller_kwargs)

        assert isinstance(kwargs['l'], Proxy)
        assert isinstance(kwargs['l'], DummyClass)
        assert kwargs['l'].dummy_method() == 42

    def test_force_lazy_initialization(self, log_capture):
        caller_args = (False, None, True)
        caller_kwargs = {
            'w': {},
            'x': "string",
            'f': lambda x: print(x),
            'kwargs': {'extra': True},
        }

        decorated = injectable(lazy=True)(foo)

        log_capture.check(
            ('root', 'WARNING',
             "@injectable decorator is set to always lazy initialize"
             " dependencies. Usage of 'lazy' function to mark dependencies"
             " as lazy is redundant"))

        _, kwargs = decorated(*caller_args, **caller_kwargs)

        assert isinstance(kwargs['y'], Proxy)
        assert isinstance(kwargs['z'], Proxy)
        assert isinstance(kwargs['l'], Proxy)
        assert isinstance(kwargs['s'], Proxy)
        assert isinstance(kwargs['y'], bool)
        assert isinstance(kwargs['z'], DummyClass)
        assert isinstance(kwargs['l'], DummyClass)
        assert isinstance(kwargs['s'], DummyClass)

    def test_default_not_to_lazy_initialize(self):
        caller_args = (False, None, True)
        caller_kwargs = {
            'w': {},
            'x': "string",
            'f': lambda x: print(x),
            'kwargs': {'extra': True},
        }

        _, kwargs = injectable()(foo)(*caller_args, **caller_kwargs)

        assert not isinstance(kwargs['y'], Proxy)
        assert not isinstance(kwargs['z'], Proxy)
        assert isinstance(kwargs['l'], Proxy)
        assert isinstance(kwargs['s'], Proxy)

    def test_injectable_with_non_instantiable_class_raises_type_error(self):
        # eligible injectable argument is annotated with non
        # instantiable class
        with pytest.raises(TypeError):
            injectable()(baz)
        with pytest.raises(TypeError):
            injectable()(qux)

        # specified argument for injection is annotated with non
        # instantiable class
        with pytest.raises(TypeError):
            injectable(['nope'])(baz)
        with pytest.raises(TypeError):
            injectable(['nope'])(qux)

    def test_injectable_with_unresolvable_reference_raises_type_error(self):
        with pytest.raises(TypeError):
            injectable()(quux)
