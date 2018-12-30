from enum import Enum
from flask_pymongo import ObjectId
from supermamas.pamperings.signup import Signup

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
        return

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
    def bubble_mama(self, user):
        self["bubble_mama"] = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name
        }

    @property
    def district(self):
        return self.get("district")

    @district.setter
    def district(self, value):
        self["district"] = {
            "id": value.id,
            "name": value.name
        }

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
