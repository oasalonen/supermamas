from flask_babel import gettext
from dateutil import rrule, parser
from datetime import datetime, date, timedelta

from supermamas.pamperings import Signup
from supermamas.pamperings import Pampering
from supermamas.accounts import Repository as AccountsRepository
from supermamas.areas import AreaService

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

    def get_all_pamperings(self):
        return self._repository().get_all()

    def prepare_pampering(self, bubble_mama_id, start_date=None, end_date=None):
        start_date = start_date if start_date else date.today()
        end_date = end_date if end_date else start_date + timedelta(days=20)
        date_range = {}
        for dt in rrule.rrule(rrule.DAILY, dtstart=datetime(start_date.year, start_date.month, start_date.day), until=datetime(end_date.year, end_date.month, end_date.day)):
            d = dt.date()
            date_range[d.isoformat()] = {
                "selected": False,
                "weekday": d.weekday(),
                "label": "{} {}/{}".format(self.weekdays()[d.weekday()], d.day, d.month)
            }

        bubble_mama = self._accounts_repository().get(bubble_mama_id)

        return {
            "bubble_mama": {
                "id": bubble_mama_id,
                "first_name": bubble_mama.first_name,
                "last_name": bubble_mama.last_name
            },
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "date_range[]": date_range
            }

    def create_pampering(self, bubble_mama_id, date_range):
        errors = {}

        available_dates = list(map(lambda d: parser.parse(d), date_range))
        if len(available_dates) == 0:
            errors["date_range[]"] = gettext(u"You must select at least one date for a pampering")
            return None, errors

        bubble_mama = self._accounts_repository().get(bubble_mama_id)
        if not bubble_mama:
            errors["bubble_mama_id"] = gettext(u"That bubble mama doesn't seem to exist...")

        if not errors:
            pampering = Pampering()
            pampering.bubble_mama = bubble_mama
            pampering.district = AreaService().get_district(bubble_mama.district["id"])
            pampering.available_dates = available_dates
            pampering = self._repository().insert(pampering)
        else:
            pampering = None

        return (pampering, errors)

    def prepare_signup(self, pampering_id, helping_mama_id):
        pampering = self._repository().get(pampering_id)
        if not pampering:
            raise Exception("Pampering not found")

        helping_mama = self._accounts_repository().get(helping_mama_id)
        if not helping_mama:
            raise Exception("Helping mama not found")

        if helping_mama_id == pampering["bubble_mama"]["id"]:
            raise Exception("A bubble mama cannot sign up for their own pampering")

        current_signup = None
        signups = {}
        if pampering.signups:
            signups = dict(pampering.signups)
            if helping_mama_id in signups:
                current_signup = signups[helping_mama_id]
                del signups[helping_mama_id]

        if not current_signup:
            current_signup = { 
                "helping_mama": {
                    "id": helping_mama.id,
                    "first_name": helping_mama.first_name,
                    "last_name": helping_mama.last_name
                },
                "availabilities": [] 
            }

        available_dates = {dt[0]:dt[1] for dt in [self.displayable_date(dt) for dt in pampering.available_dates]}

        return {
            "bubble_mama": pampering.bubble_mama,
            "available_dates": available_dates,
            "signups": signups,
            "current_signup": current_signup
        }

    def add_signup(self, pampering_id, helping_mama_id, availabilities, max_visits=0):
        errors = {}

        pampering = self._repository().get(pampering_id)
        if not pampering:
            raise Exception("Pampering not found: {}", pampering_id)

        helping_mama = self._accounts_repository().get(helping_mama_id)
        if not helping_mama:
            raise Exception("Unknown user attempted to sign up for a pampering: {}", helping_mama_id)

        availabilities = list(map(lambda d: parser.parse(d), availabilities))
        if len(availabilities) == 0:
            if helping_mama_id in pampering.signups:
                pampering_plan = self._repository().update_field(pampering_id, "signups." + helping_mama_id, None)
                return (pampering_plan, None)
            else:
                errors["availabilities[]"] = gettext(u"You must select at least one date to sign up for a pampering")
                return None, errors

        if not errors:
            signup = Signup()
            signup.helping_mama = helping_mama
            signup.availabilities = availabilities
            signup.max_visits = max_visits
        
        pampering_plan = self._repository().update_field(pampering_id, "signups." + helping_mama_id, signup)
        return (pampering_plan, None)

    def displayable_date(self, dt):
        d = dt.date()
        return (d.isoformat(), {
            "weekday": d.weekday(),
            "weekday_label": self.weekdays()[d.weekday()],
            "date_label": "{} {}/{}".format(self.weekdays()[d.weekday()], d.day, d.month)
        })

    def weekdays(self):
        return [gettext(u"Mon"), gettext(u"Tue"), gettext(u"Wed"), gettext(u"Thu"), gettext(u"Fri"), gettext(u"Sat"), gettext(u"Sun")]