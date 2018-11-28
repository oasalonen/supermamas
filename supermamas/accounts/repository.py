from flask_pymongo import PyMongo

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
        return self.pymongo.db.users

    def insert(self, user):
        return self.collection.insert_one(user)