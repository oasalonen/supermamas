from supermamas.pamperings.models.pampering import Pampering, PamperingType
from supermamas.pamperings.models.signup import Signup
from supermamas.pamperings.service import Service as PamperingService
from supermamas.pamperings.repository import Repository
from supermamas.pamperings import router
from supermamas import accounts

def init(app):
    repository = Repository(app)
    PamperingService(repository, accounts.Repository())