from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_babel import gettext
from flask_login import login_required
from dateutil import rrule, parser
from datetime import datetime, date

from supermamas.pamperings import PamperingService
from supermamas.pamperings.forms import (
    PamperingFilterForm, 
    CreatePamperingForm,
    PamperingInvitationForm)
from supermamas.common.router_utils import admin_only
from supermamas.common import ConfigurationService
from supermamas.pamperings.viewmodels import PamperingListViewModel
from supermamas.accounts import AccountsService

bp = Blueprint("pamperings", __name__)

@bp.route("/pamperings", methods=["GET", "POST"])
@login_required
@admin_only
def view_pamperings():
    form = PamperingFilterForm()

    viewmodel = PamperingListViewModel()
    viewmodel.set_pamperings(PamperingService().get_all_pamperings())

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
    bubble_mama_id = request.args.get("bubble_mama")
    form = CreatePamperingForm(request.form)

    if request.method == "POST":
        if not request.form.get("refresh_dates"):
            pampering = PamperingService().create_pampering(bubble_mama_id, form)
            if pampering:
                return redirect(url_for("pamperings.invite", pampering_id=pampering.id))
            else:
                flash(gettext(u"Something went wrong during pampering creation"))
    elif request.method == "GET":
        form.set_bubble_mama(AccountsService().get_bubble_mama(bubble_mama_id))

    return render_template(
        "pamperings/create.html.j2",
        form=form)

@bp.route("/pamperings/<pampering_id>/invite", methods=("GET", "POST"))
@login_required
@admin_only
def invite(pampering_id):
    form = PamperingInvitationForm(request.form)

    if request.method == "POST":
        PamperingService().send_pampering_invitation(pampering_id, form)
        return redirect("/")
    elif request.method == "GET":
        pampering = PamperingService().get_pampering(pampering_id)
        if not pampering:
            raise Exception(F"No such pampering {pampering_id}")
        form.initialize_fields(ConfigurationService().get("MAIL_SENDER"), pampering)
    else:
        raise Exception(F"Unhandled method {request.method}")

    return render_template(
        "pamperings/invite.html.j2",
        form=form)

@bp.route("/pamperings/signup", methods=("GET", "POST"))
@login_required
def signup():
    errors = {}
    pampering_id = request.args.get("pampering")
    helping_mama_id = request.args.get("user")
    max_visits = request.form.get("max_visits")

    if request.method == "POST":
        signup, errors = PamperingService().add_signup(pampering_id, helping_mama_id, request.form.getlist("availabilities[]"), max_visits)
        if not errors:
            return redirect("/")
        else:
            flash(gettext(u"Fix all errors"))
            pampering_plan = request.form
    else:
        pampering_plan = PamperingService().prepare_signup(pampering_id, helping_mama_id)    

    return render_template("signup_pampering.html.j2", form_errors=errors, form_values=pampering_plan)
    
@bp.route("/pamperings/finalize", methods=("GET", "POST"))
@login_required
@admin_only
def finalize():
    return None
    #return render_template("finalize_pampering.html.j2", form_errors=errors, form_values=pampering_plan)