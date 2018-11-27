from flask import Blueprint, render_template, redirect, request, flash
from flask_babel import gettext

bp = Blueprint("auth", __name__)

@bp.route("/register", methods=("GET", "POST"))
def register():
    errors = {}

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        if not first_name:
            errors["first_name"] = gettext(u"First name is missing")
        if not last_name:
            errors["last_name"] = gettext(u"Last name is missing")
        
        if not errors:
            return redirect("/")
        else:
            flash(gettext(u"Fix all errors"))

    return render_template("register.html.j2", form_errors=errors, form_values=request.form)

@bp.route("/login")
def login():
    return render_template("login.html.j2")
