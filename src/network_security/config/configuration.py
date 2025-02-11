import os
from datetime import datetime

from src.network_security.constants import training_pipeline


class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now().strftime("%d_%m_%Y_%H_%M_%S")):
        self.class_name = self.__class__.__name__
        self.timestamp = timestamp
        self.pipeline = training_pipeline.pipeline_name
        self.artifact_name = training_pipeline.artifact_dir
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)