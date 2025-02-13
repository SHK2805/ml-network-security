import sys
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from src.network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.network_security.pipeline.data_ingestion import DataIngestionTrainingPipeline
from src.network_security.pipeline.data_validation import DataValidationTrainingPipeline


class RunPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__

    def run_data_ingestion_pipeline(self) -> DataIngestionArtifact:
        tag: str = f"{self.class_name}::run_data_ingestion_pipeline::"
        try:
            data_ingestion_pipeline: DataIngestionTrainingPipeline = DataIngestionTrainingPipeline()
            logger.info(f"[STARTED]>>>>>>>>>>>>>>>>>>>> {data_ingestion_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<")
            logger.info(f"{tag}::Running the data ingestion pipeline")
            data_ingestion_artifact = data_ingestion_pipeline.data_ingestion()
            logger.info(f"{tag}::Data ingestion pipeline completed")
            logger.info(
                f"[COMPLETE]>>>>>>>>>>>>>>>>>>>> {data_ingestion_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<\n\n\n")
            return data_ingestion_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the data ingestion pipeline: {e}")
            raise CustomException(e, sys)

    def run_data_validation_pipeline(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        tag: str = f"{self.class_name}::run_data_validation_pipeline::"
        try:
            data_validation_pipeline: DataValidationTrainingPipeline = DataValidationTrainingPipeline(data_ingestion_artifact)
            logger.info(f"[STARTED]>>>>>>>>>>>>>>>>>>>> {data_validation_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<")
            logger.info(f"{tag}::Running the data validation pipeline")
            data_validation_artifact = data_validation_pipeline.data_validation()
            logger.info(f"{tag}::Data validation pipeline completed")
            logger.info(
                f"[COMPLETE]>>>>>>>>>>>>>>>>>>>> {data_validation_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<\n\n\n")
            return data_validation_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the data validation pipeline: {e}")
            raise CustomException(e, sys)

    def run(self) -> None:
        data_ingestion_artifact: DataIngestionArtifact = self.run_data_ingestion_pipeline()
        data_validation_artifact: DataValidationArtifact = self.run_data_validation_pipeline(data_ingestion_artifact)

if __name__ == "__main__":
    try:
        # Run the pipelines
        run_pipeline = RunPipeline()
        run_pipeline.run()
    except Exception as ex:
        logger.error(f"Error running the pipeline: {ex}")
        raise CustomException(ex, sys)