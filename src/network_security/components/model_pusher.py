import os
import sys

from src.network_security.entity.config_entity import ModelPusherConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from src.network_security.utils.cloud_utils.s3 import S3Sync


class ModelPusher:
    def __init__(self, config: ModelPusherConfig):
        """Initialize the ModelPusher with AWS clients."""
        self.class_name = self.__class__.__name__
        self.config = config


    def sync_artifact_to_s3(self):
        """Sync the artifact to S3."""
        tag: str = f"[{self.class_name}][{self.sync_artifact_to_s3.__name__}]::"
        try:
            local_dir = self.config.training_pipeline_config.artifact_dir
            if not os.path.exists(local_dir):
                raise CustomException(f"{tag}::Local directory {local_dir} does not exist", sys)
            aws_bucket_url = f"s3://{self.config.s3_bucket_name}/artifacts/{self.config.training_pipeline_config.timestamp}/"
            s3_sync = S3Sync(local_dir=local_dir, aws_bucket_url=aws_bucket_url)
            s3_sync.sync_to_s3()
            logger.info(f"Artifacts from {local_dir} uploaded to {aws_bucket_url}")
        except Exception as e:
            logger.error(f"{tag}::Error in uploading artifact to S3: {e}")
            raise CustomException(e, sys)

    def sync_model_to_s3(self):
        """Sync the models to S3."""
        tag: str = f"[{self.class_name}][{self.sync_model_to_s3.__name__}]::"
        try:
            local_dir = self.config.final_model_dir
            if not os.path.exists(local_dir):
                raise CustomException(f"{tag}::Local directory {local_dir} does not exist", sys)
            aws_bucket_url = f"s3://{self.config.s3_bucket_name}/models/{self.config.training_pipeline_config.timestamp}/"
            s3_sync = S3Sync(local_dir=local_dir, aws_bucket_url=aws_bucket_url)
            logger.info(f"Models from {local_dir} uploaded to {aws_bucket_url}")
            s3_sync.sync_to_s3()
        except Exception as e:
            logger.error(f"{tag}::Error in uploading artifact to S3: {e}")
            raise CustomException(e, sys)

    def push(self):
        """Push the model and artifacts to S3."""
        self.sync_artifact_to_s3()
        self.sync_model_to_s3()
