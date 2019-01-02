from flask_pymongo import ObjectId

class City(dict):
    def __init__(self, init_dict = None):
        self["districts"] = None
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

    @property
    def districts(self):
        return self.get("districts")

    def add_district(self, district):
        self.districts.append(district)
