import sys

from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from src.network_security.pipeline.data_ingestion import DataIngestionTrainingPipeline


class RunPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.data_ingestion_pipeline: DataIngestionTrainingPipeline = DataIngestionTrainingPipeline()

    def run_data_ingestion_pipeline(self) -> None:
        tag: str = f"{self.class_name}::run_data_ingestion_pipeline::"
        try:
            logger.info(f"[STARTED]>>>>>>>>>>>>>>>>>>>> {self.data_ingestion_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<")
            logger.info(f"{tag}::Running the data ingestion pipeline")
            self.data_ingestion_pipeline.data_ingestion()
            logger.info(f"{tag}::Data ingestion pipeline completed")
            logger.info(
                f"[COMPLETE]>>>>>>>>>>>>>>>>>>>> {self.data_ingestion_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<\n\n\n")
        except Exception as e:
            logger.error(f"{tag}::Error running the data ingestion pipeline: {e}")
            raise CustomException(e, sys)

    def run(self) -> None:
        self.run_data_ingestion_pipeline()

if __name__ == "__main__":
    try:
        # Run the pipelines
        run_pipeline = RunPipeline()
        run_pipeline.run()
    except Exception as ex:
        logger.error(f"Error running the pipeline: {ex}")
        raise CustomException(ex, sys)