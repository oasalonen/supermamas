from supermamas.accounts.user import User
from supermamas.accounts.repository import Repository
from supermamas.accounts.registration import RegistrationService

def init(app):
    repository = Repository(app)
    registration_service = RegistrationService(repository)