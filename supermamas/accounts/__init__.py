from supermamas.accounts.models.user import User
from supermamas.accounts.models.admin import Admin
from supermamas.accounts.models.address import Address
from supermamas.accounts.models.bubble_mama_profile import BubbleMamaProfile
from supermamas.accounts.models.helping_mama_profile import HelpingMamaProfile
from supermamas.accounts.repository import Repository
from supermamas.accounts.authentication import AuthenticationService
from supermamas.accounts.registration import RegistrationService
from supermamas.accounts import router

def init(app):
    repository = Repository(app)
    authentication_service = AuthenticationService(repository, app)
    registration_service = RegistrationService(repository, app)