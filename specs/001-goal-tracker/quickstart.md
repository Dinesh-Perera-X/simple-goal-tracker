# Quickstart: Simple Goal Tracker

## Prerequisites

- Python 3.11 or newer
- Internet access only if dependencies need to be installed; the feature itself requires no
  external service or database

## Setup

From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
PYTHONPATH=src python -m goal_tracker.app
```

Open the displayed local URL in a browser.

## Manual Validation

1. Submit a title and optional description; confirm a new incomplete goal appears.
2. Submit an empty or whitespace-only title; confirm the goal is rejected with field feedback.
3. Complete one goal; confirm its text status changes and other goals are unchanged.
4. Edit a goal; confirm content changes while completion status remains unchanged.
5. Start removal and cancel; confirm the goal remains. Confirm removal; confirm it disappears.
6. Close and restart the process; confirm the prior goals are absent.
7. Repeat the primary actions using only the keyboard and verify status/feedback is available
   without relying on color alone.

## Automated Validation

```bash
pytest
```

The suite must include model and state unit tests for whitespace, length limits, duplicate
 titles, empty-state transitions, idempotent completion, and invalid updates. Integration tests
must cover the complete create, complete, edit, remove, validation, accessibility-label, and
restart flows. Performance tests must verify the one-second action target with at least 100
in-memory goals.
