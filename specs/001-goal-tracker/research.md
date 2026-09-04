# Research: Simple Goal Tracker

## Decision: Use a small Python web application

- **Decision**: Use Python 3.11+ with Flask and server-rendered HTML.
- **Rationale**: The repository has no existing application stack. Flask provides the smallest
  clear routing and rendering surface for a single-screen interactive tool, while keeping the
  runtime easy to validate locally.
- **Alternatives considered**: A command-line interface was rejected because the specification
  requires visual status distinction, accessible controls, and consistent user-facing feedback.
  A larger frontend framework was rejected because the feature has one primary screen and no
  need for client-side routing or a build pipeline.

## Decision: Keep state in process memory

- **Decision**: Store goals in an in-memory session-state service and initialize an empty state
  when the process starts.
- **Rationale**: This directly satisfies the requirement that the tool be purely stateless and
  never write to an external database. It also makes close/restart clearing behavior explicit
  and testable.
- **Alternatives considered**: A relational database, browser local storage, and file-backed
  persistence were rejected because each would retain data outside the active process/session.

## Decision: Validate every input structure with Pydantic

- **Decision**: Define Pydantic models for goal creation and updates, and validate them before
  state mutations or other processing.
- **Rationale**: This is a project constitution mandate. Centralized field constraints provide
  consistent rejection behavior for missing, whitespace-only, and overlong values.
- **Alternatives considered**: Handwritten checks alone were rejected because they could permit
  inconsistent validation paths and would violate the project constitution.

## Decision: Use pytest with unit and integration coverage

- **Decision**: Use pytest for model/state unit tests and Flask test-client integration tests.
- **Rationale**: The split keeps boundary and state-transition tests fast while proving complete
  create, complete, edit, remove, validation, and restart flows through the user interface.
  Dedicated tests will cover the exact boundary where registered items equal a capacity-like
  limit as required by the constitution; for this feature the analogous boundary tests cover
  empty state and maximum field lengths.
- **Alternatives considered**: Manual-only verification was rejected because the constitution
  requires automated tests for new behavior and deterministic edge-case coverage.

## Decision: Set a bounded performance target

- **Decision**: Measure action completion and visible feedback, targeting the specified 95th
  percentile within one second for normal sessions of at least 100 goals.
- **Rationale**: In-memory state and a single screen make this target practical without adding
  caching or asynchronous infrastructure. The target is user-observable and aligns with the
  specification's success criteria.
- **Alternatives considered**: A throughput-only server benchmark was rejected because the
  feature's primary risk is interaction responsiveness, not multi-user request volume.
