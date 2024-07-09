"""
Test the fix for the issue 30:
Injectable fails to resolve entangled imports
https://github.com/roo-oliv/injectable/issues/30

Injectable 3.4.2 attempted to manually import injectables into system modules. This
was causing unintended side effects. Now it just executes the injectable's files.

This issue was fixed in injectable 3.4.3.
"""

from injectable import autowired, Autowired, load_injection_container
from injectable.testing import reset_injection_container


@autowired
def f(foo: Autowired("foo")): ...


def test_issue_30_fix():
    reset_injection_container()
    load_injection_container()
    f()
