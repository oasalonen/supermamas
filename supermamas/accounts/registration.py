from flask_babel import gettext
from supermamas.accounts.user import User

class RegistrationService:
    __instance = None

    def __new__(cls, repository=None):
        if not RegistrationService.__instance:
            RegistrationService.__instance = object.__new__(cls)
            RegistrationService.__instance.repository = repository
        return RegistrationService.__instance

    def register_bubble_mama(self, form):
        user = User()
        user.first_name = form["first_name"]
        user.last_name = form["last_name"]

        errors = {}
        if not user.first_name:
            errors["first_name"] = gettext(u"First name is missing")
        if not user.last_name:
            errors["last_name"] = gettext(u"Last name is missing")

        if not errors:
            user = self.repository.insert(user)
        else:
            user = None

        return (user, errors)
