import sys
from typing import Any

import pandas as pd
import os

from src.network_security.constants.training_pipeline import schema_file_path
from src.network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.network_security.entity.config_entity import DataValidationConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from scipy.stats import ks_2samp
from src.network_security.utils.main_utils.utils import read_yaml, write_yaml


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

    def validate_numerical_columns(self, data: pd.DataFrame) -> bool:
        tag: str = f"{self.class_name}::validate_numerical_columns::"
        try:
            numerical_columns = self._schema_config['numerical_columns']
            data_columns_list = list(data.columns)
            missing_columns = [col for col in numerical_columns if col not in data_columns_list]
            if missing_columns:
                logger.error(f"{tag}::Missing numerical columns in data: {missing_columns}")
                return False
            logger.info(f"{tag}::All numerical columns are validated")
            return True
        except Exception as e:
            logger.error(f"{tag}::Error validating numerical columns: {e}")
            raise CustomException(e, sys)

    def validate_train_test_data(self, train_data: pd.DataFrame, test_data: pd.DataFrame) -> bool:
        tag: str = f"{self.class_name}::validate_data::"
        # validate number of columns in train and test data
        logger.info(f"{tag}::Validating number of columns in train and test data")
        is_train_test_columns_numbers_same = self.validate_number_of_columns_in_data(train_data, test_data)
        if not is_train_test_columns_numbers_same:
            logger.error(f"{tag}::Data validation failed. Train and Test data have different number of columns")

        logger.info(f"{tag}::Validating number of columns in train data")
        is_columns_numbers_same_train = self.validate_number_of_columns(train_data)
        if not is_columns_numbers_same_train:
            logger.error(f"{tag}::Data validation failed. Train data has different number of columns")

        logger.info(f"{tag}::Validating number of columns in test data")
        is_columns_numbers_same_test = self.validate_number_of_columns(test_data)
        if not is_columns_numbers_same_test:
            logger.error(f"{tag}::Data validation failed. Test data has different number of columns")

        logger.info(f"{tag}::Validating numerical columns in train data")
        is_numerical_columns_same_train = self.validate_numerical_columns(train_data)
        if not is_numerical_columns_same_train:
            logger.error(f"{tag}::Data validation failed. Train data numerical columns are not same as schema")

        logger.info(f"{tag}::Validating numerical columns in test data")
        is_numerical_columns_same_test = self.validate_numerical_columns(test_data)
        if not is_numerical_columns_same_test:
            logger.error(f"{tag}::Data validation failed. Test data numerical columns are not same as schema")

        return (is_train_test_columns_numbers_same and
                  is_columns_numbers_same_train and
                  is_columns_numbers_same_test and
                  is_numerical_columns_same_train and
                  is_numerical_columns_same_test)

    def generate_drift_report(self, reference_data: pd.DataFrame, new_data: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
        """
        Generate a drift report comparing two datasets.

        Parameters:
            reference_data (pd.DataFrame): The reference dataset (e.g., training data).
            new_data (pd.DataFrame): The new dataset to compare against the reference.

        Returns:
            pd.DataFrame: A drift report showing the KS statistic and p-value for each feature.
        """
        tag = f"{self.class_name}::generate_drift_report::"
        report = pd.DataFrame(columns=['Feature', 'KS Statistic', 'P-Value', 'Drift Detected'])
        threshold = 0.005
        drift_detected_overall = False

        report_list = []

        for column in reference_data.columns:
            if column in new_data.columns:
                stat, p_value = ks_2samp(reference_data[column], new_data[column])
                drift_detected = p_value < threshold
                drift_detected_overall = drift_detected_overall or drift_detected
                report_list.append({
                    'Feature': column,
                    'KS Statistic': stat,
                    'P-Value': p_value,
                    'Drift Detected': drift_detected
                })

        report = pd.concat([report, pd.DataFrame(report_list)], ignore_index=True)
        status = not drift_detected_overall
        logger.info(f"{tag}::Drift report generated with status: {status}")
        return report, status

    def save_report_to_yaml(self, report: pd.DataFrame, status: bool, file_name: str = None):
        """
        Save the drift report to a YAML file.

        Parameters:
            report (pd.DataFrame): The drift report as a DataFrame.
            status (bool): The overall status indicating whether drift was detected.
            file_name (str): The name of the YAML file.
        """
        tag = f"{self.class_name}::save_report_to_yaml::"
        report_dict = report.to_dict(orient='records')
        data = {
            'status': status,
            'report': report_dict
        }
        # create directory if not exists
        drift_dir = self.data_validation_config.drift_report_dir
        drift_file_name = file_name
        if drift_file_name is None:
            drift_file_name = self.data_validation_config.drift_report_file
        os.makedirs(drift_dir, exist_ok=True)
        logger.info(f"{tag}::Folder created: {drift_dir}")
        write_yaml(file_path=drift_file_name, content=data)
        logger.info(f"{tag}::Drift report saved to {drift_file_name}")


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

            # validate train and test data
            data_status = self.validate_train_test_data(train_data, test_data)
            if not data_status:
                logger.error(f"{tag}::Data validation failed.")
                logger.error(f"{tag}::Data columns are not same as schema")
                # raise CustomException("Data validation failed", sys)

            logger.info(f"{tag}::Data validation for columns completed successfully")

            # it there is no drift then the drift_status will be True else False
            drift_report, drift_status = self.generate_drift_report(train_data, test_data)
            self.save_report_to_yaml(drift_report, drift_status)
            logger.info(f"{tag}::Drift report saved successfully with status: {drift_status}")

            # save test and train data
            valid_data_dir = self.data_validation_config.valid_data_dir
            # create directory if not exists
            os.makedirs(valid_data_dir, exist_ok=True)
            logger.info(f"{tag}::Folder created: {valid_data_dir}")
            train_data.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_data.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            logger.info(f"{tag}::Validated data saved to csv successfully")

            # create data validation artifact
            status = data_status and drift_status
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                drift_report_file_path=self.data_validation_config.drift_report_file,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path)

            return data_validation_artifact
        except Exception as e:
            logger.error(f"{tag}::Error running the data validation pipeline: {e}")
            raise CustomException(e, sys)


