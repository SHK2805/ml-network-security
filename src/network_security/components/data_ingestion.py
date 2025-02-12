import os
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# load from env
from dotenv import load_dotenv

from src.network_security.entity.artifact_entity import DataIngestionArtifact
from src.network_security.entity.config_entity import DataIngestionConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger

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
            logger.info(f"{tag}::Obtained Dataframe shape: {df.shape}")
            # _id column will be added by default. We need to remove it
            # remove the _id column
            # check if _id column exists
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
                logger.info(f"{tag}::Removed _id column")

            # replace na
            df.replace({"na":np.nan}, inplace=True)
            logger.info(f"{tag}::Replaced 'na' with np.nan")

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
           logger.info(f"{tag}::Created folder: {feature_store_dir}")
           df.to_csv(feature_store_file_path, index=False, header=True)
           logger.info(f"{tag}::Exported data into feature store: {feature_store_file_path}")
           return df
        except Exception as e:
            logger.error(f"{tag}::Error in exporting data into feature store: {e}")
            raise CustomException(e, sys)

    def export_data_into_train_test(self, df: pd.DataFrame):
        """Export the data into the train and test files."""
        tag = f"{self.class_name}::export_data_into_train_test"
        try:
            train_test_split_ratio = self.data_ingestion_config.train_test_split_ratio
            training_file_path = self.data_ingestion_config.training_file_path
            testing_file_path = self.data_ingestion_config.testing_file_path
            # create the dir if not exists
            train_test_dir = os.path.dirname(training_file_path)
            os.makedirs(train_test_dir, exist_ok=True)
            logger.info(f"{tag}::Created folder: {train_test_dir}")
            # split the data into train and test
            train_df, test_df = train_test_split(df, test_size=train_test_split_ratio, random_state=42)
            logger.info(f"{tag}::Split the data into train and test with ratio: {train_test_split_ratio}")
            # save the train and test data
            train_df.to_csv(training_file_path, index=False, header=True)
            test_df.to_csv(testing_file_path, index=False, header=True)
            logger.info(f"{tag}::Exported data into train file: {training_file_path} and test file: {testing_file_path}")
            return training_file_path, testing_file_path
        except Exception as e:
            logger.error(f"{tag}::Error in exporting data into train and test files: {e}")
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        tag = f"{self.class_name}::initiate_data_ingestion"
        try:
            logger.info(f"{tag}::Initiated data ingestion")
            # read the collection from MongoDB as a dataframe
            dataframe = self.export_collection_as_dataframe()
            logger.info(f"{tag}::Completed exporting collection as dataframe")

            df = self.export_data_into_feature_store(dataframe)
            logger.info(f"{tag}::Completed exporting data into feature store")

            training_file_path, testing_file_path = self.export_data_into_train_test(df)
            logger.info(f"{tag}::Completed exporting data into train and test files")

            logger.info(f"{tag}::Completed data ingestion")
            return DataIngestionArtifact(train_file_path=training_file_path, test_file_path=testing_file_path)
        except Exception as e:
            logger.error(f"{tag}::Error in initiating data ingestion: {e}")
            raise CustomException(e, sys)


