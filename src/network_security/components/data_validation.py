import sys
import pandas as pd
import os
from src.network_security.constants.training_pipeline import schema_file_path
from src.network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.network_security.entity.config_entity import DataValidationConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from scipy.stats import ks_2samp
from src.network_security.utils.main_utils.utils import read_yaml


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.class_name = self.__class__.__name__
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(schema_file_path)
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

    def validate_number_of_columns_in_data(self, train_data: pd.DataFrame, test_data: pd.DataFrame) -> bool:
        tag: str = f"{self.class_name}::validate_number_of_columns_in_data::"
        try:
            if train_data.shape[1] == test_data.shape[1]:
                logger.info(f"{tag}::Number of columns in train and test data are same")
                return True
            else:
                logger.error(f"{tag}::Number of columns in train and test data are different")
                logger.error(f"{tag}::Number of columns in train data: {train_data.shape[1]} and test data: {test_data.shape[1]}")
                return False
        except Exception as e:
            logger.error(f"{tag}::Error validating number of columns in train and test data: {e}")
            raise CustomException(e, sys)

    def validate_number_of_columns(self, data: pd.DataFrame) -> bool:
        tag: str = f"{self.class_name}::validate_number_of_columns::"
        try:
            numbers_of_data_columns = len(data.columns)
            numbers_of_data_columns_in_schema = len(self._schema_config['columns'])
            if numbers_of_data_columns == numbers_of_data_columns_in_schema:
                logger.info(f"{tag}::Number of columns in data is same as schema")
                return True
            else:
                logger.error(f"{tag}::Number of columns in data is different from schema")
                logger.error(f"{tag}::Number of columns in data: {numbers_of_data_columns} and schema: {numbers_of_data_columns_in_schema}")
                return False
        except Exception as e:
            logger.error(f"{tag}::Error validating number of columns: {e}")
            raise CustomException(e, sys)

    def validate_columns(self, data: pd.DataFrame) -> bool:
        tag: str = f"{self.class_name}::validate_columns::"
        try:
            columns = data.columns
            schema_columns = self._schema_config['columns']
            if set(columns) == set(schema_columns):
                logger.info(f"{tag}::Columns in data are same as schema")
                return True
            else:
                logger.error(f"{tag}::Columns in data are different from schema")
                logger.error(f"{tag}::Columns in data: {columns} and schema: {schema_columns}")
                return False
        except Exception as e:
            logger.error(f"{tag}::Error validating columns: {e}")
            raise CustomException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        tag: str = f"{self.class_name}::initiate_data_validation::"
        try:
            logger.info(f"{tag}::Initiating data validation")
            # get train and test file path
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read data from train and test file
            train_data = DataValidation.read_data(train_file_path)
            test_data = DataValidation.read_data(test_file_path)

            # validate number of columns in train and test data
            logger.info(f"{tag}::Validating number of columns in train and test data")
            is_columns_numbers_same = self.validate_number_of_columns_in_data(train_data, test_data)
            if not is_columns_numbers_same:
                logger.error(f"{tag}::Data validation failed. Train and Test data have different number of columns")

            logger.info(f"{tag}::Validating number of columns in train data")
            is_columns_numbers_same_train = self.validate_number_of_columns(train_data)
            if not is_columns_numbers_same_train:
                logger.error(f"{tag}::Data validation failed. Train data has different number of columns")

            logger.info(f"{tag}::Validating number of columns in test data")
            is_columns_numbers_same_test = self.validate_number_of_columns(test_data)
            if not is_columns_numbers_same_test:
                logger.error(f"{tag}::Data validation failed. Test data has different number of columns")

            logger.info(f"{tag}::Validating columns in train data")
            is_columns_same_train = self.validate_columns(train_data)
            if not is_columns_same_train:
                logger.error(f"{tag}::Data validation failed. Train data columns are not same as schema")

            logger.info(f"{tag}::Validating columns in test data")
            is_columns_same_test = self.validate_columns(test_data)
            if not is_columns_same_test:
                logger.error(f"{tag}::Data validation failed. Test data columns are not same as schema")

            status = (is_columns_numbers_same and
                      is_columns_numbers_same_train and
                      is_columns_numbers_same_test and
                      is_columns_same_train and
                      is_columns_same_test)

            if not status:
                logger.error(f"{tag}::Data validation failed.")
                logger.error(f"{tag}::Data columns are not same as schema")
                raise CustomException("Data validation failed", sys)

            logger.info(f"{tag}::Data validation completed successfully")
            return data_validation_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the data validation pipeline: {e}")
            raise CustomException(e, sys)


