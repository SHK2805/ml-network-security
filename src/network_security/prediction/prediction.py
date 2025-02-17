import os
import sys
import pandas as pd

from src.network_security.config.configuration import TrainingPipelineConfig
from src.network_security.constants.training_pipeline import (data_transformation_final_preprocessing_object_dir,
                                                              data_transformation_final_preprocessing_object_file_name,
                                                              model_trainer_final_model_dir,
                                                              model_trainer_final_model_file_name, target_column)
from src.network_security.entity.config_entity import ModelPredictionConfig
from src.network_security.logging.logger import logger
from src.network_security.utils.ml_utils.model.estimator import NetworkSecurityModel
from src.network_security.exception.exception import CustomException
from src.network_security.utils.main_utils.utils import load_object



class PredictionPipeline:
    def __init__(self):
        self.class_name: str = self.__class__.__name__
        self.config: ModelPredictionConfig = ModelPredictionConfig()
        self.df: pd.DataFrame = pd.DataFrame()

    def load_config(self, config: ModelPredictionConfig):
        """
        Load the configuration
        :param config: ModelPredictionConfig
        """
        self.config = config

    def load_data(self, df: pd.DataFrame):
        """
        Load the data
        :param df: input data
        """
        self.df = df

    def get_data(self) -> pd.DataFrame:
        """
        Get the data
        :return: Dataframe
        """
        return self.df

    def get_json_data(self) -> str:
        """
        Get the data in JSON format
        :return: Data in JSON format
        """
        return self.df.to_json(orient='records')

    def save_csv(self, file_path: str):
        """
        Save the data in CSV format
        :param file_path: File path
        """
        self.df.to_csv(file_path, index=False)

    def get_html_data(self) -> str:
        """
        Get the data in HTML format
        :return: Data in HTML format
        """
        return self.df.to_html()

    def get_shape(self) -> tuple:
        """
        Get the shape of the data
        :return: Shape of the data
        """
        return self.df.shape

    def insert_into_mongodb(self, mongodb_collection):
        """
        Insert the data into MongoDB
        :param mongodb_collection: MongoDB collection
        """
        tag: str = f"{self.class_name}::insert_into_mongodb::"
        try:
            # convert the dataframe to dictionary
            prediction_df_dict = self.df.to_dict(orient="records")
            # insert the records
            mongodb_collection.insert_many(prediction_df_dict)
        except Exception as e:
            logger.error(f"{tag}::Error inserting the data into MongoDB: {e}")
            raise CustomException(e, sys)

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict the class label for df
        :param df: input data
        :return: Predicted dataframe
        """
        tag: str = f"{self.class_name}::predict::"
        try:
            preprocessor_file_path = os.path.join(self.config.final_model_dir,self.config.final_preprocessing_object_file_name)
            if not os.path.exists(preprocessor_file_path):
                raise CustomException(f"Preprocessor file not found at {preprocessor_file_path}", sys)
            preprocessor = load_object(preprocessor_file_path)

            model_file_path = os.path.join(self.config.final_model_dir, self.config.final_model_file_name)
            if not os.path.exists(model_file_path):
                raise CustomException(f"Model file not found at {model_file_path}", sys)
            model = load_object(model_file_path)

            network_model = NetworkSecurityModel(preprocessor, model, "network_security_model")
            predictions = network_model.predict(df)
            df[target_column] = predictions
            self.df = df
            return self.df
        except Exception as e:
            logger.error(f"{tag}::Error running the data prediction pipeline: {e}")
            raise CustomException(e, sys)