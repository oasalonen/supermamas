from flask_pymongo import PyMongo, ObjectId

from supermamas.accounts import User

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

    def replace(self, user):
        self.collection.replace_one({ "_id": ObjectId(user.id) }, user)
    
    def get(self, user_id):
        user = self.collection.find_one({ "_id": ObjectId(user_id) })
        return User(user) if user else None

    def get_by_email(self, email):
        user = self.collection.find_one({ "email": email })
        return User(user) if user else None

    def get_by_role(self, role):
        results = self.collection.find({ "roles": role })
        return [User(result) for result in results]