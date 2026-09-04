import pytest
from pydantic import ValidationError

from goal_tracker.models import GoalCreate, GoalUpdate


def test_goal_create_trims_title_and_defaults_description():
    goal = GoalCreate(title="  Read more  ")

    assert goal.title == "Read more"
    assert goal.description == ""


def test_goal_create_rejects_whitespace_title():
    with pytest.raises(ValidationError):
        GoalCreate(title="   ")


def test_goal_create_enforces_field_limits():
    with pytest.raises(ValidationError):
        GoalCreate(title="a" * 201)
    with pytest.raises(ValidationError):
        GoalCreate(title="Valid", description="a" * 2001)


def test_goal_update_allows_partial_description_update():
    update = GoalUpdate(description="Practice every day")

    assert update.title is None
    assert update.description == "Practice every day"
