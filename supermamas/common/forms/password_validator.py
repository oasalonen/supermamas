from wtforms import ValidationError
from wtforms.validators import Regexp
from flask_babel import gettext
from re import compile
from functools import reduce

PASSWORD_REGEX = '''^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[(){}¤'"$@!%*?&])(?=.{8,})'''
REGEX_GROUPS = [
    (compile('''(?=.*[a-z])'''), gettext(u"The password is missing a lowercase letter (e.g. 'a').")),
    (compile('''(?=.*[A-Z])'''), gettext(u"The password is missing an uppercase letter (e.g. 'A').")),
    (compile('''(?=.*\d)'''), gettext(u"The password is missing a digit (e.g. '5').")),
    (compile('''(?=.*[(){}¤'"$@!%*?&])'''), gettext(u"The password is missing a special character, (e.g. '( ) { } ¤ \" $ @ ! % * ? &').")),
    (compile('''(?=.{8,})'''), gettext(u"The password is less than 8 characters long."))
]

class PasswordValidator(Regexp):

    def __init__(self):
        super().__init__(regex=PASSWORD_REGEX, message=gettext(u"Please enter a valid password"))

    def __call__(self, form, field, message=None):
        try:
            super().__call__(form, field, message)
        except ValidationError:
            errors = [match[1] for match in [(regex[0].match(field.data or ''), regex[1]) for regex in REGEX_GROUPS] if not match[0]]
            error_list = [f"<li>{error}</li>" for error in errors]
            error_message = ["<ul>{message}".format(message=gettext(u"The password is invalid because:"))] + error_list + ["</ul>"]
            error_message = "".join(error_message)
            raise ValidationError(error_message)

