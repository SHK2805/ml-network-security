import os.path
from src.network_security.constants import training_pipeline
from src.network_security.config.configuration import TrainingPipelineConfig


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.class_name = self.__class__.__name__
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.data_ingestion_dir_name)
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.data_ingestion_feature_store_dir_name, training_pipeline.file_name)
        self.training_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.data_ingestion_ingested_data_dir_name, training_pipeline.train_file_name)
        self.testing_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.data_ingestion_ingested_data_dir_name, training_pipeline.test_file_name)
        # folder structure
        # artifacts
        #   - data_ingestion
        #       - feature_store
        #           - phisingData.csv
        #       - ingested
        #           - train_data.csv
        #           - test_data.csv

        self.collection_name = training_pipeline.data_ingestion_collection_name
        self.database_name = training_pipeline.data_ingestion_database_name
        self.train_test_split_ratio = training_pipeline.data_ingestion_train_test_split_ration

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.class_name = self.__class__.__name__
        # folders
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.data_validation_dir_name)
        self.valid_data_dir = os.path.join(self.data_validation_dir, training_pipeline.data_validation_valid_dir)
        self.invalid_data_dir = os.path.join(self.data_validation_dir, training_pipeline.data_validation_invalid_dir)
        # files
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.train_file_name)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.test_file_name)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.train_file_name)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.test_file_name)
        # drift report
        self.drift_report_dir = os.path.join(self.data_validation_dir, training_pipeline.data_validation_drift_report_dir)
        self.drift_report_file = os.path.join(self.drift_report_dir, training_pipeline.data_validation_drift_report_file_name)
        # folder structure
        # - artifacts
        #   - data_validation
        #       - validated
        #           - train_data.csv
        #           - test_data.csv
        #       - invalid
        #           - train_data.csv
        #           - test_data.csv
        #       - drift_report
        #           - drift_report.yaml


