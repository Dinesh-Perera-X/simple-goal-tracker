import pytest

from goal_tracker.app import create_app
from goal_tracker.state import GoalStore


@pytest.fixture
def store():
    return GoalStore()


@pytest.fixture
def client(store):
    app = create_app(store=store)
    app.config.update(TESTING=True)
    return app.test_client()
