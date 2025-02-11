import os
from pathlib import Path
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')


def create_directory(path: Path):
    if not path.exists():
        os.makedirs(path, exist_ok=True)
        logging.info(f"Creating directory: {path}")
    else:
        logging.info(f"Directory {path} already exists")


def create_file(filepath: Path):
    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filepath.name} already exists")


def create_project_structure(project_name: str) -> bool:
    try:
        data_folder_name: str = "phishingdata"
        list_of_files = [
            # general files
            "template.py",
            "setup.py",
            ".env",
            ".gitignore",
            "requirements.txt",
            "README.md",
            "Dockerfile",
            ".dockerignore",
            "docker-compose.yml",
            # GitHub actions
            f".github/workflows/main.yml",
            # logs
            f"logs/log_{project_name}.log",
            # data folder
            f"{data_folder_name}",
            # notebooks
            f"notebooks",
            # src folder
            f"src/__init__.py",
            f"src/{project_name}/__init__.py",
            # top folders
            f"src/{project_name}/pipeline/__init__.py",
            f"src/{project_name}/cloud/__init__.py",
            # logging
            f"src/{project_name}/logging/__init__.py",
            f"src/{project_name}/logging/logger.py",
            # exception
            f"src/{project_name}/exception/__init__.py",
            f"src/{project_name}/exception/exception.py",
            # utils
            f"src/{project_name}/utils/__init__.py",
            f"src/{project_name}/utils/delete_directories.py",
            # scripts
            f"src/{project_name}/scripts/__init__.py",
            f"src/{project_name}/scripts/check_mongodb_connection.py",
            f"src/{project_name}/scripts/push_data_mongodb.py",
            # clean
            "clean.py",
            # components
            f"src/{project_name}/components/__init__.py",
            f"src/{project_name}/components/data_ingestion.py",
            # entity
            f"src/{project_name}/entity/__init__.py",
            f"src/{project_name}/entity/config_entity.py",
            # config
            f"src/{project_name}/config/__init__.py",
            f"src/{project_name}/config/configuration.py",
            # constants
            f"src/{project_name}/constants/__init__.py",
            f"src/{project_name}/constants/training_pipeline/__init__.py",
        ]

        for filepath in list_of_files:
            filepath = Path(filepath)
            filedir = filepath.parent

            # Ensure Dockerfile, docker-compose.yml and .dockerignore are treated as files
            if filepath.name in ['Dockerfile',
                                 '.dockerignore',
                                 'docker-compose.yml',
                                 'deploy.py',
                                 'cloudformation_template.yaml',
                                 '.env']:
                create_file(filepath)
                continue

            # Create directories
            create_directory(filedir)

            # Create files if they do not exist or are empty
            if filepath.suffix:  # Check if it's a file (has a suffix)
                create_file(filepath)
            else:
                create_directory(filepath)
    except Exception as e:
        logging.error(f"Error in creating project structure: {e}")
        return False
    return True


if __name__ == "__main__":
    ml_project_name = "network_security"
    create_project_structure(ml_project_name)
    logging.info(f"Project structure created for {ml_project_name}")