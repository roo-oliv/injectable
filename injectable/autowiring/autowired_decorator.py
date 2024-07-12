import inspect
from functools import wraps
from typing import TypeVar, Callable, Any, get_args, _AnnotatedAlias, Union

from injectable.autowiring.autowired_type import _Autowired, Autowired
from injectable.errors import AutowiringError

T = TypeVar("T", bound=Callable[..., Any])


def autowired(func: T) -> T:
    """
    Function decorator to setup dependency injection autowiring.

    Only parameters annotated with :class:`Autowired <injectable.Autowired>` will be
    autowired for injection.

    If no parameter is annotated with :class:`Autowired <injectable.Autowired>` an
    :class:`AutowiringError <injectable.errors.AutowiringError>` will be raised.

    An :class:`AutowiringError <injectable.errors.AutowiringError>` will also be raised
    if a parameter annotated with :class:`Autowired <injectable.Autowired>` is given a
    default value or if a non Autowired-annotated positional parameter is placed after
    an Autowired-annotated positional parameter.

    Before attempting to call an autowired function make sure
    :meth:`load_injection_container <injectable.load_injection_container>` was invoked.

    .. note::
      This decorator can be applied to any function, not only an `__init__` method.

    .. note::
      This decorator accepts no arguments and must be used without trailing parenthesis.

    Usage::

      >>> from injectable import Autowired, autowired
      >>>
      >>> @autowired
      ... def foo(dep: Autowired(...)):
      ...     ...
    """
    signature = inspect.signature(func)
    autowired_parameters = []
    for index, parameter in enumerate(signature.parameters.values()):
        annotation = _get_parameter_annotation(parameter)

        if not isinstance(annotation, _Autowired):
            if len(autowired_parameters) == 0 or parameter.kind in [
                parameter.KEYWORD_ONLY,
                parameter.VAR_KEYWORD,
            ]:
                continue
            raise AutowiringError(
                "Non-Autowired positional parameter follows Autowired parameter"
            )
        if parameter.default is not parameter.empty:
            raise AutowiringError("Default value assigned to Autowired parameter")
        if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            raise AutowiringError(f"Autowired parameter is of kind {parameter.kind}")
        autowired_parameters.append(parameter)

    if len(autowired_parameters) == 0:
        raise AutowiringError("No parameter is typed with 'Autowired'")

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_arguments = signature.bind_partial(*args, **kwargs).arguments
        args = list(args)
        for parameter in autowired_parameters:
            if parameter.name in bound_arguments:
                continue
            annotation = _get_parameter_annotation(parameter)
            dependency = annotation.inject()
            if parameter.kind is parameter.POSITIONAL_ONLY:
                args.append(dependency)
            else:
                kwargs[parameter.name] = dependency

        return func(*args, **kwargs)

    return wrapper


def _get_parameter_annotation(parameter) -> Union[type, _Autowired]:
    if isinstance(parameter.annotation, _AnnotatedAlias):
        autowired_annotations = list(
            filter(lambda t: _is_autowired(t), _get_args_flattened(parameter.annotation))
        )
        if len(autowired_annotations) == 0:
            return parameter.annotation
        if len(autowired_annotations) > 1:
            raise AutowiringError("Multiple Autowired annotations found")
        autowired_annotation = autowired_annotations[0]
        if not isinstance(autowired_annotation, _Autowired):
            return get_args(autowired_annotation(dependency=get_args(parameter.annotation)[0]))[1]
        if autowired_annotation.dependency is None:
            return type(autowired_annotation)(
                dependency=get_args(parameter.annotation)[0],
                namespace=autowired_annotation.namespace,
                group=autowired_annotation.group,
                exclude_groups=autowired_annotation.exclude_groups,
                lazy=autowired_annotation.lazy,
            )
        return autowired_annotation

    return parameter.annotation


def _is_autowired(annotation) -> bool:
    return isinstance(annotation, _Autowired) or (
        inspect.isclass(annotation) and issubclass(annotation, Autowired)
    )


def _get_args_flattened(annotation) -> list:
    return [
        arg
        for e in get_args(annotation)
        for arg in (_get_args_flattened(e) if isinstance(e, _AnnotatedAlias) else [e])
    ]
