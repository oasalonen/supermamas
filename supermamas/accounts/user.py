from flask_pymongo import ObjectId
from flask_login import UserMixin

class User(dict, UserMixin):
    def __init__(self, init_dict = None):
        if init_dict:
            self.update(init_dict)
        return

    @property
    def ROLE_ADMIN(self):
        return "ADMIN"

    @property
    def id(self):
        return str(self.get("_id"))

    @id.setter
    def id(self, value):
        self["_id"] = ObjectId(value)

    @property
    def email(self):
        return self.get("email")

    @email.setter
    def email(self, value):
        self["email"] = value

    @property
    def first_name(self):
        return self.get("first_name")
    
    @first_name.setter
    def first_name(self, value):
        self["first_name"] = value

    @property
    def last_name(self):
        return self.get("last_name")

    @last_name.setter
    def last_name(self, value):
        self["last_name"] = value

    @property
    def is_admin(self):
        return self.has_role(self.ROLE_ADMIN)

    def has_role(self, role):
        return role in self.get("roles", [])