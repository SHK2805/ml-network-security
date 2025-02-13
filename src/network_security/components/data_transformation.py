import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from src.network_security.constants.training_pipeline import target_column, data_transformation_imputer_params
from src.network_security.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact

from src.network_security.entity.config_entity import DataTransformationConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from src.network_security.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact ,data_transformation_config: DataTransformationConfig):
        try:
            self.class_name = self.__class__.__name__
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        except Exception as e:
            logger.error(f"Error in data transformation: {e}")
            raise CustomException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logger.error(f"Error reading the data: {e}")
            raise CustomException(e, sys) from e

    @staticmethod
    def get_data_transformer(cls) -> Pipeline:
        """
        It initializes the data transformer using KNNImputer object
        :param cls: DataTransformation class object
        :return: Pipeline object
        """
        logger.info(f"DataTransformation::get_data_transformer::Initiating data transformer")
        try:
            KNNImputer(**data_transformation_imputer_params)
        except Exception as e:
            logger.error(f"DataTransformation::get_data_transformer::Error in initiating data transformer: {e}")
            raise CustomException(e, sys) from e


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        tag = f"{self.class_name}::initiate_data_transformation"
        try:
            logger.info(f"{tag}::Initiating data transformation")
            # read train and test data
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # train dataframe split into dependent and independent features
            X_train = train_df.drop(target_column, axis=1)
            y_train = train_df[target_column]
            # replace -1 with 0
            y_train = y_train.replace(-1, 0)

            # test dataframe split into dependent and independent features
            X_test = test_df.drop(target_column, axis=1)
            y_test = test_df[target_column]
            # replace -1 with 0
            y_test = y_test.replace(-1, 0)

            logger.info(f"{tag}::Data transformation complete")
        except Exception as e:
            logger.error(f"{tag}::Error in data transformation: {e}")
            raise CustomException(e, sys)

