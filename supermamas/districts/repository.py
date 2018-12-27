from flask_pymongo import PyMongo, ObjectId

from supermamas.districts.district import District

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
        return self.pymongo.db.districts

    def insert(self, district):
        result = self.collection.insert_one(district)
        district.id = str(result.inserted_id)
        return district

    def remove(self, district_id):
        self.collection.delete_one({"_id": ObjectId(district_id)})
    
    def get(self, district_id):
        return District(self.collection.find_one({"_id": ObjectId(district_id)}))

    def get_all(self):
        return [District(district) for district in self.collection.find()]