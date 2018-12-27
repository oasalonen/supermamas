from supermamas.districts.district import District
from supermamas.districts.repository import Repository
from supermamas.districts.service import Service

def init(app):
    repository = Repository(app)
    service = Service(repository)