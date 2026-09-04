import pytest
from pydantic import ValidationError

from goal_tracker.models import GoalCreate, GoalUpdate
from goal_tracker.state import GoalNotFound, GoalStore


def test_store_creates_ordered_incomplete_goals_and_allows_duplicates():
    store = GoalStore()
    first = store.create(GoalCreate(title="Read"))
    second = store.create(GoalCreate(title="Read"))

    assert [goal.title for goal in store.list()] == ["Read", "Read"]
    assert first.completed is False
    assert second.completed is False


def test_store_completing_goal_is_idempotent_and_isolated():
    store = GoalStore()
    first = store.create(GoalCreate(title="Read"))
    second = store.create(GoalCreate(title="Run"))

    completed = store.complete(first.id)
    repeated = store.complete(first.id)

    assert completed.completed is True
    assert repeated.completed is True
    assert store.get(second.id).completed is False


def test_store_invalid_update_does_not_mutate_prior_state():
    store = GoalStore()
    goal = store.create(GoalCreate(title="Read"))

    with pytest.raises(ValidationError):
        store.update(goal.id, GoalUpdate(title=" " * 3))

    assert store.get(goal.id).title == "Read"


def test_store_removing_final_goal_returns_empty_state():
    store = GoalStore()
    goal = store.create(GoalCreate(title="Read"))

    store.remove(goal.id)

    assert store.list() == []


def test_store_missing_goal_raises():
    with pytest.raises(GoalNotFound):
        GoalStore().get("missing")
