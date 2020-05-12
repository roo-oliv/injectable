import sys
import pytest

if sys.version_info[:2] < (3, 8):
    pytest.skip("Skipping Python 3.8+-only tests", allow_module_level=True)
