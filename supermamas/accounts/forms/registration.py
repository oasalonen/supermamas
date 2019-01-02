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
    BooleanField)
from wtforms.widgets import Input
from wtforms.validators import InputRequired
from flask_babel import gettext

from supermamas.common.forms.recaptcha import RecaptchaField
from supermamas.pamperings.pampering import PamperingType
from supermamas.common.forms import ListFormField, RadioWithOtherForm, SelectWithOtherForm, CalendarField

PASSWORD_REGEX = '''^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[(){}¤'"$@!%*?&])(?=.{8,})'''

class AcceptanceBooleanField(BooleanField):
    def __init__(self, label=None, validators=[], false_values=None, **kwargs):
        label = label or gettext(u"I understand and agree")
        validators.append(InputRequired(gettext(u"You must agree to this to sign up")))
        super(AcceptanceBooleanField, self).__init__(label, validators, **kwargs)

class BaseRegistrationForm(Form):
    email = StringField(gettext(u"Email"), [
        validators.Email(gettext(u"Please enter a valid email address")),
        validators.InputRequired(gettext(u"Please enter a valid email address"))
        ])
    password = PasswordField(gettext(u"Password"), [
        validators.Regexp(regex=PASSWORD_REGEX, message=gettext(u"Please enter a valid password")),
        validators.InputRequired(gettext(u"Please enter a valid password"))
        ])
    verify_password = PasswordField(gettext(u"Re-enter your password"), [validators.InputRequired(gettext(u"Re-enter your password"))])
    first_name = StringField(gettext(u"First name"), [validators.InputRequired(gettext(u"Please provide your first name"))])
    last_name = StringField(gettext(u"Last name"), [validators.InputRequired(gettext(u"Please provide your last name"))])
    district = SelectField(gettext(u"District"), [validators.InputRequired(gettext(u"Please select your district"))])

    def validate_verify_password(self, field):
        if (field.data != self.password.data):
            raise ValidationError(gettext(u"The re-entered password did not match the original"))
    
    def set_districts(self, districts):
        self.district.choices = [(district.id, district.name) for district in sorted(districts, key=lambda d: d.name)]


class UserRegistrationForm(BaseRegistrationForm):
    recaptcha = RecaptchaField()


class BubbleMamaRegistrationForm(UserRegistrationForm):
    pampering_type = RadioField(
        gettext(u"Type of pampering"), 
        [InputRequired(gettext(u"Please select the type of pampering you want"))],
        choices = [
            (PamperingType.PRE, gettext(u"Pre-pampering")),
            (PamperingType.STANDARD, gettext(u"Standard pampering")),
            (PamperingType.BELATED, gettext(u"Belated pampering")),
            (PamperingType.EMERGENCY, gettext(u"Emergency pampering")),
            (PamperingType.SUPPORT, gettext(u"Support for single mothers"))
        ])

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
    # TODO: validate that one of the following dates exist
    due_date = CalendarField(gettext(u"Expected due date"))

    pampering_start_date = CalendarField(
        gettext(u"Start of pampering"),
        description=gettext(u"Kindly keep in mind that we need 2 weeks notice for organizing your pampering."))

    baby_name = StringField(gettext(u"Your baby's name"))

    baby_birth_date = CalendarField(gettext(u"Your baby's date of birth"))

    pampering_days = ListFormField(
        RadioWithOtherForm, 
        gettext(u"Which days are suitable for welcoming your HelpingMamas?"), 
        description=gettext(u"Your pampering will lasts up to 3 weeks, with 1 to 3 visits per week, depending on the availability of the HelpingMamas from your neighborhood and the answer you give us in the next question. For your information: some HelpingMamas can only stop by during the week end.")
        )
    
    max_pamperings_per_week = SelectField(
        gettext("How many visits per week maximum shall we aim for you?"), 
        [InputRequired(gettext(u"Please let us know how many pamperings at most you would like per week"))], 
        choices=[("1", 1), ("2", 2), ("3", 3)], 
        coerce=int,
        description=gettext(u"With this question we want you to tell us the maximum amount of visits per week you would feel comfortable with. We will not plan more visits per week than you tell us to. Whether we are able to reach the weekly maximum depends on the availability of the HelpingMamas from your neighborhood.")
        )

    family_situation = StringField(
        gettext(u"What is your family situation?"), 
        [InputRequired(gettext(u"Please let us know your family situation"))],
        description=gettext(u"Single or living with partner/dad? If there are brothers and sisters, please indicate their age. Please specify if the number you indicate are adults and/or children (example: 2 adults. and 1 child 2 y.o.)")
        )

    food_allergies = StringField(
        gettext(u"Food allergies"), 
        [InputRequired(gettext(u"Please let us know if you have food allergies. If you have none, please just write 'None'"))]
        )

    diet_restrictions = StringField(
        gettext(u"Diet restrictions"), 
        [InputRequired(gettext(u"Please let us know if you have diet restrictions. If you have none, please just write 'None'"))],
        description=gettext(u"e.g. gluten-free, lactose-free, vegetarian, vegan")
        )

    languages = ListFormField(
        SelectWithOtherForm, 
        gettext(u"Which languages do you understand well?"),
        description=gettext(u"Multiple answers are very much allowed :-)")
        )

    personal_message = TextAreaField(
        gettext(u"Personal message to your HelpingMamas"), 
        [InputRequired(gettext(u"Please provide a personalized message"))],
        description=gettext(u"Tell us more about yourself and leave a message here that we can forward to your HelpingMamas.")
        )

    referrer = StringField(
        gettext(u"How did you hear about SuperMamas?"), 
        [InputRequired(gettext(u"Please fill this in"))],
        description=gettext(u"A friend / Facebook (which group?) / my midwife / ..."))

    accept_contact_detail_sharing = AcceptanceBooleanField(description=gettext(u"Only the HelpingMamas who will be part of your pampering will get your contact details, and you will receive their contact details as well."))
    
    accept_welcome_helping_mamas = AcceptanceBooleanField(description=gettext(u"We kindly ask you to welcome the HelpingMamas in your home (even for a very short time). They have prepared just for you a home cooked meal during their free time."))
    
    accept_notify_helping_mamas = AcceptanceBooleanField(description=gettext(u"We ask you to notify your HelpingMama if there is a change of schedule on your side, or if you wish to have less visits. It is important information in order to reorganize your pampering."))
    
    accept_thank_helping_mamas = AcceptanceBooleanField(description=gettext(u"We kindly ask you to say \"thank you\" to your HelpingMama: she donated her time just for you without expecting anything back in return."))
    
    accept_diversity = AcceptanceBooleanField(description=gettext(u"SuperMamas is like Berlin: international. SuperMamas is about mothers helping each other, regardless of cultural background. So it could happen that your HelpingMama doesn't speak German or English perfectly."))

    allow_helping_dads = RadioField(
        gettext(u"Helping Dads"),
        [InputRequired(gettext(u"Please select the type of pampering you want"))],
        choices=[
            ("yes", gettext(u"Wonderful yes!")),
            ("no", gettext(u"I do mind. Please only send HelpingMamas for me."))
        ],
        description=gettext(u"We have received spontaneous requests from dads who also would like to help. We find this idea wonderful: it is a great way to increase the amount of help for the BubbleMamas and the new dads can connect with the \"HelpingDads\" at the same time and also get support from them. If we send a HelpingDad to pamper you, we would ask him to arrange with you a visit at a time when your husband/partner is also at home. What do you think? Would you be open to receive help from HelpingDads?"))

    def __init__(self, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        super().__init__(formdata, obj, prefix, data, meta, **kwargs)

        self.pampering_days.options.validators = [InputRequired(gettext(u"Please let us know which days of the week suit you best for pamperings"))]
        self.pampering_days.options.choices = [
            ("all", gettext(u"All days of the week (including weekend)")),
            ("weekdays", gettext(u"Monday to Friday")),
        ]

        self.languages.options.validators = [InputRequired(gettext(u"Please select at least one language"))]
        self.languages.options.choices = [
            ("german", gettext(u"German")), 
            ("english", gettext(u"English")), 
            ("french", gettext(u"French")),
            ("polish", gettext(u"Polish")), 
            ("spanish", gettext(u"Spanish"))
        ]


class AdminRegistrationForm(BaseRegistrationForm):
    responsible_districts = SelectMultipleField(gettext(u"Responsible districts"))

    def set_districts(self, districts):
        super().set_districts(districts)
        self.responsible_districts.choices = self.district.choices