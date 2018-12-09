from flask_pymongo import PyMongo, ObjectId

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
        return self.pymongo.db.pamperings

    def insert(self, pampering):
        result = self.collection.insert_one(pampering)
        pampering.id = str(result.inserted_id)
        return pampering

    def get(self, pampering_id):
        return self.collection.find_one({"_id": ObjectId(pampering_id)})

    def update_field(self, pampering_id, field, value):
        self.collection.update_one({"_id": ObjectId(pampering_id)}, {"$set": {field: value}})
