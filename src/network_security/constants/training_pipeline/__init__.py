import os
import sys
import numpy as np
import pandas as pd
from dvc.api import artifacts_show

from src.network_security.constants import database_name, collection_name, data_file_name

# COMMON CONSTANTS
target_column: str = "Result"
pipeline_name: str = "network_security"
artifact_dir: str = "artifacts"
file_name: str = data_file_name

train_file_name: str = "train_data.csv"
test_file_name: str = "test_data.csv"

# DATA INGESTION CONSTANTS
data_ingestion_collection_name: str = collection_name
data_ingestion_database_name: str = database_name
data_ingestion_dir_name: str = "data_ingestion"
data_ingestion_feature_store_dir_name: str = "feature_store"
data_ingestion_ingested_data_dir_name: str = "ingested"
data_ingestion_train_test_split_ration: float = 0.2
