# Implementation Plan: Simple Goal Tracker

**Branch**: `001-goal-tracker` | **Date**: 2026-09-03 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-goal-tracker/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Deliver a single-user goal tracker that creates, lists, completes, edits, and removes goals
during one open session. The implementation will use a small Python web application with
in-memory state, Pydantic validation at every input boundary, accessible HTML controls, and
focused automated tests. No external database or persistence layer will be introduced.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+

**Primary Dependencies**: Flask for local HTTP routing and rendering; Pydantic for input
validation; pytest for automated tests

**Storage**: In-memory session state only; no external database, file persistence, or cache

**Testing**: pytest unit tests for models and state transitions; Flask test-client integration
tests for user flows and validation responses

**Target Platform**: Linux-compatible local web runtime; current desktop and mobile browsers

**Project Type**: Single-project web application

**Performance Goals**: 95% of create, complete, edit, and remove actions complete with visible
feedback within one second during normal use; support at least 100 goals in one session

**Constraints**: Stateless process; no external database writes; validate all input structures
with Pydantic before processing; keyboard and assistive-technology access; title max 200
characters; description max 2,000 characters

**Scale/Scope**: One user and one active session per running process; one primary screen;
create, view, complete, edit, and remove goals only; no accounts, sharing, reminders, or
long-term persistence

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*GATE: PASS*

- Code quality: the design uses one small application and separates validation, session state,
  and presentation responsibilities.
- Testing: each behavior has unit or integration coverage, including whitespace, invalid
  input, duplicate titles, already-completed goals, and exact empty-state transitions.
- User experience: all actions use consistent labels, status feedback, confirmation behavior,
  semantic controls, and keyboard-accessible flows.
- Performance and reliability: in-memory operations avoid database latency; tests measure the
  one-second action target and verify safe validation failures.
- Statelessness and validation: session state is process-local and every incoming structure
  is parsed by Pydantic before business logic runs.
- Documentation and contracts: the data model, UI behavior, and runnable validation steps are
  documented in the Phase 1 artifacts.

*Post-design recheck: PASS.* The design keeps all state in memory, validates inputs with
Pydantic before mutation, defines deterministic unit and integration coverage for edge cases,
documents accessible and consistent interaction behavior, and preserves the one-second
feedback target without introducing an external database or unnecessary infrastructure.

## Project Structure

### Documentation (this feature)

```text
specs/001-goal-tracker/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
├── goal_tracker/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── state.py
│   ├── validation.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── styles.css
tests/
├── unit/
│   ├── test_models.py
│   └── test_state.py
└── integration/
  └── test_goal_flows.py
```

**Structure Decision**: Use one Python package under `src/goal_tracker` with an application
entry point, Pydantic models, an in-memory state service, and server-rendered presentation.
Tests are split by responsibility so model/state edge cases remain fast and focused while
the integration suite verifies complete user flows through the web interface.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | The design satisfies the constitution without exceptions. |
