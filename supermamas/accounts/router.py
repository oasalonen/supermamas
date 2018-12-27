from flask import Blueprint, render_template, redirect, request, flash, Response
from flask_babel import gettext
from flask_login import logout_user, login_required, login_user
from supermamas import accounts
from supermamas.accounts.forms.login import LoginForm

bp = Blueprint("accounts", __name__)

@bp.errorhandler(401)
def page_not_found(e):
    return Response("<p>" + gettext(u"Login failed") + "</p>")

@bp.route("/register", methods=("GET", "POST"))
def register():
    errors = {}

    if request.method == "POST":
        registration_service = accounts.RegistrationService()
        user, errors = registration_service.register_bubble_mama(request.form)
        if not errors:
            return redirect("/")
        else:
            flash(gettext(u"Fix all errors"))

    return render_template("register.html.j2", form_errors=errors, form_values=request.form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = accounts.AuthenticationService().authenticate(form.email.data, form.password.data)
        if user:
            login_user(user)
            flash(gettext(u"Logged in as %(name)s", name=user.first_name))
            return redirect("/")
        else:
            flash(gettext(u"Invalid login credentials"))

    return render_template("login.html.j2", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
