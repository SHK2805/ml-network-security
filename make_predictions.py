import os
import sys
from datetime import datetime

import certifi
import pandas as pd
from dotenv import load_dotenv

from src.network_security.constants import predictions_folder_name
from src.network_security.constants.training_pipeline import data_ingestion_database_name, \
    data_ingestion_collection_name
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from src.network_security.prediction.prediction import PredictionPipeline

# Fixing the ImportError
# ImportError: cannot import name 'MutableMapping' from 'collections'
# add this before MongoClient import
import collections
from src.network_security.utils.environment import get_mongodb_uri, get_mongodb_name

# Fixing the ImportError
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
collections.Sequence = collections.abc.Sequence
# add fix before importing MongoClient
from pymongo.mongo_client import MongoClient
import pymongo


ca = certifi.where()
load_dotenv()
mongo_db_url = get_mongodb_uri()
mongo_db_name = get_mongodb_name()

# mongodb client
mongodb_client = MongoClient(mongo_db_url, tlsCAFile=ca)
# mongodb database
mongodb_database = mongodb_client[data_ingestion_database_name]
mongodb_collection = mongodb_database[data_ingestion_collection_name]


def make_predictions():
    try:
        # read the file
        data_file_path = "phishingdata/testData.csv"
        if not os.path.exists(data_file_path):
            logger.error(f"File not found: {data_file_path}")
            raise FileNotFoundError(f"File not found: {data_file_path}")
        df = pd.read_csv(data_file_path)
        logger.info(f"Data read successfully: {df.shape}")

        # make the predictions
        prediction_obj = PredictionPipeline()
        prediction_df = prediction_obj.predict(df)
        logger.info(f"Predictions made successfully: {prediction_obj.get_shape()}")

        # convert to csv
        if not os.path.exists(predictions_folder_name):
            logger.info(f"Creating folder {predictions_folder_name}")
            os.makedirs(predictions_folder_name)
        predictions_file_path = os.path.join(predictions_folder_name, "predictions.csv")
        prediction_obj.save_csv(predictions_file_path)
        logger.info(f"Predictions saved successfully: {predictions_file_path}")

        # write predictions to mongodb
        # create a new collection
        collection_name = f"predictions_{datetime.now().strftime('%d%m%Y%H%M%S')}"
        mongodb_collection_predictions = mongodb_database[collection_name]
        prediction_obj.insert_into_mongodb(mongodb_collection_predictions)
        logger.info(f"Predictions inserted into MongoDB collection: {collection_name}")
    except Exception as e:
        logger.error(f"Error in making predictions: {e}")
        raise CustomException(e, sys)

if __name__ == "__main__":
    make_predictions()
