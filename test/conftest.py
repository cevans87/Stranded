import pytest


@pytest.fixture
def log_capture_fixture(caplog: pytest.LogCaptureFixture) -> pytest.LogCaptureFixture:
    # `caplog` is pytest's built-in fixture name; alias it so tests can name the
    # parameter after its type (`LogCaptureFixture`).
    return caplog
