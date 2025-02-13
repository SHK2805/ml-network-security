import sys

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from src.network_security.entity.artifact_entity import ClassificationMetricArtifact
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger

def get_classification_metrics(y_true, y_pred) -> ClassificationMetricArtifact:
    """
    Get classification metrics
    :param y_true: True labels
    :param y_pred: Predicted labels
    :return: Classification metrics
    """
    try:
        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        return ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
    except Exception as e:
        logger.error(f"Error in getting classification metrics: {str(e)}")
        raise CustomException(e, sys)