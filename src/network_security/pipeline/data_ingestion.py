import sys

from src.network_security.components.data_ingestion import DataIngestion
from src.network_security.config.configuration import TrainingPipelineConfig
from src.network_security.entity.artifact_entity import DataIngestionArtifact
from src.network_security.entity.config_entity import DataIngestionConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger

STAGE_NAME: str = "Data Ingestion Pipeline"
class DataIngestionTrainingPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.stage_name = STAGE_NAME

    def data_ingestion(self) -> None:
        tag: str = f"{self.class_name}::data_ingestion::"
        try:
            config: TrainingPipelineConfig = TrainingPipelineConfig()
            logger.info(f"{tag}::Configuration object created")

            data_ingestion_config: DataIngestionConfig = DataIngestionConfig(config)
            logger.info(f"{tag}::Data ingestion configuration obtained")

            data_ingestion: DataIngestion = DataIngestion(data_ingestion_config)
            logger.info(f"{tag}::Data ingestion object created")

            logger.info(f"{tag}::Running the data ingestion pipeline")

            data_ingestion_artifact: DataIngestionArtifact = data_ingestion.initiate_data_ingestion()
            logger.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            logger.info(f"{tag}::Data ingestion completed successfully")
        except Exception as e:
            logger.error(f"{tag}::Error running the data ingestion pipeline: {e}")
            raise CustomException(e, sys)