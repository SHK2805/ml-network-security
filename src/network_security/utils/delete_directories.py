# function to delete a directory and its subdirectories and contents
import shutil
from pathlib import Path
from typing import List


def delete_directory(directory: Path) -> None:
    """
    Delete a directory and its subdirectories and contents

    :param directory: Path to the directory
    :return: None
    """
    # check if the directory exists
    if not directory.exists():
        print(f"Directory {directory} does not exist")
        return
    shutil.rmtree(directory)
    print(f"Directory {directory} deleted")

# function that takes a list of directory checks if they exist
# and delete the directory and its subdirectories and contents
def delete_directories(directories: List[Path]) -> None:
    """
    Delete a list of directories and their subdirectories and contents

    :param directories: List of directories to delete
    :return: None
    """
    for directory in directories:
        print(f"Deleting directory: {directory}")
        delete_directory(directory)