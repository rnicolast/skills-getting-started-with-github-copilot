import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module

# store a deep copy of the initial activities state so we can restore it between tests
_original_activities = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before each test."""
    # reassign a deep copy to avoid mutation sharing
    app_module.activities = copy.deepcopy(_original_activities)
    yield
    # after the test we could also restore, but autouse ensures isolation

@pytest.fixture

def client():
    """A test client that can be used to exercise the API."""
    return TestClient(app_module.app)
