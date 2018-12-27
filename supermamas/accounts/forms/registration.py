from wtforms import Form, StringField, PasswordField, validators, ValidationError
from flask_babel import gettext

password_regex = '''^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[(){}¤'"$@!%*?&])(?=.{8,})'''

class RegistrationForm(Form):
    email = StringField(gettext(u"Email"), [validators.Email(gettext(u"Please enter a valid email address"))])
    password = PasswordField(gettext(u"Password"), [validators.Regexp(regex=password_regex, message=gettext(u"Please enter a valid password"))])
    verify_password = PasswordField(gettext(u"Re-enter password"))
    first_name = StringField(gettext(u"First name"), [validators.InputRequired(gettext(u"Please provide your first name"))])
    last_name = StringField(gettext(u"Last name"), [validators.InputRequired(gettext(u"Please provide your last name"))])

    def validate_verify_password(self, field):
        if (field.data != self.password.data):
            raise ValidationError(gettext(u"The re-entered password did not match the original"))