"""
Testing utilities to ease mocking injectables.

A usage example is available in the :ref:`testing_example` subsection of the
:ref:`usage_examples` section.
"""
from injectable.testing.clear_injectables import clear_injectables
from injectable.testing.register_injectables import register_injectables

__all__ = ["clear_injectables", "register_injectables"]
