from flask import Blueprint, render_template, redirect, request, flash, Response, session, url_for
from flask_babel import gettext
from flask_login import logout_user, login_required, login_user, current_user
from supermamas import accounts
from supermamas.areas import AreaService
from supermamas.common.router_utils import is_safe_url, admin_only
from supermamas.accounts.forms.login import LoginForm
from supermamas.accounts.forms.registration import (
    BubbleMamaRegistrationForm, 
    AdminRegistrationForm, 
    CityForm,
    PamperingTypeForm)
from supermamas.accounts.viewmodels import BubbleMamaRegistrationBreadcrumbs

bp = Blueprint("accounts", __name__)

@bp.errorhandler(401)
def page_not_found(e):
    return Response("<p>" + gettext(u"Login failed") + "</p>")

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = accounts.AuthenticationService().authenticate(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            flash(gettext(u"Logged in as %(name)s", name=user.first_name))

            url = request.args.get("next")
            url = url if url and is_safe_url(url) else "/"
            return redirect(url)
        else:
            flash(gettext(u"Invalid login credentials"))

    return render_template("login.html.j2", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@bp.route("/accounts/registration/bubble_mama/intro")
def register_bubble_mama_intro():
    breadcrumbs = BubbleMamaRegistrationBreadcrumbs(BubbleMamaRegistrationBreadcrumbs.Step.INTRODUCTION, None, None)
    return render_template("accounts/registration/bubble_mama_intro.html.j2", breadcrumbs=breadcrumbs)

@bp.route("/accounts/registration/bubble_mama/city", methods=["GET", "POST"])
def register_bubble_mama_city():
    form = CityForm(request.form)

    if request.method == "POST" and form.validate():
        return redirect(url_for("accounts.register_bubble_mama_pampering_type", city=form.city.data))

    breadcrumbs = BubbleMamaRegistrationBreadcrumbs(BubbleMamaRegistrationBreadcrumbs.Step.CITY, None, None)
    return render_template("accounts/registration/bubble_mama_city.html.j2", form=form, breadcrumbs=breadcrumbs)

@bp.route("/accounts/registration/bubble_mama/pampering_type", methods=["GET", "POST"])
def register_bubble_mama_pampering_type():
    form = PamperingTypeForm(request.args.get("city"), request.form)

    if request.method == "POST" and form.validate():
        return redirect(url_for(
            "accounts.register_bubble_mama_profile", 
            city=form.city.data, 
            pampering_type=form.pampering_type.data))

    breadcrumbs = BubbleMamaRegistrationBreadcrumbs(BubbleMamaRegistrationBreadcrumbs.Step.PAMPERING_TYPE, form.city.data, None)
    return render_template("accounts/registration/bubble_mama_pampering_type.html.j2", form=form, breadcrumbs=breadcrumbs)

@bp.route("/accounts/registration/bubble_mama/profile", methods=("GET", "POST"))
def register_bubble_mama_profile():
    form = BubbleMamaRegistrationForm(request.args.get("city"), request.args.get("pampering_type"), request.form)
    form.set_districts(AreaService().districts())

    if request.method == "POST" and form.validate():
        user = accounts.RegistrationService().register(
            form.email.data,
            form.password.data,
            form.first_name.data,
            form.last_name.data,
            form.district.data
            )
        if user:
            return redirect("/")
        else:
            flash(gettext(u"We could not register your account. Have you already signed up with this email?"))

    breadcrumbs = BubbleMamaRegistrationBreadcrumbs(
        BubbleMamaRegistrationBreadcrumbs.Step.PROFILE, 
        form.city.data, 
        form.pampering_type.data)
    return render_template("accounts/registration/bubble_mama_profile.html.j2", form=form, breadcrumbs=breadcrumbs)

@bp.route("/accounts/registration/admin", methods=["GET", "POST"])
@login_required
@admin_only
def register_admin():
    form = AdminRegistrationForm(request.form)
    form.set_districts(AreaService().districts())

    if request.method == "POST" and form.validate():
        user = accounts.RegistrationService().register_admin(
            form.email.data,
            form.password.data,
            form.first_name.data,
            form.last_name.data,
            form.district.data,
            form.responsible_districts.data
            )
        if user:
            return redirect("/")
        else:
            flash(gettext(u"Something went wrong with the account registration."))
    
    return render_template("register_admin.html.j2", form=form)

# Need to do a GET to avoid a creating a form in the activation email
@bp.route("/accounts/<user_id>/activation", methods=["GET"])
def activate_user(user_id):
    code = request.args.get("code")
    accounts.RegistrationService().activate_user(user_id, code)
    flash(gettext(u"Your account has been successfully activated. You may now log in to your account."))
    return redirect(url_for("accounts.login"))