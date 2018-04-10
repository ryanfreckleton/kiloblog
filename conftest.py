import pytest
import kiloblog


@pytest.fixture
def app():
    return kiloblog.app
