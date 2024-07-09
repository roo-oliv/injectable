"""
Test the fix for the issue 80:
Injectable fails reading files with UTF-8 characters in Windows.
https://github.com/roo-oliv/injectable/issues/80

Injectable 3.4.4 and prior releases attempted to read files with the default system
encoding, which is 'cp-1252' for Windows, and throws an UnicodeDecodeError when reading
files with UTF-8 characters.

This issue was fixed in injectable 3.4.5.
"""

from injectable import injectable, autowired, Autowired, load_injection_container


@injectable
class Foo80:
    pass


@autowired
def bar(foo: Autowired(Foo80)):
    """UTF-8 chars: ⏩⏰⏣⎇⎗⎙⏻⏿⏨⏆什"""
    assert foo is not None


def test_issue_80_fix():
    load_injection_container()
    bar()
