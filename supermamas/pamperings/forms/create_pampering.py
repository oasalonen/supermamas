from wtforms import Form, SelectMultipleField
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

    def __init__(self, formdata=None, **kwargs):
        super().__init__(formdata, **kwargs)

        date_range = []
        for dt in rrule.rrule(rrule.DAILY, dtstart=self.start_date.datetime(), until=self.end_date.datetime()):
            d = dt.date()
            date_range.append((d.isoformat(), "{} {}/{}".format(weekdays()[d.weekday()], d.day, d.month)))
        self.available_dates.choices = date_range


        
