from flask_babel import gettext
from dateutil import rrule, parser
from datetime import datetime, date, timedelta

from supermamas.districts.district import District

class Service:
    __instance = None

    def __new__(cls, repository=None):
        if not Service.__instance:
            Service.__instance = object.__new__(cls)
            Service.__instance.repository = repository
        return Service.__instance

    def _repository(self):
        return Service.__instance.repository

    def districts(self):
        return self._repository().get_all()

    def get_district(self, district_id):
        return self._repository().get(district_id)
    
    def add_district(self, district_name):
        errors = {}
        if not district_name:
            errors["district_name"] = gettext(u"District name is missing")

        if not errors:
            district = District()
            district.name = district_name
            district = self._repository().insert(district)
        else:
            district = None

        return (district, errors)

    def delete_district(self, district_id):
        self._repository().remove(district_id)