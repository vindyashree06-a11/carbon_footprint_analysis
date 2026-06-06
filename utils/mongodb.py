
from pymongo import MongoClient
import os

class MongoDBManager:

    def __init__(
        self,
        uri=None,
        database="steel_esg"
    ):

        self.uri = uri or os.getenv(
            "MONGO_URI",
            "mongodb://localhost:27017"
        )

        self.client = MongoClient(
            self.uri
        )

        self.db = self.client[database]

    def insert_document(
        self,
        collection,
        document
    ):

        return (
            self.db[collection]
            .insert_one(document)
        )

    def insert_many(
        self,
        collection,
        documents
    ):

        return (
            self.db[collection]
            .insert_many(documents)
        )

    def find_all(
        self,
        collection
    ):

        return list(
            self.db[collection]
            .find()
        )

    def delete_all(
        self,
        collection
    ):

        return (
            self.db[collection]
            .delete_many({})
        )
