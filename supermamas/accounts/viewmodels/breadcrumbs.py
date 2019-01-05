from enum import IntEnum
from flask import url_for
from flask_babel import gettext

class BubbleMamaRegistrationBreadcrumbs(dict):

    class Step(IntEnum):
        INTRODUCTION = 0,
        CITY = 1,
        PAMPERING_TYPE = 2,
        PROFILE = 3

    def __init__(self, current_step, city, pampering_type):
        step = self.properties(self.Step.INTRODUCTION, self.Step.INTRODUCTION, city, pampering_type)
        self["steps"] = [self.properties(step, current_step, city, pampering_type) for step in self.Step]

    def properties(self, step, current_step, city, pampering_type):
        switcher = {
            self.Step.INTRODUCTION: {
                "label": gettext(u"Become a BubbleMama"),
                "link": url_for("accounts.register_bubble_mama_intro"),
                "is_current": current_step == self.Step.INTRODUCTION,
                "is_disabled": current_step < self.Step.INTRODUCTION 
            },
            self.Step.CITY: {
                "label": gettext(u"City"),
                "link": url_for("accounts.register_bubble_mama_city"),
                "is_current": current_step == self.Step.CITY,
                "is_disabled": current_step < self.Step.CITY 
            },
            self.Step.PAMPERING_TYPE: {
                "label": gettext(u"Pampering Type"),
                "link": url_for("accounts.register_bubble_mama_pampering_type", city=city),
                "is_current": current_step == self.Step.PAMPERING_TYPE,
                "is_disabled": current_step < self.Step.PAMPERING_TYPE 
            },
            self.Step.PROFILE: {
                "label": gettext(u"Profile"),
                "link": url_for("accounts.register_bubble_mama_profile", city=city, pampering_type=pampering_type),
                "is_current": current_step == self.Step.PROFILE,
                "is_disabled": current_step < self.Step.PROFILE 
            }
        }
        return switcher.get(step)


class HelpingMamaRegistrationBreadcrumbs(dict):

    class Step(IntEnum):
        INTRODUCTION = 0,
        CITY = 1,
        PROFILE = 2

    def __init__(self, current_step, city):
        step = self.properties(self.Step.INTRODUCTION, self.Step.INTRODUCTION, city)
        self["steps"] = [self.properties(step, current_step, city) for step in self.Step]

    def properties(self, step, current_step, city):
        switcher = {
            self.Step.INTRODUCTION: {
                "label": gettext(u"Become a HelpingMama"),
                "link": url_for("accounts.register_helping_mama_intro"),
                "is_current": current_step == self.Step.INTRODUCTION,
                "is_disabled": current_step < self.Step.INTRODUCTION 
            },
            self.Step.CITY: {
                "label": gettext(u"City"),
                "link": url_for("accounts.register_helping_mama_city"),
                "is_current": current_step == self.Step.CITY,
                "is_disabled": current_step < self.Step.CITY 
            },
            self.Step.PROFILE: {
                "label": gettext(u"Profile"),
                "link": url_for("accounts.register_helping_mama_profile", city=city),
                "is_current": current_step == self.Step.PROFILE,
                "is_disabled": current_step < self.Step.PROFILE 
            }
        }
        return switcher.get(step)