"""
Core injectable API.

A collection of examples on how to use the provided API is available in the
:ref:`usage_examples` section.
"""
from injectable.autowiring.autowired_type import Autowired
from injectable.autowiring.autowired_decorator import autowired
from injectable.container.injection_container import InjectionContainer
from injectable.container.injectable import Injectable
from injectable.injection.injectable_factory_decorator import injectable_factory
from injectable.injection.inject import inject, inject_multiple
from injectable.injection.injectable_decorator import injectable
from injectable import errors
from injectable import testing

__all__ = [
    "InjectionContainer",
    "Injectable",
    "autowired",
    "Autowired",
    "injectable_factory",
    "injectable",
    "inject",
    "inject_multiple",
    "errors",
    "testing",
]
