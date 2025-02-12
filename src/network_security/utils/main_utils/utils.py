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
