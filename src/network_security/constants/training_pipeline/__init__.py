import os

import numpy as np

from src.network_security.constants import database_name, collection_name, data_file_name

# COMMON CONSTANTS
target_column: str = "Result"
pipeline_name: str = "network_security"
artifact_dir: str = "artifacts"
file_name: str = data_file_name

train_file_name: str = "train_data.csv"
test_file_name: str = "test_data.csv"
schema_file_path: str = os.path.join("data_schema", "schema.yaml")
model_params_file_path: str = os.path.join("model_params", "model_params.yaml")

# DATA INGESTION CONSTANTS
data_ingestion_database_name: str = database_name
data_ingestion_collection_name: str = collection_name
data_ingestion_dir_name: str = "data_ingestion"
data_ingestion_feature_store_dir_name: str = "feature_store"
data_ingestion_ingested_data_dir_name: str = "ingested"
data_ingestion_train_test_split_ration: float = 0.2

# DATA VALIDATION CONSTANTS
data_validation_dir_name: str = "data_validation"
data_validation_valid_dir: str = "validated"
data_validation_invalid_dir: str = "invalid"
data_validation_drift_report_dir: str = "drift_report"
data_validation_drift_report_file_name: str = "drift_report.yaml"

# DATA TRANSFORMATION CONSTANTS
data_transformation_dir_name: str = "data_transformation"
data_transformation_transformed_data_dir: str = "transformed"
data_transformation_transformed_object_dir: str = "transformed_object"
data_transformation_train_file_name = "train_data.npy"
data_transformation_test_file_name = "test_data.npy"
preprocessing_object_file_name = "preprocessing.pkl"
data_transformation_final_preprocessing_object_dir : str = "final_models"
data_transformation_final_preprocessing_object_file_name : str = "preprocessing.pkl"
# this is to replace the missing values in the dataset
# knn imputer is used to replace the missing values
data_transformation_imputer_params: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

# MODEL TRAINER CONSTANTS
model_trainer_dir_name: str = "model_trainer"
model_trainer_trained_model_dir: str = "trained_model"
model_trainer_saved_model_dir: str = "saved_models"
model_trainer_trained_model_file_name: str = "model.pkl"
model_trainer_final_model_dir: str = "final_models"
model_trainer_final_model_file_name: str = "model.pkl"
model_trainer_expected_score: float = 0.6
model_trainer_over_fitting_under_fitting_threshold: float = 0.05

# MODEL PREDICTION CONSTANTS
prediction_final_model_dir: str = "final_models"
prediction_final_preprocessing_object_file_name : str = "preprocessing.pkl"
prediction_final_model_file_name: str = "model.pkl"



