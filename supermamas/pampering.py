from flask import Blueprint, render_template, redirect, request, flash
from flask_babel import gettext
from supermamas import pamperings

bp = Blueprint("pampering", __name__)

@bp.route("/create_pampering", methods=("GET", "POST"))
def register():
    errors = {}

    if request.method == "POST":
        user, errors = pamperings.Service().create_pampering(request.form)
        if not errors:
            return redirect("/")
        else:
            flash(gettext(u"Fix all errors"))

    return render_template("create_pampering.html.j2", form_errors=errors, form_values=request.form)
