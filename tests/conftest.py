import pytest
from testfixtures import LogCapture


@pytest.fixture(autouse=True)
def log_capture():
    with LogCapture() as capture:
        yield capture
