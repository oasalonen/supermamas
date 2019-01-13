from enum import Enum
from flask_pymongo import ObjectId

from supermamas.pamperings.models.signup import Signup
from supermamas.accounts import UserReference
from supermamas.areas import District
from supermamas.common import Entity, Model

class PamperingType(Enum):
    PRE = "PRE"
    STANDARD = "STANDARD"
    BELATED = "BELATED"
    EMERGENCY = "EMERGENCY"
    SUPPORT = "SUPPORT"

class Pampering(Entity):
    def __init__(self, init_dict=None):
        super().__init__(init_dict)
        if init_dict:
            self.bubble_mama = init_dict.get("bubble_mama")
            self.district = init_dict.get("district")
            self.bubble_mama_info = init_dict.get("bubble_mama_info")

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
    def bubble_mama_info(self):
        return self.get("bubble_mama_info")

    @bubble_mama_info.setter
    def bubble_mama_info(self, value):
        self["bubble_mama_info"] = self.BubbleMamaInfo(value)

    class BubbleMamaInfo(Model):

        @property
        def name(self):
            return self.get("name")

        @name.setter
        def name(self, value):
            self["name"] = value

        @property
        def family_situation(self):
            return self.get("family_situation")

        @family_situation.setter
        def family_situation(self, value):
            self["family_situation"] = value

        @property
        def food_allergies(self):
            return self.get("food_allergies")

        @food_allergies.setter
        def food_allergies(self, value):
            self["food_allergies"] = value

        @property
        def diet_restrictions(self):
            return self.get("diet_restrictions")

        @diet_restrictions.setter
        def diet_restrictions(self, value):
            self["diet_restrictions"] = value

        @property
        def languages(self):
            return self.get("languages")

        @languages.setter
        def languages(self, value):
            self["languages"] = value

        @property
        def personal_message(self):
            return self.get("personal_message")

        @personal_message.setter
        def personal_message(self, value):
            self["personal_message"] = value

        @property
        def nearby_poi(self):
            return self.get("nearby_poi")

        @nearby_poi.setter
        def nearby_poi(self, value):
            self["nearby_poi"] = value
    

