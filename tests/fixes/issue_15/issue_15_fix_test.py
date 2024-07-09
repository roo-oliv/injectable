"""
Test the fix for the issue 15:
Using named args breaks injectable
https://github.com/roo-oliv/injectable/issues/15

Injectable 3.4.0 attempted to always inject autowired parameters as positional args
which may result in passing a duplicated parameter when the caller passes a
non-keyword-only parameter as named arg.

This issue was fixed in injectable 3.4.1.
"""

from injectable import injectable, autowired, Autowired, load_injection_container


@injectable
class Foo:
    pass


@autowired
def bar(qux, foo: Autowired(Foo)):
    assert qux == "QUX"
    assert foo is not None


def test_issue_15_fix():
    load_injection_container()
    bar(qux="QUX")
