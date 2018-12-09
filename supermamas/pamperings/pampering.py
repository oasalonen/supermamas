from supermamas.pamperings.signup import Signup

class Pampering(dict):
    def __init__(self, init_dict=None):
        if init_dict:
            self.update(init_dict)
        return

    @property 
    def id(self):
        return self["_id"]

    @id.setter
    def id(self, value):
        self["_id"] = value

    @property
    def bubble_mama(self):
        return self["bubble_mama"]

    @bubble_mama.setter
    def bubble_mama(self, value):
        self["bubble_mama"] = value

    @property
    def available_dates(self):
        return self["available_dates"]

    @available_dates.setter
    def available_dates(self, dates):
        self["available_dates"] = dates

    @property
    def signups(self):
        return self["signups"]

    @property
    def assignments(self):
        return self["assignments"]
