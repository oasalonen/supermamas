from flask_babel import gettext
from dateutil import rrule
from datetime import datetime, date, timedelta

from supermamas.pamperings import Signup
from supermamas.pamperings import Pampering
from supermamas.accounts import Repository as AccountsRepository

class Service:
    __instance = None

    def __new__(cls, repository=None, accounts_repository=None):
        if not Service.__instance:
            Service.__instance = object.__new__(cls)
            Service.__instance.repository = repository
            Service.__instance.accounts_repository = accounts_repository
        return Service.__instance

    def _repository(self):
        return Service.__instance.repository

    def _accounts_repository(self):
        return Service.__instance.accounts_repository

    def prepare_pampering(self, bubble_mama_id, start_date=None, end_date=None):
        start_date = start_date if start_date else date.today()
        end_date = end_date if end_date else start_date + timedelta(days=14)
        date_range = {}
        for dt in rrule.rrule(rrule.DAILY, dtstart=datetime(start_date.year, start_date.month, start_date.day), until=datetime(end_date.year, end_date.month, end_date.day)):
            d = dt.date()
            date_range[d.isoformat()] = {
                "selected": True,
                "label": "{} {}/{}".format(self.weekdays()[d.weekday()], d.day, d.month)
            }

        return {
            "bubble_mama_id": bubble_mama_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "date_range[]": date_range
            }

    def create_pampering(self, bubble_mama_id, form):
        available_dates = list(filter(lambda d: d.selected, form.date_range))

        pampering = Pampering()
        pampering.bubble_mama = self._accounts_repository().get(bubble_mama_id)
        pampering.available_dates = available_dates
        # Save in db
        # Return potential errors
        return pampering, None

    def add_signup(self, pampering_id, helping_mama_id, availabilities, max_visits=0):
        signup = Signup()
        signup.helping_mama = self._accounts_repository().get(helping_mama_id)
        signup.availabilities = availabilities
        signup.max_visits = max_visits
        
        self._repository().update_field(pampering_id, "signups." + helping_mama_id, signup)

    def weekdays(self):
        return [gettext(u"Mon"), gettext(u"Tue"), gettext(u"Wed"), gettext(u"Thu"), gettext(u"Fri"), gettext(u"Sat"), gettext(u"Sun")]