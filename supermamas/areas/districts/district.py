from flask_pymongo import ObjectId

from supermamas.common import Entity

class District(Entity):
    @property
    def name(self):
        return self.get("name")

    @name.setter
    def name(self, value):
        self["name"] = value
