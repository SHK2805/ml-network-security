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
        self.aws_bucket_path = f"s3://{config.s3_bucket_name}/artifact/{config.s3_artifact_dir}/"


    def sync_artifact_to_s3(self):
        """Sync the artifact to S3."""
        tag: str = f"{self.class_name}::sync_artifact_to_s3"
        try:
            s3_sync = S3Sync(local_dir=self.config.final_model_dir, aws_bucket_url=self.aws_bucket_path)
            logger.info(f"Artifact uploaded to {self.aws_bucket_path}")
        except Exception as e:
            logger.error(f"{tag}::Error in uploading artifact to S3: {e}")
            raise CustomException(e, sys)