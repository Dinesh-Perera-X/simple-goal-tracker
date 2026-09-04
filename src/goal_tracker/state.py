from typing import List

from .models import Goal, GoalCreate, GoalUpdate


class GoalNotFound(Exception):
    pass


class GoalStore:
    def __init__(self) -> None:
        self._goals: list[Goal] = []

    def list(self) -> List[Goal]:
        return [goal.model_copy(deep=True) for goal in self._goals]

    def get(self, goal_id: str) -> Goal:
        for goal in self._goals:
            if goal.id == goal_id:
                return goal.model_copy(deep=True)
        raise GoalNotFound(goal_id)

    def create(self, payload: GoalCreate) -> Goal:
        goal = Goal(title=payload.title, description=payload.description)
        self._goals.append(goal)
        return goal.model_copy(deep=True)

    def complete(self, goal_id: str) -> Goal:
        for goal in self._goals:
            if goal.id == goal_id:
                goal.completed = True
                return goal.model_copy(deep=True)
        raise GoalNotFound(goal_id)

    def update(self, goal_id: str, payload: GoalUpdate) -> Goal:
        for goal in self._goals:
            if goal.id == goal_id:
                if payload.title is not None:
                    goal.title = payload.title
                if payload.description is not None:
                    goal.description = payload.description
                return goal.model_copy(deep=True)
        raise GoalNotFound(goal_id)

    def remove(self, goal_id: str) -> None:
        for index, goal in enumerate(self._goals):
            if goal.id == goal_id:
                del self._goals[index]
                return
        raise GoalNotFound(goal_id)
