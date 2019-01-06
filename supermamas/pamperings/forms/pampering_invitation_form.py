from wtforms import Form, StringField, TextAreaField
from wtforms.validators import Email, InputRequired
from flask_babel import gettext
from re import split

from supermamas.common import TemplateRenderer, ConfigurationService

class PamperingInvitationForm(Form):

    sender = StringField(
        gettext(u"Sender"), [
        Email(gettext(u"Please enter a valid email address")),
        InputRequired(gettext(u"Please fill this field"))
        ])

    recipients = TextAreaField(
        gettext(u"Recipients"), 
        [InputRequired(gettext(u"Please fill this field"))],
        description=gettext(u"Email addresses of HelpingMamas who should receive the pampering invitation.")
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

    def initialize_fields(self, sender=None, recipients=None, pampering=None):
        if sender:
            self.sender.data = sender
        
        if recipients:
            self.recipients.data = ", ".join(recipients)

        if pampering:
            self.initialize_subject(pampering)
            self.initialize_message(pampering)

    def initialize_subject(self, pampering):
        name = pampering.bubble_mama_info.name
        district = pampering.district.name
        nearby = pampering.bubble_mama_info.nearby_poi
        self.subject.data = F"Would you like to pamper {name} in {district} near {nearby}?"

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

    def get_recipients(self):
        return [x for x in split(",| ", self.recipients.data) if len(x) > 0]
