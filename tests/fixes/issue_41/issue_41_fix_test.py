"""
Test the fix for the issue 41:
ImportError due to changes in 3.4.3
https://github.com/roo-oliv/injectable/issues/41

Injectable (>=3.4.3, <= 3.4.6) executes files with injectables as scripts to register
dependencies but this does not work for files which use relative imports.

This issue was fixed in injectable 3.4.7 by executing files as modules but a fallback
to script-like execution still exists due to some corner cases involving pytest.
Specifically, if you declare injectables in the same file of the test being run the
fallback will be used so if you also use relative imports in this test injectable will
fail to load the injection container. The workaround for now would be to use absolute
imports or to declare the injectables in a separated file.
"""

from injectable import autowired, Autowired, load_injection_container
from injectable.testing import reset_injection_container


@autowired
def f(foo: Autowired("foo")):
    assert foo.is_ok()


def test_issue_41_fix():
    reset_injection_container()
    load_injection_container()
    f()
