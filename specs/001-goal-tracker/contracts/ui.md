# User Interface Contract: Simple Goal Tracker

## Screen

The tracker exposes one primary screen containing:

- A goal creation form with a required title field, optional description field, and submit
  control.
- An empty-state message when no goals exist.
- A goal list where every item shows its title, optional description, and unambiguous status.
- Controls to complete, edit, and remove each goal.

## Interaction Rules

- Submitting a valid form adds an incomplete goal and provides visible success feedback.
- Missing, whitespace-only, or overlong values remain uncommitted and identify the field needing
  correction with a non-sensitive message.
- Completing a goal updates its status without changing other goals.
- Editing updates title and/or description while preserving completion status.
- Removing requires confirmation; cancellation leaves the goal unchanged.
- Duplicate titles are accepted.
- Closing or restarting the process exposes an empty list because no data is persisted.

## Accessibility Rules

- Every input and action control has an accessible name.
- Status is conveyed through text as well as visual styling.
- Validation and success feedback is associated with the relevant form or action and is
  available to assistive technology.
- All workflows are operable with keyboard input and have a visible focus indicator.

## Error Contract

Validation failures return a user-readable correction message and do not mutate session state.
Unexpected failures return a generic non-sensitive error message and do not expose internal
paths, stack traces, or data.
