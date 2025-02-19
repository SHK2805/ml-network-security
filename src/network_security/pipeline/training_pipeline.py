import os
import sys

from src.network_security.components.model_pusher import ModelPusher
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger

# import components
from src.network_security.components.data_ingestion import DataIngestion
from src.network_security.components.data_validation import DataValidation
from src.network_security.components.data_transformation import DataTransformation
from src.network_security.components.model_trainer import ModelTrainer

# import config
from src.network_security.entity.config_entity import (TrainingPipelineConfig,
                                                       DataIngestionConfig,
                                                       DataValidationConfig,
                                                       DataTransformationConfig,
                                                       ModelTrainerConfig, ModelPusherConfig)

# import artifact entity
from src.network_security.entity.artifact_entity import (DataIngestionArtifact,
                                                        DataValidationArtifact,
                                                        DataTransformationArtifact,
                                                        ModelTrainerArtifact)

class TrainingPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.stage_name = "Training Pipeline"
        self.config: TrainingPipelineConfig = TrainingPipelineConfig()

    def run_data_ingestion_pipeline(self) -> DataIngestionArtifact:
        tag: str = f"{self.class_name}::run_data_ingestion_pipeline::"
        try:
            logger.info(f"{tag}::Data ingestion configuration started")
            data_ingestion_config: DataIngestionConfig = DataIngestionConfig(self.config)
            data_ingestion: DataIngestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact: DataIngestionArtifact = data_ingestion.initiate_data_ingestion()
            logger.info(f"{tag}::Data ingestion completed successfully with artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the data ingestion pipeline: {e}")
            raise CustomException(e, sys)

    def run_data_validation_pipeline(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        tag: str = f"{self.class_name}::run_data_validation_pipeline::"
        try:
            logger.info(f"{tag}::Data validation configuration started")
            data_validation_config: DataValidationConfig = DataValidationConfig(self.config)
            data_validation: DataValidation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                                             data_validation_config=data_validation_config)
            data_validation_artifact: DataValidationArtifact = data_validation.initiate_data_validation()
            logger.info(f"{tag}::Data validation completed successfully with artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the data validation pipeline: {e}")
            raise CustomException(e, sys)

    def run_data_transformation_pipeline(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        tag: str = f"{self.class_name}::run_data_transformation_pipeline::"
        try:
            logger.info(f"{tag}::Data transformation configuration started")
            data_transformation_config: DataTransformationConfig = DataTransformationConfig(self.config)
            data_transformation: DataTransformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                                         data_transformation_config=data_transformation_config)
            data_transformation_artifact: DataTransformationArtifact = data_transformation.initiate_data_transformation()
            logger.info(f"{tag}::Data transformation completed successfully with artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the data transformation pipeline: {e}")
            raise CustomException(e, sys)

    def run_model_trainer_pipeline(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        tag: str = f"{self.class_name}::run_model_trainer_pipeline::"
        try:
            logger.info(f"{tag}::Model training configuration started")
            model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(self.config)
            model_trainer: ModelTrainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                                       model_trainer_config=model_trainer_config)
            model_trainer_artifact: ModelTrainerArtifact = model_trainer.initiate_model_trainer()
            logger.info(f"{tag}::Model training completed successfully with artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the model training pipeline: {e}")
            raise CustomException(e, sys)

    def run_pusher_pipeline(self):
        tag: str = f"{self.class_name}::run_pusher_pipeline::"
        try:
            logger.info(f"{tag}::Model pusher configuration started")
            model_pusher_config: ModelPusherConfig = ModelPusherConfig(self.config)
            model_pusher: ModelPusher = ModelPusher(config=model_pusher_config)
            logger.info(f"{tag}::Model pusher object created")
            logger.info(f"{tag}::Running the model pusher pipeline")
            model_pusher.push()
            logger.info(f"{tag}::Model pusher pipeline completed")
        except Exception as e:
            logger.error(f"{tag}::Error running the model pusher pipeline: {e}")
            raise CustomException

    def run_training_pipeline(self):
        tag: str = f"{self.class_name}::run_training_pipeline::"
        try:
            logger.info(f"[STARTED]>>>>>>>>>>>>>>>>>>>> {self.stage_name} <<<<<<<<<<<<<<<<<<<<")
            data_ingestion_artifact = self.run_data_ingestion_pipeline()
            data_validation_artifact = self.run_data_validation_pipeline(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.run_data_transformation_pipeline(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.run_model_trainer_pipeline(data_transformation_artifact=data_transformation_artifact)
            logger.info(f"[COMPLETE]>>>>>>>>>>>>>>>>>>>> {self.stage_name} <<<<<<<<<<<<<<<<<<<<\n\n\n")
            return model_trainer_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the training pipeline: {e}")
            raise CustomException(e, sys)

    def run(self):
        tag: str = f"{self.class_name}::run::"
        try:
            logger.info(f"{tag}::Training pipeline started")
            self.run_training_pipeline()
            self.run_pusher_pipeline()
            logger.info(f"{tag}::Training pipeline completed")
        except Exception as e:
            logger.error(f"{tag}::Error running the training pipeline: {e}")
            raise CustomException(e, sys)