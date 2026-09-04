# Data Model: Simple Goal Tracker

## Goal

Represents one user-defined commitment held only during the active process session.

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| id | opaque identifier | yes | Generated uniquely within the active session | Used for actions, not shown as user content |
| title | text | yes | Trim surrounding whitespace; 1-200 characters after trimming | Duplicate titles are allowed |
| description | text | no | Treat missing value as empty; maximum 2,000 characters | May be blank |
| completed | boolean | yes | Defaults to false | Only incomplete goals transition to completed |

All creation and update payloads MUST be parsed by Pydantic before the state service processes
or mutates them. Invalid payloads MUST leave the prior state unchanged.

## Goal Status

- `incomplete`: initial state for every new goal.
- `completed`: reached when the user marks an incomplete goal complete.

The completed state is idempotent: marking an already completed goal complete leaves it
completed and does not affect any other goal.

## Active Session

The state container holds an ordered collection of goals for one running tracker process. It
starts empty, has no external persistence, and is discarded when the process closes or restarts.
Removing the last goal returns the collection to its empty state.

## State Transitions

| Current state | Action | Result |
|---------------|--------|--------|
| Empty | Create valid goal | One incomplete goal |
| Non-empty | Create valid goal | Existing goals unchanged; new incomplete goal appended |
| Incomplete | Complete | Completed |
| Completed | Complete | Completed; no other changes |
| Existing | Valid edit | Updated title/description; status preserved |
| Existing | Invalid edit | No change; validation feedback |
| Existing | Confirm removal | Goal removed |
| Existing | Cancel removal | No change |
| Any | Process restart | Empty active session |
