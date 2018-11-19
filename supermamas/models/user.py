
class User(dict):
    def __init__(self, init_dict = None):
        if init_dict:
            self.update(init_dict)
        return

    @property
    def ROLE_ADMIN(self):
        return "ADMIN"

    @property
    def first_name(self):
        return self["first_name"]

    @property
    def last_name(self):
        return self["last_name"]

    @property
    def is_admin(self):
        return self.has_role(self.ROLE_ADMIN)

    def has_role(self, role):
        return role in self.get("roles", [])

    #def from_registration(registration):
