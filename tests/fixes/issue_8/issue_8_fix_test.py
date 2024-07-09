"""
Test the fix for the issue 8:
Autowired(List[...]) does not work with qualifiers
https://github.com/roo-oliv/injectable/issues/8

Injectable 3.1.3 attempts to use the argument of typing.List as a qualifier though
string arguments to subscriptable typing types are encapsulated in a typing.ForwardRef
object so the argument of the ForwardRef should be used as qualifier actually and not
the ForwardRef object itself.

This issue was fixed in injectable 3.1.4.
"""

from typing import List

from injectable import injectable, autowired, Autowired, load_injection_container
from injectable.testing import reset_injection_container


@injectable(qualifier="foo")
class Foo:
    pass


@autowired
def bar(foo: Autowired(List["foo"])):
    assert foo is not None
    assert len(foo) == 1


def test_issue_8_fix():
    reset_injection_container()
    load_injection_container()
    bar()
