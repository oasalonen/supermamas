from flask import Blueprint, render_template, redirect, request, flash
from flask_babel import gettext
from dateutil import rrule
from datetime import datetime

from supermamas import pamperings

bp = Blueprint("pampering", __name__)

@bp.route("/create_pampering", methods=("GET", "POST"))
def register():
    errors = {}
    bubble_mama_id = request.args.get("bubble_mama_id")
    start_date = None
    end_date = None

    if request.method == "POST":
        if request.form["refresh_dates"]:
            start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
        else:
            user, errors = pamperings.Service().create_pampering(bubble_mama_id, request.form.getlist("date_range[]"))
            if not errors:
                return redirect("/")
            else:
                flash(gettext(u"Fix all errors"))

    pampering_plan = pamperings.Service().prepare_pampering(bubble_mama_id, start_date, end_date)
    return render_template("create_pampering.html.j2", form_errors=errors, form_values=pampering_plan)
