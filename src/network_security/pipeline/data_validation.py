import sys

from src.network_security.components.data_validation import DataValidation
from src.network_security.config.configuration import TrainingPipelineConfig
from src.network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.network_security.entity.config_entity import DataValidationConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger

STAGE_NAME: str = "Data Validation Pipeline"
class DataValidationTrainingPipeline:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact):
        self.class_name = self.__class__.__name__
        self.stage_name = STAGE_NAME
        self.data_ingestion_artifact = data_ingestion_artifact

    def data_validation(self) -> DataValidationArtifact:
        tag: str = f"{self.class_name}::data_validation::"
        try:
            config: TrainingPipelineConfig = TrainingPipelineConfig()
            logger.info(f"{tag}::Configuration object created")

            data_validation_config: DataValidationConfig = DataValidationConfig(config)
            logger.info(f"{tag}::Data validation configuration obtained")

            data_validation: DataValidation = DataValidation(self.data_ingestion_artifact, data_validation_config)
            logger.info(f"{tag}::Data validation object created")

            logger.info(f"{tag}::Running the data validation pipeline")

            data_validation_artifact: DataValidationArtifact = data_validation.initiate_data_validation()
            logger.info(f"Data Validation Artifact: {data_validation_artifact}")
            logger.info(f"{tag}::Data validation completed successfully")
            return data_validation_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the data validation pipeline: {e}")
            raise CustomException(e, sys)