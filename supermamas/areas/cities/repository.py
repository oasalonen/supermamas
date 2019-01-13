from flask_pymongo import PyMongo, ObjectId

from supermamas.areas.cities import City

class Repository:
    __instance = None

    def __new__(cls, app=None):
        if not Repository.__instance:
            Repository.__instance = object.__new__(cls)
            Repository.__instance.app = app
            Repository.__instance.pymongo = PyMongo(app)
        return Repository.__instance

    @property
    def collection(self):
        return self.pymongo.db.cities

    def insert(self, city):
        result = self.collection.insert_one(city)
        city.id = str(result.inserted_id)
        return city

    def remove(self, city_id):
        self.collection.delete_one({"_id": ObjectId(city_id)})
    
    def get(self, city_id):
        city = self.collection.find_one({"_id": ObjectId(city_id)})
        return City(city) if city else None

    def get_all(self):
        return [City(city) for city in self.collection.find()]

    def get_by_district(self, district_id):
        city = self.collection.find_one({ "districts._id": ObjectId(district_id) })
        return City(city) if city else None