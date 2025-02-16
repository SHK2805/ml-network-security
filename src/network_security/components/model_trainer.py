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
import mlflow


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

    def track_mlflow(self, data_type,
                     best_model,
                     best_model_name,
                     classification_metrics: ClassificationMetricArtifact):
        tag: str = f"{self.class_name}::track_mlflow"
        try:
            logger.info(f"{tag}::Tracking MLflow")
            mlflow.start_run()
            mlflow.sklearn.log_model(best_model, 'model')
            mlflow.log_param('data_type', data_type)
            mlflow.log_param('model_name', best_model_name)
            mlflow.log_metric('precision', classification_metrics.precision_score)
            mlflow.log_metric('recall', classification_metrics.recall_score)
            mlflow.log_metric('f1', classification_metrics.f1_score)
            mlflow.end_run()
            logger.info(f"{tag}::MLflow tracking complete")
        except Exception as e:
            logger.error(f"{tag}::Error in tracking MLflow: {str(e)}")
            raise CustomException(e, sys)

    def train_and_evaluate_models(self, x_train, y_train, x_test, y_test):
        """
        This function, train_and_evaluate_models, is designed to train and evaluate multiple machine learning models,
        performing hyperparameter tuning and then selecting the best model based on its performance.
        Here's a step-by-step explanation of what it does:

        Load Models and Hyperparameters:
            It starts by loading the model configurations and hyperparameters from a YAML file using the read_yaml function.

        Initialize StratifiedKFold:
            The function initializes a StratifiedKFold object for cross-validation with 5 splits.

        Training Models:
            The function iterates over each model specified in the YAML file.
            For each model, it performs hyperparameter tuning using GridSearchCV with the specified parameters.
            It trains the model on the training data x_train and y_train.

        Evaluate Performance:
            After training, the function evaluates the trained model on both the training and test datasets.
            It calculates accuracy scores and classification metrics (such as precision, recall, f1-score) for both datasets.

        Store Results:
            The results, including the best parameters, accuracy scores, and classification metrics for each model, are stored in a dictionary.

        Select the Best Model:
            It selects the best model based on test accuracy.

        Track Metrics with MLflow:
            For the selected best model, it tracks the classification metrics for both train and test datasets using MLflow.

        Save Model and Preprocessing Object:
            It saves the preprocessing object and the best model in a specified directory.
            It ensures the model is saved correctly and logs an error if not.

        Return Model Trainer Artifact:
            Finally, it returns a ModelTrainerArtifact containing the path to the trained model file and the classification metrics for both the train and test datasets.

        Train and evaluate multiple models
        :param x_train: training features
        :param y_train: training target
        :param x_test: test features
        :param y_test: test target
        :return: ModelTrainerArtifact
        """
        tag: str = f"{self.class_name}::train_model"
        try:
            logger.info(f"{tag}::Training model")

            # Load models and hyperparameters from YAML file
            models_config = read_yaml(model_params_file_path)

            # Dictionary to store the results
            results = {}

            # Train each model with GridSearchCV for hyperparameter tuning and evaluate their performance
            """
            Initialize an object of the StratifiedKFold class with 5 splits. 
            Here's a breakdown of what it does:
                StratifiedKFold: 
                    This is a cross-validation technique used to split data into k folds while maintaining the distribution of class labels. 
                    It's particularly useful for classification tasks where we want to ensure 
                    that each fold has the same proportion of classes as the original dataset.

                n_splits: 
                    This parameter specifies the number of folds to create.

            StratifiedKFold(n_splits=n), we are setting up a cross-validation strategy that will split the data into n folds, 
            ensuring that each fold has a balanced representation of the class labels.
            """
            skf = StratifiedKFold(n_splits=5)
            for name, model_info in models_config['models'].items():
                logger.info(f'********** Training for: {name} started **********')
                model_class = eval(model_info['model'])
                model = model_class()
                grid_search = GridSearchCV(model, model_info['params'], cv=skf, scoring='f1')
                grid_search.fit(x_train, y_train)

                # Best model based on hyperparameter tuning
                # assigns the best-performing model
                # found during the hyperparameter tuning process to the variable best_model.
                best_model = grid_search.best_estimator_
                # best_model = model_class(**grid_search.best_params_)
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
                logger.info(f'********** Training for: {name} complete **********')

            # Find the best model based on multiple metrics (e.g., test accuracy)
            """
            Identify the model with the highest test accuracy and assigns its name to the variable best_model_name
            Here's a breakdown of how it works:
                results: 
                    This is a dictionary where the keys are model names and 
                    the values are ModelResult objects containing the evaluation metrics for each model.
                max function: 
                    This function is used to find the key (model name) that corresponds to the maximum value of a specified criterion.
                key=lambda k: results[k].test_accuracy: 
                    This lambda function is used as the criterion for the max function. 
                    It goes through each key (model name) in the results dictionary and 
                    fetches the test_accuracy from the corresponding ModelResult object.
            """
            best_model_name = max(results, key=lambda k: results[k].test_accuracy)
            """
            The best_model_result contains several key components about the best-performing model. 
            Here are the details:
                best_model: The best model itself, selected based on the highest test accuracy.    
                best_params: The best hyperparameters found during the grid search for this model.
                train_accuracy: The accuracy of the best model on the training set.
                test_accuracy: The accuracy of the best model on the test set.
                train_metrics: The classification metrics (precision, recall, f1-score) of the best model on the training set.
                test_metrics: The classification metrics (precision, recall, f1-score) of the best model on the test set.
            """
            best_model_result = results[best_model_name]

            # Calculate classification metrics for the best model
            """
            The best_model itself is the machine learning model that performed the best during the evaluation process. 
            This container includes the complete model with the optimized hyperparameters selected by the GridSearchCV.
            Here's what it generally contains:
                Model Architecture: 
                    This includes the structure of the model (e.g., algorithm type like Decision Tree, Random Forest, etc.) 
                    and its parameters (e.g., depth of a tree, number of trees in a forest, etc.).
                Learned Weights/Parameters: 
                    The trained parameters or weights that the model learned during the training process.
                Methods for Predictions: 
                    The functions or methods used by the model to make predictions (e.g., predict function).
            Essentially, best_model is ready to make predictions on new data using the parameters and structure learned during the training phase. 
            It's encapsulated to provide an easy-to-use interface for making future predictions and analyses.
            
            There's no need to manually add the hyperparameters to best_model 
            because the GridSearchCV process inherently selects and sets the optimal hyperparameters for the model during the training phase. 
            When the grid_search.best_estimator_ is assigned to best_model, it already contains the best combination of hyperparameters found during the grid search.
            So in summary, best_model is automatically configured with the best hyperparameters. 
            There's no need for additional steps to manually add them.
            """
            best_model = best_model_result.best_model

            # train
            y_pred_train = best_model.predict(x_train)
            train_classification_metrics: ClassificationMetricArtifact = get_classification_metrics(y_train, y_pred_train)
            logger.info(f'Best Model train: {best_model_name}')
            logger.info(f'Classification Metrics train: {train_classification_metrics}')
            # track mlflow
            self.track_mlflow("train", best_model, best_model_name, train_classification_metrics)

            # test
            y_pred = best_model.predict(x_test)
            test_classification_metrics: ClassificationMetricArtifact = get_classification_metrics(y_test, y_pred)
            logger.info(f'Best Model train: {best_model_name}')
            logger.info(f'Classification Metrics test: {test_classification_metrics}')
            # track mlflow
            self.track_mlflow("test", best_model, best_model_name, test_classification_metrics)

            # load the preprocessing object
            preprocessing_object = load_object(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            if not os.path.exists(model_dir_path):
                logger.info(f"{tag}::Creating model directory")
                os.makedirs(model_dir_path, exist_ok=True)

            network_security_model: NetworkSecurityModel =  NetworkSecurityModel(preprocessor=preprocessing_object,
                                                                                 model=best_model,
                                                                                 model_name=best_model_name)
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