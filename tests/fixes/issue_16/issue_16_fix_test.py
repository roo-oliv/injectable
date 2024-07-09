"""
Test the fix for the issue 16:
Optional injection doesn't work when there are the namespace is empty
https://github.com/roo-oliv/injectable/issues/16

Injectable 3.4.1 attempted to get the namespace to perform an injection by direct key
access which would result in an error if the namespace doesn't exist. This behavior
would lead to optional injections referring an inexistent namespace to fail.

This issue was fixed in injectable 3.4.2.
"""

from typing import Optional

from injectable import autowired, Autowired
from injectable.testing import reset_injection_container


@autowired
def a(x: Autowired(Optional["anything"])):
    assert x is None


def test_issue_15_fix():
    reset_injection_container()
    a()
