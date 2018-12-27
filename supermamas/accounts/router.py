from flask import Blueprint, render_template, redirect, request, flash, Response
from flask_babel import gettext
from flask_login import logout_user, login_required, login_user
from supermamas import accounts
from supermamas.accounts.forms.login import LoginForm
from supermamas.accounts.forms.registration import RegistrationForm

bp = Blueprint("accounts", __name__)

@bp.errorhandler(401)
def page_not_found(e):
    return Response("<p>" + gettext(u"Login failed") + "</p>")

@bp.route("/register", methods=("GET", "POST"))
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        user = accounts.AuthenticationService().register(
            form.email.data,
            form.password.data,
            form.first_name.data,
            form.last_name.data
            )
        if user:
            return redirect("/")
        else:
            flash(gettext(u"We could not register your account. Have you already signed up with this email?"))

    return render_template("register.html.j2", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = accounts.AuthenticationService().authenticate(form.email.data, form.password.data)
        if user:
            login_user(user)
            flash(gettext(u"Logged in as %(name)s", name=user.first_name))

            url = request.args.get("next")
            return redirect(url if url else "/")
        else:
            flash(gettext(u"Invalid login credentials"))

    return render_template("login.html.j2", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
