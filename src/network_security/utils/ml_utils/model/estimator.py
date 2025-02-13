import os
import sys
from src.network_security.constants.training_pipeline import (model_trainer_saved_model_dir,
                                                              model_trainer_trained_model_file_name)
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger

class NetworkSecurityModel:
    def __init__(self, preprocessor, model):
        try:
            self.class_name = self.__class__.__name__
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            logger.error(f"Error in initializing NetworkSecurityModel: {str(e)}")
            raise CustomException(e, sys)

    def predict(self, x):
        try:
            tag: str = f"{self.class_name}::predict"
            x_transform = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transform)
            return y_pred
        except Exception as e:
            logger.error(f"Error in predicting: {str(e)}")
            raise CustomException(e, sys)