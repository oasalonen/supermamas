from flask_pymongo import ObjectId
from flask_login import UserMixin
from secrets import token_urlsafe
from datetime import datetime, timedelta

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
    def is_active(self):
        activation = self.get("activation")
        return activation["is_activated"] if activation else False

    @property
    def activation_code(self):
        activation = self.get("activation")
        return activation["code"] if activation else None

    def require_activation(self):
        self["activation"] = {
            "is_activated": False,
            "code": token_urlsafe(16),
            "expires": datetime.utcnow() + timedelta(days=7)
        }

    def activate(self, code):
        activation = self.get("activation")
        if activation and not self.is_active:
            if code and activation.get("code") == code:
                if activation.get("expires") > datetime.utcnow():
                    self["activation"] = {
                        "is_activated": True
                    }
                else:
                    raise Exception("Activation code expired")
            else:
                raise Exception("Unknown activation code")
        else:
            raise Exception("Account cannot be activated")

    @property
    def email(self):
        return self.get("email")

    @email.setter
    def email(self, value):
        self["email"] = value

    @property
    def password(self):
        return self.get("password")

    @password.setter
    def password(self, value):
        self["password"] = value

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
    def district(self):
        return self.get("district")

    @district.setter
    def district(self, value):
        self["district"] = {
            "id": value.id,
            "name": value.name
        }

    @property
    def is_admin(self):
        return self.has_role(self.ROLE_ADMIN)

    @property
    def roles(self):
        return self.get("roles", [])
        
    def has_role(self, role):
        return role in self.roles

    def add_role(self, role):
        if not self.has_role(role):
            roles = self.roles
            roles.append(role)
            self["roles"] = roles