import os
import sys
import json
from pathlib import Path
import certifi  # Provides Mozilla's root CA bundle for SSL verification
import pandas as pd
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from src.network_security.constants import database_name, collection_name, data_file_name, data_file_folder_name

# Fixing the ImportError
import collections
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
collections.Sequence = collections.abc.Sequence

class NetworkDataExtract:
    def __init__(self, input_database_name=database_name, input_collection_name=collection_name):
        self.class_name = self.__class__.__name__
        self.client = None
        self.database_name = input_database_name
        self.collection_name = input_collection_name
        self.collection = None
        self.database = None
        self.records = None
        try:
            self.load_env()
            self.mongo_uri = self.get_mongodb_uri()
        except Exception as e:
            logger.error(f"{self.class_name}::Error in initializing class: {e}")
            raise CustomException(e, sys)

    def load_env(self):
        """Loads environment variables from a .env file."""
        load_dotenv()

    def get_mongodb_uri(self):
        """Retrieves the MongoDB URI from environment variables."""
        return os.getenv("ATLAS_MONGODB_URI")

    def read_csv(self, file_path):
        tag: str = self.class_name + "::read_csv"
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            logger.info(f"{tag}::CSV file read successfully: {file_path}")
            return df
        except Exception as e:
            logger.error(f"{tag}::Error in reading CSV file: {e}")
            raise CustomException(e, sys)

    def cv_to_json(self, file_path):
        tag: str = self.class_name + "::cv_to_json"
        try:
            df = self.read_csv(file_path)
            records = json.loads(df.to_json(orient='records'))
            logger.info(f"{tag}::Dataframe converted to JSON successfully.")
            return records
        except Exception as e:
            logger.error(f"{tag}::Error in converting dataframe to JSON: {e}")
            raise CustomException(e, sys)

    def connect_to_mongodb(self):
        """Creates a MongoDB client and connects to the database."""
        tag: str = self.class_name + "::connect_to_mongodb"
        try:
            self.client = MongoClient(self.mongo_uri)
            self.database = self.client[self.database_name]
            self.collection = self.database[self.collection_name]
            logger.info(f"{tag}::Connected to MongoDB database: {self.database_name}")
        except Exception as e:
            logger.error(f"{tag}::Error in connecting to MongoDB: {e}")
            raise CustomException(e, sys)

    def insert_data_mongodb(self, records):
        tag: str = self.class_name + "::insert_data_mongodb"
        try:
            self.collection.insert_many(records)
            count = self.collection.count_documents({})
            logger.info(f"{tag}::Total records inserted into MongoDB: {count}")
            return count
        except Exception as e:
            logger.error(f"{tag}::Error in inserting data into MongoDB: {e}")
            raise CustomException(e, sys)
        finally:
            if self.client:
                self.client.close()
                logger.info(f"{tag}::MongoDB connection closed.")

    def process(self, file_path):
        records = self.cv_to_json(file_path)
        self.connect_to_mongodb()
        count = self.insert_data_mongodb(records)
        logger.info(f"{self.class_name}::Records inserted into MongoDB successfully. Total records: {count}")
        return count

def main():
    tag: str = "push_data_mongodb::main"
    try:
        file_path = os.path.join(Path(__file__).parent.parent.parent.parent, Path(data_file_folder_name, data_file_name))
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{tag}::File not found: {file_path}")
        database_name = "phishing_data"
        collection_name = "phishing_data"

        obj = NetworkDataExtract()
        count = obj.process(file_path)
        logger.info(f"{tag}::Records inserted into MongoDB successfully. Total records: {count}")
    except Exception as e:
        logger.error(f"{tag}::Error in pushing data into MongoDB: {e}")
        raise CustomException(e, sys)

if __name__ == "__main__":
    main()
