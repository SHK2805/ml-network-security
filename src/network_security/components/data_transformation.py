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
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
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
            # the ** operator is used to unpack the dictionary of the hyperparameters
            imputer:KNNImputer = KNNImputer(**data_transformation_imputer_params)
            logger.info(f"DataTransformation::get_data_transformer:: Imputer initiated with hyperparameters: {data_transformation_imputer_params}")
            processor: Pipeline = Pipeline([
                ('imputer', imputer)
            ])
            return processor

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

            # get the data transformer
            processor = DataTransformation.get_data_transformer(self)
            # here we can give fit_transform on X_train,
            # but since we are using a pipeline we gave fit and transform separately,
            # we do not need to do this separately
            processor_object = processor.fit(X_train)
            # the transform object will be used to transform the train and test data
            # this will return the data as an array
            transformed_X_train = processor_object.transform(X_train)
            transformed_X_test = processor_object.transform(X_test)

            # combine the transformed independent features with the dependent features
            transformed_train_data = np.c_[transformed_X_train, np.array(y_train)]
            transformed_test_data = np.c_[transformed_X_test, np.array(y_test)]

            # save the numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, transformed_train_data)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, transformed_test_data)
            save_object(self.data_transformation_config.transformed_object_file_path, processor)
            # save the preprocessing object in final_models folder
            # create the folder if it does not exist
            if not os.path.exists(self.data_transformation_config.transformed_final_preprocessing_object_dir):
                logger.info(f"{tag}::Creating final preprocessing object directory at: "
                            f"{self.data_transformation_config.transformed_final_preprocessing_object_dir}")
                os.makedirs(self.data_transformation_config.transformed_final_preprocessing_object_dir)
            save_object(self.data_transformation_config.final_transformed_reprocessing_object_file_path, processor)

            # preparing artifacts
            artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            logger.info(f"{tag}::Data transformation complete")
            return artifact
        except Exception as e:
            logger.error(f"{tag}::Error in data transformation: {e}")
            raise CustomException(e, sys)

