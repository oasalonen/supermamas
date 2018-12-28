from wtforms import Form, StringField, PasswordField, validators, BooleanField
from flask_babel import gettext

class LoginForm(Form):
    email = StringField(gettext(u"Email"), [validators.InputRequired(gettext(u"Please enter an email"))])
    password = PasswordField(gettext(u"Password"), [validators.InputRequired(gettext(u"Please enter a password"))])
    remember_me = BooleanField(gettext(u"Remember me"))