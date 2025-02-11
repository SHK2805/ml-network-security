import os
import sys

import numpy as np
import pandas as pd
# load from env
from dotenv import load_dotenv

from src.network_security.config.configuration import TrainingPipelineConfig
from src.network_security.entity.config_entity import DataIngestionConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from src.network_security.utils.environment import get_mongodb_uri

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
import pymongo

load_dotenv()

# read mongodb url
MONGO_DB_URL = get_mongodb_uri()

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.class_name = self.__class__.__name__
            self.data_ingestion_config = data_ingestion_config
            self.mongodb_client = None
        except Exception as e:
            logger.error(f"Error in data ingestion: {e}")
            raise CustomException(e, sys)

    def export_collection_as_dataframe(self):
        """Export the collection as a dataframe."""
        tag = f"{self.class_name}::export_collection_as_dataframe"
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongodb_client = MongoClient(MONGO_DB_URL)
            # read all the data in the collection
            collection = self.mongodb_client[database_name][collection_name]
            # convert the collection to a dataframe
            df = pd.DataFrame(list(collection.find()))
            # _id column will be added by default. We need to remove it
            # remove the _id column
            # check if _id column exists
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            # replace na
            df.replace({"na":np.nan}, inplace=True)

            return df
        except Exception as e:
            logger.error(f"{tag}::Error in exporting collection as dataframe: {e}")
            raise CustomException(e, sys)

    def export_data_into_feature_store(self, df: pd.DataFrame):
        """Export the data into the feature store."""
        tag = f"{self.class_name}::export_data_into_feature_store"
        try:
           feature_store_file_path = self.data_ingestion_config.feature_store_file_path
           # create the dir if not exists
           feature_store_dir = os.path.dirname(feature_store_file_path)
           os.makedirs(feature_store_dir, exist_ok=True)
           df.to_csv(feature_store_file_path, index=False, header=True)
           return df
        except Exception as e:
            logger.error(f"{tag}::Error in exporting data into feature store: {e}")
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        tag = f"{self.class_name}::initiate_data_ingestion"
        try:
            # read the collection from MongoDB as a dataframe
            df = self.export_collection_as_dataframe()
        except Exception as e:
            logger.error(f"{tag}::Error in initiating data ingestion: {e}")
            raise CustomException(e, sys)


