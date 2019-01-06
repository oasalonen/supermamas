from flask_pymongo import ObjectId
from flask_login import UserMixin
from secrets import token_urlsafe
from datetime import datetime, timedelta
from supermamas.accounts.models.address import Address
from supermamas.accounts.models.helping_mama_profile import HelpingMamaProfile
from supermamas.accounts.models.bubble_mama_profile import BubbleMamaProfile

class User(dict, UserMixin):
    def __init__(self, init_dict = None):
        self.address = Address()
        if init_dict:
            self.update(init_dict)

            address = init_dict.get("address")
            if address:
                self.address = Address(address)

            bubble_mama_profile = init_dict.get("bubble_mama_profile")
            if bubble_mama_profile:
                self.bubble_mama_profile = BubbleMamaProfile(bubble_mama_profile)

            helping_mama_profile = init_dict.get("helping_mama_profile")
            if helping_mama_profile:
                self.helping_mama_profile = HelpingMamaProfile(helping_mama_profile)
        return

    @property
    def ROLE_ADMIN(self):
        return "ADMIN"

    @property
    def ROLE_BUBBLE_MAMA(self):
        return "BUBBLE_MAMA"

    @property
    def ROLE_HELPING_MAMA(self):
        return "HELPING_MAMA"

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
    def phone_number(self):
        return self.get("postal_code")

    @phone_number.setter
    def phone_number(self, value):
        self["phone_number"] = value

    @property
    def address(self):
        return self.get("address")

    @address.setter
    def address(self, value):
        self["address"] = value

    @property
    def referrer(self):
        return self.get("referrer")

    @referrer.setter
    def referrer(self, value):
        self["referrer"] = value

    @property
    def registration_time(self):
        return self.get("registration_time")

    @registration_time.setter
    def registration_time(self, value):
        self["registration_time"] = value

    @property
    def bubble_mama_profile(self):
        return self.get("bubble_mama_profile")

    @bubble_mama_profile.setter
    def bubble_mama_profile(self, value):
        self["bubble_mama_profile"] = value

    @property
    def helping_mama_profile(self):
        return self.get("helping_mama_profile")

    @helping_mama_profile.setter
    def helping_mama_profile(self, value):
        self["helping_mama_profile"] = value

    @property
    def is_admin(self):
        return self.has_role(self.ROLE_ADMIN)

    @property
    def is_bubble_mama(self):
        return self.has_role(self.ROLE_BUBBLE_MAMA)

    @property
    def is_helping_mama(self):
        return self.has_role(self.ROLE_HELPING_MAMA)

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