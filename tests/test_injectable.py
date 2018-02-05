import pytest

from injectable import injectable


class DummyClass(object):
    pass


class NoDefaultConstructorClass(object):
    def __init__(self, something):
        pass


def bar(*args, x: DummyClass = None, y: 'DummyClass', f: callable):
    return args, {'x': x, 'y': y, 'f': f}


def foo(a,
        b: int,
        c,
        *,
        w=42,
        x: str = None,
        y: 'bool',
        z: DummyClass,
        f: callable,
        **kwargs):
    kwargs.update({
        'w': w,
        'x': x,
        'y': y,
        'z': z,
        'f': f,
    })
    return (a, b, c), kwargs


def qux(*, nope: NoDefaultConstructorClass):
    return nope


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
            'y': True,
            'f': lambda x: print(x),
            'kwargs': {'extra': True},
        }

        args, kwargs = injectable()(foo)(*caller_args, **caller_kwargs)

        assert isinstance(kwargs['z'], DummyClass)

    def test_injectable_with_non_instantiable_class_raises_type_error(self):
        # eligible injectable argument is annotated with non
        # instantiable class
        with pytest.raises(TypeError):
            injectable()(qux)

        # specificed argument for injection is annotated with non
        # instantiable class
        with pytest.raises(TypeError):
            injectable(['nope'])(qux)
