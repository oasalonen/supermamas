from supermamas.districts.district import District
from supermamas.districts.repository import Repository
from supermamas.districts.service import Service
from supermamas.districts import router

def init(app):
    repository = Repository(app)
    service = Service(repository)