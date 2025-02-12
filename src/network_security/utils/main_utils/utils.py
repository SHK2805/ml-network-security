import yaml
import os
import sys
import numpy as np
import dill
import pickle
from src.network_security.exception.exception import CustomException
from src.network_security.logging.logger import logger

def read_yaml(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error reading the yaml file: {e}")
        raise CustomException(e, sys) from e

def write_yaml(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        logger.error(f"Error writing the yaml file: {e}")
        raise CustomException(e, sys) from e