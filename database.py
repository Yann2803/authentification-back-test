import pymongo


class DB(object):

    URI = "mongodb://127.0.0.1:27017"

    @staticmethod
    def init():
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['newDB']

    @staticmethod
    def insert(collection, query):
        DB.DATABASE[collection].insert(query)

    @staticmethod
    def find_one(collection, query):
        print('query', query)
        return DB.DATABASE[collection].find_one(query)

    @staticmethod
    def delete_one(collection, query):
        return DB.DATABASE[collection].delete_one(query)

    @staticmethod
    def find(collection):
        return DB.DATABASE[collection].find()

    @staticmethod
    def update_one(collection, searched_id, query):
        return DB.DATABASE[collection].update_one(searched_id, query)