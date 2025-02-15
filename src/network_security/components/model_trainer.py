import os
import sys

from sklearn.model_selection import GridSearchCV, StratifiedKFold

from src.network_security.constants.training_pipeline import model_params_file_path
from src.network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelResult, \
    ClassificationMetricArtifact
from src.network_security.entity.config_entity import ModelTrainerConfig
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger
from src.network_security.utils.main_utils.utils import load_object, load_numpy_array_data, read_yaml, save_object
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
            logger.info(f"{tag}::Training model")

            # Load models and hyperparameters from YAML file
            models_config = read_yaml(model_params_file_path)

            # Dictionary to store the results
            results = {}

            # Train each model with GridSearchCV for hyperparameter tuning and evaluate their performance
            skf = StratifiedKFold(n_splits=5)
            for name, model_info in models_config['models'].items():
                model_class = eval(model_info['model'])
                model = model_class()
                grid_search = GridSearchCV(model, model_info['params'], cv=skf, scoring='f1')
                grid_search.fit(x_train, y_train)

                best_model = grid_search.best_estimator_
                best_model.fit(x_train, y_train)

                # Predictions for train and test sets
                y_train_pred = best_model.predict(x_train)
                y_test_pred = best_model.predict(x_test)

                # Accuracy scores for train and test sets
                train_accuracy = accuracy_score(y_train, y_train_pred)
                test_accuracy = accuracy_score(y_test, y_test_pred)

                # Classification metrics for train and test sets
                train_metrics = get_classification_metrics(y_train, y_train_pred)
                test_metrics = get_classification_metrics(y_test, y_test_pred)

                results[name] = ModelResult(
                    best_model=best_model,
                    best_params=grid_search.best_params_,
                    train_accuracy=train_accuracy,
                    test_accuracy=test_accuracy,
                    train_metrics=train_metrics,
                    test_metrics=test_metrics
                )

                logger.info(f'{name} Best Parameters: {grid_search.best_params_}')
                logger.info(f'{name} Train Accuracy: {train_accuracy:.2f}')
                logger.info(f'{name} Test Accuracy: {test_accuracy:.2f}')

            # Find the best model based on multiple metrics (e.g., test accuracy)
            best_model_name = max(results, key=lambda k: results[k].test_accuracy)
            best_model_result = results[best_model_name]

            # Calculate classification metrics for the best model
            best_model = best_model_result.best_model

            # train
            y_pred_train = best_model.predict(x_train)
            train_classification_metrics: ClassificationMetricArtifact = get_classification_metrics(y_train, y_pred_train)
            logger.info(f'Best Model train: {best_model_name}')
            logger.info(f'Classification Metrics train: {train_classification_metrics}')

            # test
            y_pred = best_model.predict(x_test)
            test_classification_metrics: ClassificationMetricArtifact = get_classification_metrics(y_test, y_pred)
            logger.info(f'Best Model train: {best_model_name}')
            logger.info(f'Classification Metrics test: {test_classification_metrics}')

            # load the preprocessing object
            preprocessing_object = load_object(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            if not os.path.exists(model_dir_path):
                logger.info(f"{tag}::Creating model directory")
                os.makedirs(model_dir_path, exist_ok=True)

            network_security_model: NetworkSecurityModel =  NetworkSecurityModel(preprocessor=preprocessing_object, model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path, network_security_model)

            # check if the model is saved
            if not os.path.exists(self.model_trainer_config.trained_model_file_path):
                logger.error(f"{tag}::Model not saved")
                raise CustomException(f"{tag}::Model not saved", sys)

            # model trainer artifact
            model_trainer_artifact: ModelTrainerArtifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_classification_metrics,
                test_metric_artifact=test_classification_metrics
            )

            logger.info(f"{tag}::Model trainer artifact: {model_trainer_artifact}")
            logger.info(f"{tag}::Model training complete")

            return model_trainer_artifact

        except Exception as e:
            logger.error(f"{tag}::Error in training model: {str(e)}")
            raise CustomException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        tag: str = f"{self.class_name}::initiate_model_trainer"
        try:
            logger.info(f"{tag}::Initiating model training")
            train_df = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_df = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            # split data into dependent and independent features
            # the last column is the target column
            x_train, y_train = train_df[:, :-1], train_df[:, -1]
            x_test, y_test = test_df[:, :-1], test_df[:, -1]

            # train the model
            model_trainer_artifact = self.train_and_evaluate_models(x_train, y_train, x_test, y_test)
            logger.info(f"{tag}::Complete model training")
            return model_trainer_artifact
        except Exception as e:
            logger.error(f"{tag}::Error in loading data: {str(e)}")
            raise CustomException(e, sys)