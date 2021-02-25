import pymongo
import pdb


class MongoProvider(object):

    collection_name = "water"

    def __init__(self, uri, database):
        self.mongo_uri = uri
        self.mongo_db = database or "water"

    def get_collection(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        return self.client[self.mongo_db][self.collection_name]

    def close_connection(self):
        self.client.close()
