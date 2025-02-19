import sys
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from dotenv import load_dotenv
# Fixing the ImportError
# ImportError: cannot import name 'MutableMapping' from 'collections'
# add this before MongoClient import
import collections

from src.network_security.utils.environment import get_mongodb_uri

# Fixing the ImportError
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
collections.Sequence = collections.abc.Sequence
# add fix before importing MongoClient
from pymongo.mongo_client import MongoClient

class MongoDBConnector:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.client = None

    def load_env(self):
        """Loads environment variables from a .env file."""
        load_dotenv()

    def get_mongodb_uri(self):
        """Retrieves the MongoDB URI from environment variables."""
        return get_mongodb_uri()

    def create_mongo_client(self, uri):
        """Creates and returns a MongoDB client."""
        self.client = MongoClient(uri)

    def ping_mongo_client(self):
        """Pings the MongoDB client to confirm connection."""
        tag: str = f"[{self.class_name}][{self.ping_mongo_client.__name__}]::"
        try:
            self.client.admin.command('ping')
            logger.info(f"{tag}>>>>>>>>>> MongoDB connection successful! <<<<<<<<<<")
        except Exception as e:
            logger.error(f"An error occurred while trying to ping your deployment: {e}")
            raise CustomException(e, sys)

    def connect(self):
        self.load_env()
        uri = self.get_mongodb_uri()
        self.create_mongo_client(uri)
        self.ping_mongo_client()

if __name__ == "__main__":
    connector = MongoDBConnector()
    connector.connect()