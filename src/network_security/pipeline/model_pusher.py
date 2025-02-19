import sys

from src.network_security.components.model_pusher import ModelPusher
from src.network_security.config.configuration import TrainingPipelineConfig
from src.network_security.entity.config_entity import ModelPusherConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger

STAGE_NAME: str = "Model Pusher Pipeline"
class ModelPusherTrainingPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.stage_name = STAGE_NAME

    def model_pusher(self) -> None:
        tag: str = f"[{self.class_name}][{self.model_pusher.__name__}]::"
        try:
            logger.info(f"{tag}::Model pusher pipeline started")
            config: TrainingPipelineConfig = TrainingPipelineConfig()
            logger.info(f"{tag}::Configuration object created")

            model_pusher_config: ModelPusherConfig = ModelPusherConfig(config)
            logger.info(f"{tag}::Model pusher configuration obtained")

            model_pusher = ModelPusher(config=model_pusher_config)
            logger.info(f"{tag}::Model pusher object created")

            logger.info(f"{tag}::Running the model pusher pipeline")
            model_pusher.push()
            logger.info(f"{tag}::Model pusher pipeline completed")
        except Exception as e:
            logger.error(f"{tag}::Error running the model training pipeline: {e}")
            raise CustomException(e, sys)