from flask import Blueprint, render_template, redirect, request, flash
from flask_babel import gettext
from flask_login import login_required
from dateutil import rrule, parser
from datetime import datetime, date

from supermamas import pamperings
from supermamas.pamperings.forms import PamperingFilterForm
from supermamas.common.router_utils import admin_only
from supermamas.pamperings.viewmodels import PamperingListViewModel

bp = Blueprint("pamperings", __name__)

@bp.route("/pamperings", methods=["GET", "POST"])
@login_required
@admin_only
def view_pamperings():
    form = PamperingFilterForm()

    viewmodel = PamperingListViewModel()
    viewmodel.set_pamperings(pamperings.Service().get_all_pamperings())

    return render_template("view_pamperings.html.j2", form=form, viewmodel=viewmodel)

@bp.route("/pamperings/<id>", methods=["GET"])
@login_required
@admin_only
def get_details(id):
    redirect("/")

@bp.route("/pamperings/create", methods=("GET", "POST"))
@login_required
@admin_only
def create():
    errors = {}
    bubble_mama_id = request.args.get("bubble_mama")
    start_date = None
    end_date = None

    if request.method == "POST":
        if request.form.get("refresh_dates"):
            start_date = parser.parse(request.form["start_date"]).date()
            end_date = parser.parse(request.form["end_date"]).date()
        else:
            pampering, errors = pamperings.Service().create_pampering(bubble_mama_id, request.form.getlist("date_range[]"))
            if not errors:
                return redirect("/")
            else:
                flash(gettext(u"Fix all errors"))

    pampering_plan = pamperings.Service().prepare_pampering(bubble_mama_id, start_date, end_date)
    return render_template("create_pampering.html.j2", form_errors=errors, form_values=pampering_plan)

@bp.route("/pamperings/signup", methods=("GET", "POST"))
@login_required
def signup():
    errors = {}
    pampering_id = request.args.get("pampering")
    helping_mama_id = request.args.get("user")
    max_visits = request.form.get("max_visits")

    if request.method == "POST":
        signup, errors = pamperings.Service().add_signup(pampering_id, helping_mama_id, request.form.getlist("availabilities[]"), max_visits)
        if not errors:
            return redirect("/")
        else:
            flash(gettext(u"Fix all errors"))
            pampering_plan = request.form
    else:
        pampering_plan = pamperings.Service().prepare_signup(pampering_id, helping_mama_id)    

    return render_template("signup_pampering.html.j2", form_errors=errors, form_values=pampering_plan)
    
@bp.route("/pamperings/finalize", methods=("GET", "POST"))
@login_required
@admin_only
def finalize():
    return None
    #return render_template("finalize_pampering.html.j2", form_errors=errors, form_values=pampering_plan)