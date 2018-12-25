
class Signup(dict):
    def __init__(self, init_dict = None):
        if init_dict:
            self.update(init_dict)
        else:
            self["max_visits"] = 0
        return

    @property
    def helping_mama(self):
        return self.get("helping_mama")

    @helping_mama.setter
    def helping_mama(self, user):
        self["helping_mama"] = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    
    @property
    def availabilities(self):
        return self.get("availabilities")

    @availabilities.setter
    def availabilities(self, value):
        self["availabilities"] = value

    @property
    def max_visits(self):
        return self.get("max_visits")

    @max_visits.setter
    def max_visits(self, value):
        self["max_visits"] = value