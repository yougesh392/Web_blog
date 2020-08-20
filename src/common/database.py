import pymongo


class Database(object):
    # static variables
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    """
    @staticmethod
    To tell python not giving self Because this method
    is not going to be of instace to database
    but only for this class
    """

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
