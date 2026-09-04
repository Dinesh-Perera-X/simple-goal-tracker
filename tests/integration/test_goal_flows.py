def test_empty_state_and_create_flow(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"No goals yet" in response.data

    response = client.post("/goals", data={"title": "  Read more  ", "description": "Books"})
    assert response.status_code == 302

    page = client.get(response.headers["Location"])
    assert b"Read more" in page.data
    assert b"Incomplete" in page.data
    assert b"Books" in page.data
    assert b"Goal added" in page.data


def test_invalid_create_shows_feedback_without_mutation(client):
    response = client.post("/goals", data={"title": "   "})

    assert response.status_code == 400
    assert b"Title" in response.data
    assert b"No goals yet" in response.data


def test_completion_updates_only_selected_goal(client):
    first = client.post("/goals", data={"title": "Read"})
    first_page = client.get(first.headers["Location"])
    first_id = first_page.get_data(as_text=True).split('data-goal-id="')[1].split('"')[0]
    client.post("/goals", data={"title": "Run"})

    response = client.post(f"/goals/{first_id}/complete")
    page = client.get(response.headers["Location"])
    body = page.get_data(as_text=True)

    assert b"Completed" in page.data
    assert body.count("Incomplete") == 1


def test_edit_remove_cancel_and_confirm(client):
    created = client.post("/goals", data={"title": "Read"})
    page = client.get(created.headers["Location"])
    goal_id = page.get_data(as_text=True).split('data-goal-id="')[1].split('"')[0]

    response = client.post(f"/goals/{goal_id}/edit", data={"title": "Study"})
    assert response.status_code == 302
    assert b"Study" in client.get(response.headers["Location"]).data

    cancel = client.post(f"/goals/{goal_id}/remove", data={"confirm": "no"})
    assert cancel.status_code == 302
    assert b"Study" in client.get(cancel.headers["Location"]).data

    removed = client.post(f"/goals/{goal_id}/remove", data={"confirm": "yes"})
    assert removed.status_code == 302
    assert b"No goals yet" in client.get(removed.headers["Location"]).data


def test_restart_uses_fresh_store(client, store):
    client.post("/goals", data={"title": "Temporary"})
    fresh_client = client.application.test_client()
    fresh_client.application.extensions["goal_store"] = type(store)()

    assert b"Temporary" not in fresh_client.get("/").data


def test_accessible_labels_and_text_status(client):
    body = client.get("/").get_data(as_text=True)

    assert 'aria-live="polite"' in body
    assert 'for="title"' in body
    assert 'aria-label="Goal title"' in body
    assert 'aria-label="Goal description"' in body


def test_performance_for_100_goals(client, store):
    from statistics import quantiles
    from time import perf_counter

    action_durations = []
    for index in range(100):
        started = perf_counter()
        client.post("/goals", data={"title": f"Goal {index}"})
        action_durations.append(perf_counter() - started)

    response = client.get("/")
    assert response.status_code == 200
    assert response.data.count(b"goal-card") == 100
    assert quantiles(action_durations, n=100)[94] < 1.0


def test_unexpected_errors_are_non_sensitive(client, monkeypatch):
    def fail(_):
        raise RuntimeError("/secret/internal/path")

    monkeypatch.setattr(client.application.extensions["goal_store"], "create", fail)
    response = client.post("/goals", data={"title": "Read"})

    assert response.status_code == 500
    assert b"Something went wrong" in response.data
    assert b"secret/internal/path" not in response.data
