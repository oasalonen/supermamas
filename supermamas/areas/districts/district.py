from flask_pymongo import ObjectId

class District(dict):
    def __init__(self, init_dict = None):
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
    def name(self):
        return self.get("name")

    @name.setter
    def name(self, value):
        self["name"] = value
