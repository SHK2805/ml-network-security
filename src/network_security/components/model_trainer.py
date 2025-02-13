import os
import sys

from sklearn.model_selection import GridSearchCV

from src.network_security.constants.training_pipeline import model_params_file_path
from src.network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelResult, \
    ClassificationMetricArtifact
from src.network_security.entity.config_entity import ModelTrainerConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from src.network_security.utils.main_utils.utils import load_object, load_numpy_array_data, read_yaml
from src.network_security.utils.ml_utils.metric.classification_metrics import get_classification_metrics
from src.network_security.utils.ml_utils.model.estimator import NetworkSecurityModel
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.metrics import r2_score, accuracy_score


class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        try:
            self.class_name = self.__class__.__name__
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            logger.error(f"Error in initializing ModelTrainer: {str(e)}")
            raise CustomException(e, sys)

    def train_and_evaluate_models(self, x_train, y_train, x_test, y_test):
        tag: str = f"{self.class_name}::train_model"
        try:
            logger.info(f"{tag} - Training model")

            # Load models and hyperparameters from YAML file
            models_config = read_yaml(model_params_file_path)

            # Dictionary to store the results
            results = {}

            # Train each model with GridSearchCV for hyperparameter tuning and evaluate their performance
            for name, model_info in models_config['models'].items():
                model_class = eval(model_info['model'])
                model = model_class()
                grid_search = GridSearchCV(model, model_info['params'], cv=3, scoring='accuracy')
                grid_search.fit(x_train, y_train)

                best_model = grid_search.best_estimator_
                best_model.fit(x_train, y_train)

                y_train_pred = best_model.predict(x_train)
                y_test_pred = best_model.predict(x_test)

                train_accuracy = accuracy_score(y_train, y_train_pred)
                test_accuracy = accuracy_score(y_test, y_test_pred)

                results[name] = ModelResult(
                    best_model=best_model,
                    best_params=grid_search.best_params_,
                    train_accuracy=train_accuracy,
                    test_accuracy=test_accuracy
                )

                logger.info(f'{name} Best Parameters: {grid_search.best_params_}')
                logger.info(f'{name} Train Accuracy: {train_accuracy:.2f}')
                logger.info(f'{name} Test Accuracy: {test_accuracy:.2f}')

            # Find the best model based on test accuracy
            best_model_name = max(results, key=lambda k: results[k].test_accuracy)
            best_model_result = results[best_model_name]

            # Calculate classification metrics for the best model
            best_model = best_model_result.best_model
            y_pred = best_model.predict(x_test)
            classification_metrics: ClassificationMetricArtifact = get_classification_metrics(y_test, y_pred)

            logger.info(f'Best Model: {best_model_name}')
            logger.info(f'Classification Metrics: {classification_metrics}')

            return best_model_name, best_model_result, classification_metrics
        except Exception as e:
            logger.error(f"{tag} - Error in training model: {str(e)}")
            raise CustomException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        tag: str = f"{self.class_name}::initiate_model_trainer"
        try:
            logger.info(f"{tag} - Initiating model training")
            train_df = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_df = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            # split data into dependent and independent features
            # the last column is the target column
            x_train, y_train = train_df[:, :-1], train_df[:, -1]
            x_test, y_test = test_df[:, :-1], test_df[:, -1]

            # train the model


            logger.info(f"{tag} - Complete model training")
        except Exception as e:
            logger.error(f"{tag} - Error in loading data: {str(e)}")
            raise CustomException(e, sys)