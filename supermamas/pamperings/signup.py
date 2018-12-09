
class Signup(dict):
    def __init__(self, init_dict = None):
        if init_dict:
            self.update(init_dict)
        else:
            self["max_visits"] = 0
        return

    @property
    def helping_mama(self):
        return self["helping_mama"]

    @helping_mama.setter
    def helping_mama(self, value):
        self["helping_mama"] = value
    
    @property
    def availabilities(self):
        return self["availabilities"]

    @availabilities.setter
    def availabilities(self, value):
        self["availabilities"] = value

    @property
    def max_visits(self):
        return self["max_visits"]