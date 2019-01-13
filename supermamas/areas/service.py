from flask_babel import gettext
from dateutil import rrule, parser
from datetime import datetime, date, timedelta

from supermamas.areas.districts import District
from supermamas.areas.cities import City

class Service:
    __instance = None

    def __new__(cls, district_repository=None, city_repository=None):
        if not Service.__instance:
            Service.__instance = object.__new__(cls)
            Service.__instance.district_repository = district_repository
            Service.__instance.city_repository = city_repository
        return Service.__instance

    def _district_repository(self):
        return Service.__instance.district_repository

    def _city_repository(self):
        return Service.__instance.city_repository

    def cities(self):
        return self._city_repository().get_all()

    def districts(self):
        return self._district_repository().get_all()

    def get_city(self, city_id):
        return self._city_repository().get(city_id)

    def get_district(self, district_id):
        return self._district_repository().get(district_id)

    def get_districts_in_same_city_by_district(self, district_id):
        city = self._city_repository().get_by_district(district_id)
        return city.districts

    def add_city(self, city_name):
        errors = {}
        if not city_name:
            errors["city_name"] = gettext(u"City name is missing")

        if not errors:
            city = City()
            city.name = city_name
            city = self._city_repository().insert(city)
        else:
            city = None

        return (city, errors)
    
    def add_district(self, district_name):
        errors = {}
        if not district_name:
            errors["district_name"] = gettext(u"District name is missing")

        if not errors:
            district = District()
            district.name = district_name
            district = self._district_repository().insert(district)
        else:
            district = None

        return (district, errors)

    def delete_city(self, city_id):
        self._city_repository().remove(city_id)

    def delete_district(self, district_id):
        self._district_repository().remove(district_id)