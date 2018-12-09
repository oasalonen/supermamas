from supermamas.pamperings.pampering import Pampering
from supermamas.pamperings.signup import Signup
from supermamas.pamperings.service import Service
from supermamas.pamperings.repository import Repository
from supermamas import accounts

def init(app):
    repository = Repository(app)
    service = Service(repository, accounts.Repository())