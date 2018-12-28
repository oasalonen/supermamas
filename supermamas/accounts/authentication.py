from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from supermamas.accounts.user import User
from supermamas import districts

# TODO: use alternative tokens
# https://flask-login.readthedocs.io/en/latest/#alternative-tokens
def load_user(user_id):
    return AuthenticationService()._repository().get(user_id)

class AuthenticationService:
    __instance = None

    def __new__(cls, repository=None, app=None):
        if not AuthenticationService.__instance:
            AuthenticationService.__instance = object.__new__(cls)
            AuthenticationService.__instance.repository = repository

            login_manager = LoginManager()
            login_manager.init_app(app)
            login_manager.user_loader(load_user)
            login_manager.login_view = "accounts.login"
            AuthenticationService.__instance.login_manager = login_manager

            AuthenticationService.__instance.bcrypt = Bcrypt(app)
        return AuthenticationService.__instance

    def _repository(self):
        return self.__instance.repository

    def _login_manager(self):
        return self.__instance.login_manager

    def _bcrypt(self):
        return self.__instance.bcrypt

    def authenticate(self, email, password):
        user = self._repository().get_by_email(email)
        if user and self._bcrypt().check_password_hash(user.password, password):
            return user
        else:
            return None

