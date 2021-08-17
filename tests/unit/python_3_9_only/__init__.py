import sys
import pytest

if sys.version_info[:2] < (3, 9):
    pytest.skip("Skipping Python 3.9+-only tests", allow_module_level=True)
