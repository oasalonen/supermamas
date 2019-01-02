from supermamas.areas.cities.city import City
from supermamas.areas.cities.repository import Repository as CityRepository

def init(app):
    CityRepository(app)