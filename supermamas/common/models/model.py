from flask_pymongo import ObjectId

"""Any model type that gets persisted by the application."""
class Model(dict):
    def __init__(self, init_dict = None):
        if init_dict:
            self.update(init_dict)

"""An entity model. Identifiable by its 'id' property."""
class Entity(Model):
    @property
    def id(self):
        return str(self.get("_id"))

    @id.setter
    def id(self, value):
        self["_id"] = ObjectId(value)

"""A reference to an entity. Note that a reference needs to shed any
extra properties given to it, so it should not call the dict.update() 
method at all.
"""
class Reference(Entity):
    def __init__(self, init_dict = None):
        if init_dict:
            self.id = init_dict["_id"]