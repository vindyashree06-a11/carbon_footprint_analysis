# utils/mongodb.py

import os
import logging
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    ServerSelectionTimeoutError,
    PyMongoError
)

# ----------------------------------------------------
# LOGGER
# ----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ----------------------------------------------------
# ENV VARIABLES
# ----------------------------------------------------

MONGO_URI = os.getenv("MONGO_URI")

DATABASE_NAME = os.getenv(
    "MONGO_DB_NAME",
    "steel_esg_db"
)

# ----------------------------------------------------
# CONNECTION
# ----------------------------------------------------

class MongoDBManager:

    def __init__(self):

        self.client = None
        self.db = None

        self.connect()

    # ------------------------------------------------

    def connect(self):

        try:

            self.client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000
            )

            self.client.admin.command("ping")

            self.db = self.client[
                DATABASE_NAME
            ]

            logger.info(
                "MongoDB Atlas Connected"
            )

        except (
            ConnectionFailure,
            ServerSelectionTimeoutError
        ) as e:

            logger.error(
                f"MongoDB Connection Failed: {e}"
            )

            self.client = None
            self.db = None

    # ------------------------------------------------

    def is_connected(self):

        return self.db is not None

    # ------------------------------------------------

    def get_collection(
        self,
        collection_name
    ):

        if not self.is_connected():
            return None

        return self.db[
            collection_name
        ]

    # ------------------------------------------------

    def insert_one(
        self,
        collection_name,
        document
    ):

        try:

            collection = self.get_collection(
                collection_name
            )

            if collection is None:
                return None

            document[
                "created_at"
            ] = datetime.utcnow()

            result = collection.insert_one(
                document
            )

            return str(
                result.inserted_id
            )

        except PyMongoError as e:

            logger.error(
                f"Insert Error: {e}"
            )

            return None

    # ------------------------------------------------

    def insert_many(
        self,
        collection_name,
        documents
    ):

        try:

            collection = self.get_collection(
                collection_name
            )

            if collection is None:
                return []

            for doc in documents:

                doc[
                    "created_at"
                ] = datetime.utcnow()

            result = collection.insert_many(
                documents
            )

            return [
                str(x)
                for x in result.inserted_ids
            ]

        except PyMongoError as e:

            logger.error(
                f"Bulk Insert Error: {e}"
            )

            return []

    # ------------------------------------------------

    def find(
        self,
        collection_name,
        query={}
    ):

        try:

            collection = self.get_collection(
                collection_name
            )

            if collection is None:
                return []

            return list(
                collection.find(query)
            )

        except PyMongoError as e:

            logger.error(
                f"Find Error: {e}"
            )

            return []

    # ------------------------------------------------

    def find_one(
        self,
        collection_name,
        query={}
    ):

        try:

            collection = self.get_collection(
                collection_name
            )

            if collection is None:
                return None

            return collection.find_one(
                query
            )

        except PyMongoError as e:

            logger.error(
                f"Find One Error: {e}"
            )

            return None

    # ------------------------------------------------

    def update_one(
        self,
        collection_name,
        query,
        update_data
    ):

        try:

            collection = self.get_collection(
                collection_name
            )

            if collection is None:
                return 0

            result = collection.update_one(
                query,
                {
                    "$set":
                    update_data
                }
            )

            return result.modified_count

        except PyMongoError as e:

            logger.error(
                f"Update Error: {e}"
            )

            return 0

    # ------------------------------------------------

    def delete_one(
        self,
        collection_name,
        query
    ):

        try:

            collection = self.get_collection(
                collection_name
            )

            if collection is None:
                return 0

            result = collection.delete_one(
                query
            )

            return result.deleted_count

        except PyMongoError as e:

            logger.error(
                f"Delete Error: {e}"
            )

            return 0

    # ------------------------------------------------

    def count_documents(
        self,
        collection_name,
        query={}
    ):

        try:

            collection = self.get_collection(
                collection_name
            )

            if collection is None:
                return 0

            return collection.count_documents(
                query
            )

        except PyMongoError:

            return 0

    # ------------------------------------------------

    def close(self):

        if self.client:

            self.client.close()

            logger.info(
                "MongoDB Connection Closed"
            )

# ----------------------------------------------------
# GLOBAL INSTANCE
# ----------------------------------------------------

mongo = MongoDBManager()

# ----------------------------------------------------
# DATASET LOGS
# ----------------------------------------------------

def save_dataset_log(
    filename,
    rows,
    columns
):

    return mongo.insert_one(

        "dataset_logs",

        {

            "filename": filename,

            "rows": rows,

            "columns": columns

        }
    )

# ----------------------------------------------------
# EMISSIONS
# ----------------------------------------------------

def save_emission_report(
    report
):

    return mongo.insert_one(

        "emissions",

        report

    )

# ----------------------------------------------------
# PREDICTIONS
# ----------------------------------------------------

def save_prediction(
    prediction_data
):

    return mongo.insert_one(

        "predictions",

        prediction_data

    )

# ----------------------------------------------------
# ALERTS
# ----------------------------------------------------

def save_alert(
    alert_data
):

    return mongo.insert_one(

        "alerts",

        alert_data

    )

# ----------------------------------------------------
# ESG REPORTS
# ----------------------------------------------------

def save_esg_report(
    report_data
):

    return mongo.insert_one(

        "esg_reports",

        report_data

    )

# ----------------------------------------------------
# INSIGHTS
# ----------------------------------------------------

def save_insight(
    insight_data
):

    return mongo.insert_one(

        "insights",

        insight_data

    )

# ----------------------------------------------------
# BULK STORAGE
# ----------------------------------------------------

def save_many_predictions(
    predictions
):

    return mongo.insert_many(

        "predictions",

        predictions

    )

# ----------------------------------------------------
# FETCH FUNCTIONS
# ----------------------------------------------------

def get_dataset_logs():

    return mongo.find(
        "dataset_logs"
    )

def get_emissions():

    return mongo.find(
        "emissions"
    )

def get_predictions():

    return mongo.find(
        "predictions"
    )

def get_alerts():

    return mongo.find(
        "alerts"
    )

def get_esg_reports():

    return mongo.find(
        "esg_reports"
    )

def get_insights():

    return mongo.find(
        "insights"
    )

# ----------------------------------------------------
# DASHBOARD STATS
# ----------------------------------------------------

def get_database_statistics():

    return {

        "dataset_logs":
            mongo.count_documents(
                "dataset_logs"
            ),

        "emissions":
            mongo.count_documents(
                "emissions"
            ),

        "predictions":
            mongo.count_documents(
                "predictions"
            ),

        "alerts":
            mongo.count_documents(
                "alerts"
            ),

        "esg_reports":
            mongo.count_documents(
                "esg_reports"
            ),

        "insights":
            mongo.count_documents(
                "insights"
            )
    }

# ----------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------

def database_health_check():

    try:

        mongo.client.admin.command(
            "ping"
        )

        return True

    except Exception:

        return False

# ----------------------------------------------------
# TEST
# ----------------------------------------------------

if __name__ == "__main__":

    print(
        "MongoDB Atlas Module Loaded"
    )

    print(
        "Connected:",
        database_health_check()
    )
