from flask_pymongo import PyMongo, ObjectId

from supermamas.accounts.user import User

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
        result = self.collection.insert_one(user)
        user.id = str(result.inserted_id)
        return user
    
    def get(self, user_id):
        return User(self.collection.find_one({"_id": ObjectId(user_id)}))