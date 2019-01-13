from flask_pymongo import ObjectId
from supermamas.areas import District
from supermamas.common import Entity

class City(Entity):
    def __init__(self, init_dict = None):
        self["districts"] = []
        super().__init__(init_dict)
        if init_dict:
            districts = init_dict.get("districts")
            if districts:
                self["districts"] = [District(district) for district in districts]

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
