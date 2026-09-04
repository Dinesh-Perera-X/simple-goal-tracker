from flask import Flask, flash, redirect, render_template, request, url_for
from pydantic import ValidationError

from .models import GoalCreate, GoalUpdate
from .state import GoalNotFound, GoalStore
from .validation import validation_message


def create_app(store: GoalStore | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "goal-tracker-local"
    app.extensions["goal_store"] = store or GoalStore()

    def render_home(message: str | None = None, status: int = 200):
        goals = app.extensions["goal_store"].list()
        return render_template("index.html", goals=goals, message=message), status

    @app.get("/")
    def index():
        return render_home()

    @app.post("/goals")
    def create_goal():
        try:
            payload = GoalCreate(
                title=request.form.get("title", ""),
                description=request.form.get("description", ""),
            )
            app.extensions["goal_store"].create(payload)
        except ValidationError as error:
            return render_home(validation_message(error), 400)
        except Exception:
            return render_home("Something went wrong. Please try again.", 500)
        flash("Goal added.")
        return redirect(url_for("index"))

    @app.post("/goals/<goal_id>/complete")
    def complete_goal(goal_id: str):
        try:
            app.extensions["goal_store"].complete(goal_id)
        except GoalNotFound:
            return render_home("That goal could not be found.", 404)
        except Exception:
            return render_home("Something went wrong. Please try again.", 500)
        flash("Goal completed.")
        return redirect(url_for("index"))

    @app.post("/goals/<goal_id>/edit")
    def edit_goal(goal_id: str):
        try:
            payload = GoalUpdate(
                title=request.form.get("title"),
                description=request.form.get("description"),
            )
            app.extensions["goal_store"].update(goal_id, payload)
        except ValidationError as error:
            return render_home(validation_message(error), 400)
        except GoalNotFound:
            return render_home("That goal could not be found.", 404)
        except Exception:
            return render_home("Something went wrong. Please try again.", 500)
        flash("Goal updated.")
        return redirect(url_for("index"))

    @app.post("/goals/<goal_id>/remove")
    def remove_goal(goal_id: str):
        if request.form.get("confirm") != "yes":
            flash("Removal canceled.")
            return redirect(url_for("index"))
        try:
            app.extensions["goal_store"].remove(goal_id)
        except GoalNotFound:
            return render_home("That goal could not be found.", 404)
        except Exception:
            return render_home("Something went wrong. Please try again.", 500)
        flash("Goal removed.")
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
