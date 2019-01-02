from supermamas.areas.districts.district import District
from supermamas.areas.districts.repository import Repository as DistrictRepository

def init(app):
    DistrictRepository(app)