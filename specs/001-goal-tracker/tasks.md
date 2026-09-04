---

description: "Executable task list for the Simple Goal Tracker"
---

# Tasks: Simple Goal Tracker

**Input**: Design documents from `/specs/001-goal-tracker/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ui.md,
quickstart.md

**Tests**: Included because the constitution and specification require deterministic automated
coverage, including dedicated boundary and validation tests.

**Organization**: Tasks are grouped by user story so each increment can be implemented and
tested independently after the shared foundation is complete.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the Python web application and test tooling.

- [X] T001 Create the source and test directory structure from plan.md in `src/` and `tests/`
- [X] T002 [P] Create the Python package entry point in `src/goal_tracker/__init__.py`
- [X] T003 [P] Add Flask, Pydantic, and pytest dependency pins in `requirements.txt`
- [X] T004 [P] Add local test configuration and source import settings in `pytest.ini`
- [X] T005 [P] Add the local run and test commands to `README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish validation, state ownership, application wiring, and shared UI structure
before any story-specific work.

**CRITICAL**: User story work depends on this phase.

- [X] T006 Define the Goal, GoalCreate, and GoalUpdate Pydantic models in `src/goal_tracker/models.py`
- [X] T007 Implement process-local active-session state and goal state transitions in `src/goal_tracker/state.py`
- [X] T008 [P] Implement centralized Pydantic validation error formatting in `src/goal_tracker/validation.py`
- [X] T009 [P] Create the Flask application factory and route registration in `src/goal_tracker/app.py`
- [X] T010 [P] Create the semantic page shell, accessible form regions, feedback region, and goal-list placeholders in `src/goal_tracker/templates/index.html`
- [X] T011 [P] Add consistent status, focus, validation, and responsive layout styles in `src/goal_tracker/static/styles.css`
- [X] T012 [P] Add foundational model and state boundary tests in `tests/unit/test_models.py` and `tests/unit/test_state.py`
- [X] T013 Add shared test fixtures for a fresh active session and Flask test client in `tests/conftest.py`

**Checkpoint**: The application can start with an empty in-memory session, validate inputs, and
render the accessible shell before story behavior is added.

---

## Phase 3: User Story 1 - Create and View Goals (Priority: P1) MVP

**Goal**: Let a user create valid goals and see every active goal with clear incomplete status.

**Independent Test**: Start with an empty session, create two valid goals, and verify both
appear with their titles and incomplete statuses; submit invalid titles and verify no mutation.

### Tests for User Story 1

- [X] T014 [P] [US1] Add unit tests for valid goal creation, duplicate titles, title trimming, empty titles, and maximum title/description lengths in `tests/unit/test_state.py`
- [X] T015 [P] [US1] Add integration tests for create, list, empty-state, validation feedback, and Pydantic rejection flows in `tests/integration/test_goal_flows.py`

### Implementation for User Story 1

- [X] T016 [US1] Implement validated create-goal state mutation and ordered listing in `src/goal_tracker/state.py`
- [X] T017 [US1] Implement the create-goal and list-goals routes with validation feedback in `src/goal_tracker/app.py`
- [X] T018 [US1] Render goal titles, optional descriptions, incomplete status text, and empty-state feedback in `src/goal_tracker/templates/index.html`
- [X] T019 [US1] Add create-form, goal-list, and incomplete-status presentation styles in `src/goal_tracker/static/styles.css`

**Checkpoint**: User Story 1 is independently functional and testable as the MVP.

---

## Phase 4: User Story 2 - Complete Goals (Priority: P1)

**Goal**: Let a user mark goals complete while keeping all other goal statuses unchanged.

**Independent Test**: Create multiple goals, complete one, and verify only that goal changes to
completed and remains visually and textually distinct.

### Tests for User Story 2

- [X] T020 [P] [US2] Add unit tests for incomplete-to-completed and already-completed idempotent transitions in `tests/unit/test_state.py`
- [X] T021 [P] [US2] Add integration tests for completion controls, mixed statuses, and accessible status feedback in `tests/integration/test_goal_flows.py`

### Implementation for User Story 2

- [X] T022 [US2] Implement validated complete-goal state transition without affecting other goals in `src/goal_tracker/state.py`
- [X] T023 [US2] Implement the complete-goal route and success feedback in `src/goal_tracker/app.py`
- [X] T024 [US2] Add complete controls and text status changes to each goal item in `src/goal_tracker/templates/index.html`
- [X] T025 [US2] Add completed-status styling that does not rely on color alone in `src/goal_tracker/static/styles.css`

**Checkpoint**: User Stories 1 and 2 are independently functional and testable.

---

## Phase 5: User Story 3 - Revise or Remove Goals (Priority: P2)

**Goal**: Let a user edit goal content or remove a goal with confirmation and cancellation.

**Independent Test**: Edit one goal, cancel removal for a second, then confirm removal for that
second goal; verify the edit persists and only the confirmed goal disappears.

### Tests for User Story 3

- [X] T026 [P] [US3] Add unit tests for valid edits, invalid edits preserving prior state, and removal of the final goal in `tests/unit/test_state.py`
- [X] T027 [P] [US3] Add integration tests for edit, completion-status preservation, removal confirmation, cancellation, and empty-state return in `tests/integration/test_goal_flows.py`

### Implementation for User Story 3

- [X] T028 [US3] Implement validated goal update and removal state operations in `src/goal_tracker/state.py`
- [X] T029 [US3] Implement edit, update, and confirmed-removal routes with non-sensitive errors in `src/goal_tracker/app.py`
- [X] T030 [US3] Render edit controls, confirmation flow, cancellation behavior, and remove feedback in `src/goal_tracker/templates/index.html`
- [X] T031 [US3] Add edit and removal control states consistent with the shared interaction styles in `src/goal_tracker/static/styles.css`

**Checkpoint**: All specified user stories are independently functional and testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify constitution compliance and complete user-observable quality requirements.

- [X] T032 [P] Add restart/session-reset integration coverage proving no prior goals are available in `tests/integration/test_goal_flows.py`
- [X] T033 [P] Add accessibility assertions for labels, keyboard order, focus visibility, status text, and feedback association in `tests/integration/test_goal_flows.py`
- [X] T034 [P] Add performance coverage for 100 in-memory goals and measure request-to-render completion for create, complete, edit, and remove actions, verifying the 95th percentile is under one second in `tests/integration/test_goal_flows.py`
- [X] T035 [P] Add safe unexpected-error handling and non-sensitive response assertions in `src/goal_tracker/app.py` and `tests/integration/test_goal_flows.py`
- [X] T036 Run the complete automated suite and record the expected command in `quickstart.md`
- [X] T037 Run every manual validation scenario from `quickstart.md` and document any known limitation in `quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; creates the package and test environment.
- **Foundational (Phase 2)**: Depends on Setup; blocks all user story work.
- **User Story 1 (Phase 3)**: Depends on Foundational; delivers the MVP.
- **User Story 2 (Phase 4)**: Depends on Foundational and User Story 1 because it reuses the
  implemented goal list, model, and routes.
- **User Story 3 (Phase 5)**: Depends on Foundational and User Story 1 because it reuses the
  implemented goal representation and list.
- **Polish (Phase 6)**: Depends on the stories selected for delivery.

### User Story Dependencies

- **US1 (P1)**: No dependency on another user story after Foundational.
- **US2 (P1)**: Depends on US1's goal list and is independently testable once US1 is complete.
- **US3 (P2)**: Depends on US1's goal representation and list and is independently testable
  once US1 is complete.

### Requirement Coverage

- **FR-001, FR-003, FR-009**: T014-T019
- **FR-002**: T006, T008, T012, T015, T017
- **FR-004, FR-005**: T020-T025
- **FR-006, FR-007**: T026-T031
- **FR-008, SC-006**: T007, T032
- **FR-010**: T010-T011, T021, T024-T025, T033
- **FR-011, SC-002**: T034
- **SC-001, SC-003, SC-004, SC-005**: T015, T021, T027, T033, T034

### Parallel Opportunities

- T002-T005 can run in parallel after the directory structure exists.
- T008-T012 can run in parallel after the package and dependencies are available, except T013
  depends on the application factory and shared state interfaces.
- Within each story, its unit and integration test tasks can be prepared in parallel before
  implementation; template and stylesheet work can also proceed in parallel with route work.
- T032-T035 can run in parallel after the story implementation is complete.
- US2 and US3 can be assigned separately after US1 is complete, provided shared-file changes
  are coordinated.

## Parallel Example: User Story 1

```text
Task: "T014 [US1] Unit tests in tests/unit/test_state.py"
Task: "T015 [US1] Integration tests in tests/integration/test_goal_flows.py"
Task: "T018 [US1] Goal list rendering in src/goal_tracker/templates/index.html"
Task: "T019 [US1] Goal list styles in src/goal_tracker/static/styles.css"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational.
3. Complete Phase 3 User Story 1.
4. Run the US1 unit and integration tests and validate the create/list flow manually.
5. Stop for MVP review before adding completion, editing, or removal.

### Incremental Delivery

1. Add US2 completion behavior and verify mixed-status behavior.
2. Add US3 editing/removal behavior and verify confirmation and cancellation.
3. Complete Phase 6 cross-cutting validation for restart clearing, accessibility, errors, and
   performance.

## Notes

- Every task uses the required checkbox, sequential ID, optional parallel marker, story label
  for story tasks, and concrete file path format.
- Test tasks precede implementation tasks within each story so failures expose missing behavior.
- No task introduces a database, external persistence, or unvalidated input path.
