from wtforms import (Form, 
    Field,
    StringField, 
    PasswordField, 
    validators,
    ValidationError, 
    SelectField, 
    SelectMultipleField, 
    RadioField,
    TextAreaField,
    FormField,
    BooleanField,
    HiddenField,
    IntegerField)
from wtforms.widgets import Input
from wtforms.validators import InputRequired, Email, Regexp
from flask_babel import gettext

from supermamas.common.forms.recaptcha import RecaptchaField
from supermamas.common.forms import PasswordValidator
from supermamas.areas import AreaService

class AcceptanceBooleanField(BooleanField):
    def __init__(self, label=None, validators=[], false_values=None, **kwargs):
        label = label or gettext(u"I understand and agree")
        validators.append(InputRequired(gettext(u"You must agree to this to sign up")))
        super(AcceptanceBooleanField, self).__init__(label, validators, **kwargs)

class CityForm(Form):
    city = SelectField(
        gettext(u"City"), 
        [InputRequired(gettext(u"Please select your city"))],
        choices = [(city.id, city.name) for city in AreaService().cities()])
    
class BaseRegistrationForm(Form):
    email = StringField(
        gettext(u"Email"), [
        Email(gettext(u"Please enter a valid email address")),
        InputRequired(gettext(u"Please enter a valid email address"))
        ])

    password = PasswordField(
        gettext(u"Password"), 
        [PasswordValidator(), InputRequired(gettext(u"Please enter a valid password"))],
        description=gettext(u"A valid password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one number, and one special character.")
        )

    verify_password = PasswordField(
        gettext(u"Re-enter your password"), 
        [InputRequired(gettext(u"Re-enter your password"))],
        description=gettext(u"Type your password again exactly as before to make sure it's correct.")
        )

    first_name = StringField(gettext(u"First name"), [InputRequired(gettext(u"Please provide your first name"))])
    last_name = StringField(gettext(u"Last name"), [InputRequired(gettext(u"Please provide your last name"))])
    district = SelectField(gettext(u"District"), [InputRequired(gettext(u"Please select your district"))])
    city = HiddenField()

    def validate_verify_password(self, field):
        if (field.data != self.password.data):
            raise ValidationError(gettext(u"The re-entered password did not match the original"))

    def __init__(self, city, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        super().__init__(formdata, obj, prefix, data, meta, **kwargs)

        if city:
            self.city.data = city

        districts = AreaService().get_city(city).districts
        self.district.choices = [(district.id, district.name) for district in sorted(districts, key=lambda d: d.name)]


class UserRegistrationForm(BaseRegistrationForm):
    recaptcha = RecaptchaField()

    address_line1 = StringField(
        gettext(u"Street address"), 
        [InputRequired(gettext(u"Please provide your street address"))])

    address_line2 = StringField(gettext(u"Address line 2"))

    postal_code = StringField(
        gettext(u"Postal code"), 
        [InputRequired(gettext(u"Please provide your postal code"))])

    phone_number = StringField(
        gettext(u"Phone number"), 
        [InputRequired(gettext(u"Please provide your phone number"))])

    referrer = StringField(
        gettext(u"How did you hear about SuperMamas?"), 
        [InputRequired(gettext(u"Please fill this in"))],
        description=gettext(u"A friend / Facebook (which group?) / my midwife / ..."))

    def __init__(self, city, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        super().__init__(city, formdata, obj, prefix, data, meta, **kwargs)

class AdminRegistrationForm(BaseRegistrationForm):
    responsible_districts = SelectMultipleField(gettext(u"Responsible districts"))

    def __init__(self, city, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        super().__init__(city, formdata, obj, prefix, data, meta, **kwargs)
        self.responsible_districts.choices = self.district.choices