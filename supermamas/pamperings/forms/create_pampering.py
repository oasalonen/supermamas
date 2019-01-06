from wtforms import Form, SelectMultipleField, StringField
from wtforms.validators import InputRequired
from flask_babel import gettext
from dateutil import rrule, parser
from datetime import datetime, date, timedelta

from supermamas.common.forms import CalendarField, CalendarSelectField
from supermamas.common import weekdays

def default_start_date():
    return datetime.utcnow() + timedelta(days=14)

def default_end_date():
    return default_start_date() + timedelta(days=20)

class CreatePamperingForm(Form):
    start_date = CalendarField(
        gettext(u"Start date"),
        default=default_start_date()
        )

    end_date = CalendarField(
        gettext(u"End date"),
        default=default_end_date()
        )

    available_dates = CalendarSelectField("")

    nearby_poi = StringField(
        gettext(u"Nearby place"),
        [InputRequired(gettext(u"Please fill this field"))],
        description=gettext(u"e.g. a nearby station that helps HelpingMamas understand approximately where the pampering will happen")
        )

    bubble_mama_name = StringField(
        gettext(u"BubbleMama's name"),
        [InputRequired(gettext(u"Please fill this field"))],
        description=gettext(u"Only share BubbleMama's first name")
        )

    family_situation = StringField(gettext(u"Family situation"))

    food_allergies = StringField(gettext(u"Food allergies"))

    diet_restrictions = StringField(gettext(u"Diet restrictions"))

    languages = StringField(gettext(u"Languages understood"))

    personal_message = StringField(gettext(u"Personal message"))

    def __init__(self, formdata=None, **kwargs):
        super().__init__(formdata, **kwargs)

        date_range = []
        for dt in rrule.rrule(rrule.DAILY, dtstart=self.start_date.datetime(), until=self.end_date.datetime()):
            d = dt.date()
            date_range.append((d.isoformat(), "{} {}/{}".format(weekdays()[d.weekday()], d.day, d.month)))
        self.available_dates.choices = date_range

    def set_bubble_mama(self, bubble_mama):
        profile = bubble_mama.bubble_mama_profile
        self.bubble_mama_name.data = bubble_mama.first_name
        self.family_situation.data = profile.family_situation
        self.food_allergies.data = profile.food_allergies
        self.diet_restrictions.data = profile.diet_restrictions
        self.languages.data = ", ".join(profile.languages)
        self.personal_message.data = profile.personal_message

        
