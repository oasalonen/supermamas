from flask import Blueprint, render_template

bp = Blueprint("auth", __name__)

@bp.route("/register")
def register():
    return render_template("register.html.j2")

@bp.route("/login")
def login():
    return render_template("login.html.j2")
