import sys

from src.network_security.components.data_ingestion import DataIngestion
from src.network_security.config.configuration import TrainingPipelineConfig
from src.network_security.entity.artifact_entity import DataIngestionArtifact
from src.network_security.entity.config_entity import DataIngestionConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger

if __name__ == '__main__':
    try:
        logger.info("Starting the application")
        training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()
        data_ingestion_config: DataIngestionConfig = DataIngestionConfig(training_pipeline_config)
        data_ingestion: DataIngestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact: DataIngestionArtifact =  data_ingestion.initiate_data_ingestion()
        logger.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
        logger.info("Completed the application")

    except Exception as e:
        raise CustomException(e, sys)