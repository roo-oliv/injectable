"""
Do not try to reproduce anything you see here at home
"""
import types


def get_class(reference: str, reference_module: dict):
    """
    return a class reference found in the reference_module
    """
    if reference in reference_module:
        return reference_module.get(reference)
    else:
        return reference_module.get('__builtins__').get(reference)


def copy_func(f, name=None):
    """
    return a function with same code, globals, defaults, closure, and
    name (or provide a new name)
    """
    fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__,
                            f.__defaults__, f.__closure__)
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)
    return fn
