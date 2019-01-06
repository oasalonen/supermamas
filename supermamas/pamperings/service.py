from flask_babel import gettext
from dateutil import rrule, parser
from datetime import datetime, date, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from supermamas.pamperings import Signup
from supermamas.pamperings import Pampering
from supermamas.accounts import Repository as AccountsRepository
from supermamas.areas import AreaService
from supermamas.common import Emailer

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

    def get_pampering(self, pampering_id):
        return self._repository().get(pampering_id)

    def get_all_pamperings(self):
        return self._repository().get_all()

    def get_by_bubble_mamas(self, bubble_mama_ids):
        pamperings = self._repository().get_by_bubble_mamas(bubble_mama_ids)
        return dict([(pampering.bubble_mama.id, pampering) for pampering in pamperings])

    def create_pampering(self, bubble_mama_id, form):
        bubble_mama = self._accounts_repository().get(bubble_mama_id)
        if not bubble_mama:
            raise Exception("Bubble mama {} does not exist", bubble_mama_id)

        available_dates = form.available_dates.get_datetimes()
        district = AreaService().get_district(bubble_mama.address.district.id)
        if not district:
            raise Exception("District {} does not exist", bubble_mama.address.district.id)

        pampering = Pampering()
        pampering.bubble_mama = bubble_mama
        pampering.district = AreaService().get_district(bubble_mama.address.district.id)
        pampering.available_dates = available_dates

        bubble_mama_info = Pampering.BubbleMamaInfo()
        bubble_mama_info.name = form.bubble_mama_name.data
        bubble_mama_info.family_situation = form.family_situation.data
        bubble_mama_info.food_allergies = form.food_allergies.data
        bubble_mama_info.diet_restrictions = form.diet_restrictions.data
        bubble_mama_info.languages = form.languages.data
        bubble_mama_info.personal_message = form.personal_message.data
        bubble_mama_info.nearby_poi = form.nearby_poi.data

        pampering.bubble_mama_info = bubble_mama_info
        pampering = self._repository().insert(pampering)

        return pampering

    def send_pampering_invitation(self, pampering_id, form):
        message = MIMEMultipart("alternative")
        message["Subject"] = form.subject.data
        message["From"] = form.sender.data
        message["To"] = ""

        # TODO: attach plaintext
        message.attach(MIMEText(form.message.data, "html"))

        Emailer().send_message(form.get_recipients(), message)

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