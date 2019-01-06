from wtforms.validators import InputRequired
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
from flask_babel import gettext
from re import split

from supermamas.accounts.forms.registration import UserRegistrationForm, AcceptanceBooleanField
from supermamas.pamperings import PamperingType
from supermamas.common.forms import ListFormField, RadioWithOtherForm, SelectWithOtherForm, CalendarField

def get_form_for_pampering_type(pampering_type, city, form):
    if pampering_type == PamperingType.PRE.value or pampering_type == PamperingType.STANDARD.value:
        return PreBirthRegistrationForm(city, pampering_type, form)
    elif (pampering_type == PamperingType.BELATED.value or 
        pampering_type == PamperingType.SUPPORT.value or
        pampering_type == PamperingType.EMERGENCY.value):
        return PostBirthRegistrationForm(city, pampering_type, form)
    else:
        raise Exception("Unknown pampering type {}", pampering_type)

class PamperingTypeForm(Form):
    city = HiddenField()

    pampering_type = SelectField(
        gettext(u"Type of pampering"), 
        [InputRequired(gettext(u"You must select a pampering type to continue"))],
        choices = [
            (PamperingType.STANDARD.value, gettext(u"Standard pampering")),
            (PamperingType.PRE.value, gettext(u"Pre-pampering")),
            (PamperingType.BELATED.value, gettext(u"Belated pampering")),
            (PamperingType.EMERGENCY.value, gettext(u"Emergency pampering")),
            (PamperingType.SUPPORT.value, gettext(u"Support for single mothers"))
        ])

    def __init__(self, city, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        super().__init__(formdata, obj, prefix, data, meta, **kwargs)
        if city:
            self.city.data = city

class BubbleMamaRegistrationForm(UserRegistrationForm):
    pampering_type = HiddenField()

    pampering_start_date = CalendarField(
        gettext(u"Start of pampering"),
        [InputRequired(gettext(u"Please provide a date"))],
        description=gettext(u"Kindly keep in mind that we need 2 weeks notice for organizing your pampering."))

    pampering_days = ListFormField(
        RadioWithOtherForm, 
        gettext(u"Which days are suitable for welcoming your HelpingMamas?"), 
        description=gettext(u"Your pampering will lasts up to 3 weeks, with 1 to 3 visits per week, depending on the availability of the HelpingMamas from your neighborhood and the answer you give us in the next question. For your information: some HelpingMamas can only stop by during the week end.")
        )
    
    max_pamperings_per_week = SelectField(
        gettext("How many visits per week maximum shall we aim for you?"), 
        [InputRequired(gettext(u"Please let us know how many pamperings at most you would like per week"))], 
        choices=[(1, 1), (2, 2), (3, 3)], 
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

    def __init__(self, city, pampering_type, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        super().__init__(city, formdata, obj, prefix, data, meta, **kwargs)

        if pampering_type:
            self.pampering_type.data = pampering_type

        self.pampering_days.form.set_required(True)
        self.pampering_days.flags.required = True
        self.pampering_days.options.choices = [
            ("All days", gettext(u"All days of the week (including weekend)")),
            ("Weekdays", gettext(u"Monday to Friday")),
            ("Other", gettext(u"Other"))
        ]

        self.languages.flags.required = True
        self.languages.options.choices = [
            ("German", gettext(u"German")), 
            ("English", gettext(u"English")), 
            ("French", gettext(u"French")),
            ("Polish", gettext(u"Polish")), 
            ("Spanish", gettext(u"Spanish"))
        ]

    def get_languages(self):
        other_languages = [x for x in split(",| ", self.languages.other.data) if len(x) > 0]
        return self.languages.options.data + other_languages

    def get_pampering_days(self):
        return self.pampering_days.other.data or self.pampering_days.options.data

class PreBirthRegistrationForm(BubbleMamaRegistrationForm):
    due_date = CalendarField(
        gettext(u"Expected due date"),
        [InputRequired(gettext(u"Please fill in this field"))])

class PostBirthRegistrationForm(BubbleMamaRegistrationForm):
    baby_name = StringField(
        gettext(u"Your baby's name"),
        [InputRequired(gettext(u"Please fill in this field"))])

    baby_birth_date = CalendarField(
        gettext(u"Your baby's date of birth"),
        [InputRequired(gettext(u"Please fill in this field"))])