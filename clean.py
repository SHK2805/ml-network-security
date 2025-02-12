from pathlib import Path
from src.network_security.utils.delete_directories import delete_directories

def clean():
    try:
        # paths = [Path("logs")]
        paths = [Path("artifacts"), Path("logs")]
        # delete the folders
        delete_directories(paths)
        print(f"Cleaned up the project directories")
    except Exception as e:
        raise e

if __name__ == "__main__":
    clean()