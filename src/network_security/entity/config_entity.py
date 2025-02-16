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

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.class_name = self.__class__.__name__
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,
                                                         training_pipeline.data_transformation_dir_name)
        self.transformed_train_file_path = os.path.join(self.data_transformation_dir,
                                                             training_pipeline.data_transformation_transformed_data_dir,
                                                             training_pipeline.data_transformation_train_file_name)
        self.transformed_test_file_path = os.path.join(self.data_transformation_dir,
                                                            training_pipeline.data_transformation_transformed_data_dir,
                                                            training_pipeline.data_transformation_test_file_name)
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir,
                                                              training_pipeline.data_transformation_transformed_object_dir,
                                                              training_pipeline.preprocessing_object_file_name)
        self.transformed_final_preprocessing_object_dir = os.path.join(training_pipeline_config.artifact_dir,
                                            training_pipeline.data_transformation_final_preprocessing_object_dir)
        self.final_transformed_reprocessing_object_file_path = os.path.join(self.transformed_final_preprocessing_object_dir,
                                                  training_pipeline.data_transformation_final_preprocessing_object_file_name)
        # folder structure
        # - artifacts
        #   - data_transformation
        #       - transformed
        #           - train.npy
        #           - test.npy
        #       - transformed_object
        #           - preprocessing.pkl

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.class_name = self.__class__.__name__
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.model_trainer_dir_name)
        self.trained_model_file_path = os.path.join(self.model_trainer_dir, training_pipeline.model_trainer_trained_model_dir,
                                                        training_pipeline.model_trainer_trained_model_file_name)
        self.final_model_dir = os.path.join(training_pipeline_config.artifact_dir,
                                            training_pipeline.model_trainer_final_model_dir)
        self.final_model_file_path = os.path.join(self.final_model_dir,
                                                    training_pipeline.model_trainer_final_model_file_name)

        self.expected_accuracy = training_pipeline.model_trainer_expected_score
        self.overfitting_underfitting_threshold = training_pipeline.model_trainer_over_fitting_under_fitting_threshold

        # folder structure
        # - artifacts
        #   - model_trainer
        #       - trained_model
        #           - model.pkl
        #       - final_models
        #           - model.pkl
        #           - preprocessing.pkl
        #       - saved_models
        #           - model.pkl



