"""
Test the fix for the issue 81:
No context is created when no injectables are found, attempt to put object fails.
https://github.com/roo-oliv/injectable/issues/81

In injectable 3.4.5 and prior releases the :func:`testing.register_injectables` utility
wasn't check for the existence of the requested namespace and would fail if it didn't
exist. Currently, there is no public API exposed for direct creation of a namespace. This
is only possible when loading the injection container and a injectable is discovered and
registered to the namespace.

This issue was fixed in injectable 3.4.6.
"""

from injectable import Injectable, inject
from injectable.testing import register_injectables, reset_injection_container


def foo():
    mocked_injectable = Injectable(lambda: object())
    register_injectables({mocked_injectable}, object)
    assert inject(object)


def test_issue_81_fix():
    reset_injection_container()
    foo()
