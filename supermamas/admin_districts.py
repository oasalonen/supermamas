from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required
from flask_babel import gettext

from supermamas import districts

bp = Blueprint("admin_districts", __name__)

@bp.route("/admin/districts", methods=("GET", "POST"))
@login_required
def admin():
    errors = {}
    if request.method == "POST":
        district, errors = districts.Service().add_district(request.form["district_name"])
        if errors:
            flash(gettext(u"Fix all errors"))

    all_districts = districts.Service().districts()

    return render_template("districts.html.j2", districts=all_districts)

@bp.route("/admin/districts/<district_id>", methods=["DELETE"])
def delete(district_id):
    districts.Service().delete_district(district_id)
    all_districts = districts.Service().districts()

    return render_template("districts.html.j2", form_errors={}, form_values={}, districts=all_districts)
