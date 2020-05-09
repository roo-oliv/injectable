"""
This is the injectable's public API.

.. seealso::

    The :ref:`usage_examples` section presents a collection of examples on how to use
    this API.
"""
from injectable.autowiring.autowired_type import Autowired
from injectable.autowiring.autowired_decorator import autowired
from injectable.container.injection_container import InjectionContainer
from injectable.container.injectable import Injectable
from injectable.container.load_injection_container import load_injection_container
from injectable.injection.injectable_factory_decorator import injectable_factory
from injectable.injection.inject import inject, inject_multiple
from injectable.injection.injectable_decorator import injectable
from injectable import errors
from injectable import testing
from injectable import constants

__all__ = [
    "load_injection_container",
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
    "constants",
]
