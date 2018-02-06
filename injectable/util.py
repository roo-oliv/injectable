import inspect

from typing import Type


def get_class(reference: str, reference_module: dict) -> Type:
    """
    return a class reference found in the reference_module
    """
    if reference in reference_module:
        return reference_module.get(reference)
    else:
        return reference_module.get('__builtins__').get(reference)


def is_lazy(reference) -> bool:
    try:
        return reference.lazy_init
    except AttributeError:
        return False


def is_injectable(argument: str, specs: inspect.FullArgSpec) -> bool:
    if specs.kwonlydefaults is not None and argument in specs.kwonlydefaults:
        return False

    annotation = specs.annotations.get(argument)

    if inspect.isclass(annotation):
        return True

    if isinstance(annotation, str):
        return True

    return is_lazy(annotation)


def lazy(type_annotation: (Type, str)):

    def wrapper():
        return type_annotation
    wrapper.lazy_init = True

    return wrapper
