from flask import Blueprint, render_template, redirect, request, flash
from flask_babel import gettext
from supermamas import accounts

bp = Blueprint("auth", __name__)

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

@bp.route("/login")
def login():
    return render_template("login.html.j2")
