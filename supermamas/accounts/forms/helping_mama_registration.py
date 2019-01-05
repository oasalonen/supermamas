from wtforms.validators import InputRequired
from wtforms import (Form,
    StringField,
    TextAreaField)
from flask_babel import gettext
from re import split

from supermamas.accounts.forms.registration import UserRegistrationForm, AcceptanceBooleanField
from supermamas.common.forms.selectwithother import ListFormField, SelectWithOtherForm

class HelpingMamaRegistrationForm(UserRegistrationForm):
    good_to_know = StringField(
        gettext(u"Good to know"),
        description=gettext(u"Car or no car / job / parental leave /...")
        )

    speciality = StringField(
        gettext(u"Speciality"),
        description=gettext(u"If you can cook for a special diet, please let us know here (gluten free, lactose free, vegan, ...) ")
        )
    
    personal_experience = ListFormField(
        SelectWithOtherForm, 
        gettext(u"Personal experience"),
        description=gettext(u"A few details on your personal experience will help us connecting HelpingMamas with BubbleMamas with special needs (examples: how many children, lactation consultant, premature baby, miscarriage, postpartum depression, SIDS...)")
        )
    
    personal_message = TextAreaField(
        gettext(u"Feel free to tell us more about yourself"),
        )

    accept_contact_detail_sharing = AcceptanceBooleanField(description=gettext(u"Only the BubbleMamas you will be taking care of will receive your phone number, and you will receive her phone number as well."))

    accept_diversity = AcceptanceBooleanField(description=gettext(u"SuperMamas is like Berlin: international. SuperMamas is about mothers helping each other, regardless of cultural background. So it could happen that your BubbleMama doesn't speak very good German or English."))
    
    def __init__(self, city, formdata, **kwargs):
        super().__init__(city, formdata, **kwargs)

        self.personal_experience.options.choices = [
            ("Postpartum depression", gettext(u"Postpartum depression")), 
            ("Traumatic birth", gettext(u"Traumatic birth")), 
            ("Premature birth", gettext(u"Premature birth"))
        ]

    def get_personal_experience(self):
        other_experience = [x for x in split(",", self.personal_experience.other.data) if len(x) > 0]
        return self.personal_experience.options.data + other_experience