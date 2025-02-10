import logging
import os
from datetime import datetime

# Define the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

# Create logs directory if it doesn't exist
logs_directory = os.path.join(project_root, "logs")
os.makedirs(logs_directory, exist_ok=True)

# Define log file name with timestamp
log_filename = datetime.now().strftime(os.path.join(logs_directory, "ml_project_%Y%m%d_%H%M%S.log"))

# Set up logger
logger = logging.getLogger("CustomLogger")
logger.setLevel(logging.DEBUG)
logger.propagate = False # avoid printing to console multiple times and yolo overwriting the logger configuration

# Create file handler to log to a file
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)

# Create console handler to log to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define log message format
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example usage
if __name__ == "__main__":
    logger.info("Starting the machine learning project...")
    try:
        # Your machine learning code here
        logger.debug("Debugging information")
        logger.info("Training model...")
        # Simulate a warning
        logger.warning("This is a warning message")
        # Simulate an error
        # raise ValueError("This is an error message")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    logger.info("Finished the machine learning project.")