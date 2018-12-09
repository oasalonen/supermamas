from flask_babel import gettext
from supermamas.pamperings import Signup
from supermamas.pamperings import Pampering
from supermamas.accounts import Repository as AccountsRepository

class Service:
    __instance = None

    def __new__(cls, repository=None, accounts_repository=None):
        if not Service.__instance:
            Service.__instance = object.__new__(cls)
            Service.__instance.repository = repository
            Service.__instance.accounts_repository = accounts_repository
        return Service.__instance

    def _repository(self):
        return Service.__instance.repository

    def _accounts_repository(self):
        return Service.__instance.accounts_repository

    def create_pampering(self, bubble_mama_id, available_dates):
        pampering = Pampering()
        pampering.bubble_mama = self._accounts_repository().get(bubble_mama_id)
        pampering.available_dates = available_dates
        # Save in db
        # Return potential errors
        return pampering, None

    def add_signup(self, pampering_id, helping_mama_id, availabilities, max_visits=0):
        signup = Signup()
        signup.helping_mama = self._accounts_repository().get(helping_mama_id)
        signup.availabilities = availabilities
        signup.max_visits = max_visits
        
        self._repository().update_field(pampering_id, "signups." + helping_mama_id, signup)