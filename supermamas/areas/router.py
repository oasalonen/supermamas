from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required
from flask_babel import gettext

from supermamas.areas import AreaService
from supermamas.common.router_utils import admin_only

bp = Blueprint("districts", __name__)

@bp.route("/districts", methods=("GET", "POST"))
@login_required
@admin_only
def admin():
    errors = {}
    if request.method == "POST":
        district, errors = AreaService().add_district(request.form["district_name"])
        if errors:
            flash(gettext(u"Fix all errors"))

    all_districts = AreaService().districts()

    return render_template("districts.html.j2", districts=all_districts)

@bp.route("/districts/<district_id>", methods=["DELETE"])
@login_required
@admin_only
def delete(district_id):
    AreaService().delete_district(district_id)
    all_districts = AreaService().districts()

    return render_template("districts.html.j2", form_errors={}, form_values={}, districts=all_districts)
