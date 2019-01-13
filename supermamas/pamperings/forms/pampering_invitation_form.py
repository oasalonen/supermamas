from wtforms import Form, StringField, TextAreaField, SelectMultipleField
from wtforms.validators import Email, InputRequired
from flask_babel import gettext
from re import split

from supermamas.common import TemplateRenderer, ConfigurationService
from supermamas.areas import AreaService

class PamperingInvitationForm(Form):

    sender = StringField(
        gettext(u"Sender"), [
        Email(gettext(u"Please enter a valid email address")),
        InputRequired(gettext(u"Please fill this field"))
        ])

    districts = SelectMultipleField(
        gettext(u"Send to districts"),
        description=gettext(u"The email will be sent to each HelpingMama in a selected district.")
    )

    additional_recipients = TextAreaField(
        gettext(u"Additional recipients"), 
        description=gettext(u"Email addresses of additional HelpingMamas who should receive the pampering invitation. Separate each e-mail address by a space or comma.")
        )

    subject = StringField(
        gettext(u"Subject"),
        [InputRequired(gettext(u"Please fill this field"))]
        )

    message = TextAreaField(
        gettext(u"Message"),
        [InputRequired(gettext(u"Please fill this field"))]
        )

    def __init__(self, formdata=None, **kwargs):
        super().__init__(formdata, **kwargs)

    def initialize_fields(self, sender=None, pampering=None):
        if sender:
            self.sender.data = sender

        if pampering:
            self.initialize_subject(pampering)
            self.initialize_districts(pampering)
            self.initialize_message(pampering)

    def initialize_subject(self, pampering):
        name = pampering.bubble_mama_info.name
        district = pampering.district.name
        nearby = pampering.bubble_mama_info.nearby_poi
        self.subject.data = F"Would you like to pamper {name} in {district} near {nearby}?"

    def initialize_districts(self, pampering):
        districts_in_city = AreaService().get_districts_in_same_city_by_district(pampering.district.id)
        self.districts.choices = [(district.id, district.name) for district in districts_in_city]
        self.districts.data = [pampering.district.id]

    def initialize_message(self, pampering):
        signup_link = "{uri_base}/pamperings/{id}/signup".format(
            uri_base=ConfigurationService().get("URI_BASE"),
            id=pampering.id)

        self.message.data = TemplateRenderer().render(
                "pamperings/invite_email.html.j2", 
                name=pampering.bubble_mama_info.name,
                signup_link=signup_link,
                district=pampering.district.name,
                nearby=pampering.bubble_mama_info.nearby_poi,
                languages=pampering.bubble_mama_info.languages,
                family_situation=pampering.bubble_mama_info.family_situation,
                food_allergies=pampering.bubble_mama_info.food_allergies,
                diet_restrictions=pampering.bubble_mama_info.diet_restrictions,
                message=pampering.bubble_mama_info.personal_message)

    def get_additional_recipients(self):
        return [x for x in split(",| ", self.additional_recipients.data) if len(x) > 0]
