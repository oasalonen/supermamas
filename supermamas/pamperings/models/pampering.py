from enum import Enum
from flask_pymongo import ObjectId

from supermamas.pamperings.models.signup import Signup
from supermamas.accounts import UserReference
from supermamas.areas import District

class PamperingType(Enum):
    PRE = "PRE"
    STANDARD = "STANDARD"
    BELATED = "BELATED"
    EMERGENCY = "EMERGENCY"
    SUPPORT = "SUPPORT"

class Pampering(dict):
    def __init__(self, init_dict=None):
        if init_dict:
            self.update(init_dict)
            self.bubble_mama = init_dict.get("bubble_mama")
            self.district = init_dict.get("district")

    @property 
    def id(self):
        return str(self.get("_id"))

    @id.setter
    def id(self, value):
        self["_id"] = ObjectId(value)

    @property
    def bubble_mama(self):
        return self.get("bubble_mama")

    @bubble_mama.setter
    def bubble_mama(self, value):
        self["bubble_mama"] = UserReference(value) if value else None

    @property
    def district(self):
        return self.get("district")

    @district.setter
    def district(self, value):
        self["district"] = District(value) if value else None

    @property
    def available_dates(self):
        return self.get("available_dates")

    @available_dates.setter
    def available_dates(self, dates):
        self["available_dates"] = dates

    @property
    def start_date(self):
        if self.available_dates:
            return sorted(self.available_dates)[0]
        else:
            return None
    
    @property
    def end_date(self):
        if self.available_dates:
            return sorted(self.available_dates)[-1]
        else:
            return None

    @property
    def signups(self):
        return self.get("signups")

    @property
    def assignments(self):
        return self.get("assignments")

    @property
    def nearby_poi(self):
        return self.get("nearby_poi")

    @nearby_poi.setter
    def nearby_poi(self, value):
        self["nearby_poi"] = value