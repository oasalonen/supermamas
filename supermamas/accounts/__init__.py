from supermamas.accounts.user import User
from supermamas.accounts.repository import Repository
from supermamas.accounts.registration import RegistrationService
from supermamas.accounts.authentication import AuthenticationService
from supermamas.accounts import router

def init(app):
    repository = Repository(app)
    registration_service = RegistrationService(repository)
    authentication_service = AuthenticationService(repository, app)