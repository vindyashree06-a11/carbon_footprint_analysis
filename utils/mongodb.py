from pymongo import MongoClient
from datetime import datetime
import os


class MongoDBManager:

    def __init__(
        self,
        uri=None,
        database=None
    ):

        self.uri = uri or os.getenv("MONGO_URI")

        self.database = database or os.getenv(
            "MONGO_DB_NAME",
            "steel_esg"
        )

        self.client = MongoClient(
            self.uri,
            serverSelectionTimeoutMS=5000
        )

        self.db = self.client[self.database]

        # Verify Atlas Connection
        self.client.admin.command("ping")

    # ===================================
    # GENERIC METHODS
    # ===================================

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

    # ===================================
    # DATASET LOGS
    # ===================================

    def insert_dataset_log(
        self,
        document
    ):

        return (
            self.db["dataset_logs"]
            .insert_one(document)
        )

    # ===================================
    # PREDICTIONS
    # ===================================

    def save_prediction(
        self,
        document
    ):

        return (
            self.db["predictions"]
            .insert_one(document)
        )

    # ===================================
    # ALERTS
    # ===================================

    def save_alert(
        self,
        document
    ):

        return (
            self.db["alerts"]
            .insert_one(document)
        )

    # ===================================
    # ESG REPORTS
    # ===================================

    def save_esg_report(
        self,
        document
    ):

        return (
            self.db["esg_reports"]
            .insert_one(document)
        )

    # ===================================
    # FORECASTS
    # ===================================

    def save_forecast(
        self,
        document
    ):

        return (
            self.db["forecasts"]
            .insert_one(document)
        )

    # ===================================
    # MODEL SCORES
    # ===================================

    def save_model_score(
        self,
        document
    ):

        return (
            self.db["model_scores"]
            .insert_one(document)
        )

    # ===================================
    # FUTURE SCENARIOS
    # ===================================

    def save_scenario(
        self,
        document
    ):

        return (
            self.db["future_scenarios"]
            .insert_one(document)
        )

    # ===================================
    # MONTE CARLO
    # ===================================

    def save_simulation(
        self,
        document
    ):

        return (
            self.db["simulation_results"]
            .insert_one(document)
        )

    # ===================================
    # DIGITAL TWIN
    # ===================================

    def save_digital_twin(
        self,
        document
    ):

        return (
            self.db["digital_twin"]
            .insert_one(document)
        )

    # ===================================
    # HEALTH CHECK
    # ===================================

    def health_check(self):

        try:

            self.client.admin.command("ping")

            return True

        except:

            return False
