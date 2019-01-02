from supermamas.areas.districts import District, DistrictRepository
from supermamas.areas.cities import City, CityRepository
from supermamas.areas import cities, districts
from supermamas.areas.service import Service as AreaService
from supermamas.areas import router

def init(app):
    cities.init(app)
    districts.init(app)
    AreaService(DistrictRepository(), CityRepository())