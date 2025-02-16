import os


def get_mongodb_uri():
    """Retrieves the MongoDB URI from environment variables."""
    return os.getenv("ATLAS_MONGODB_URI")

def get_mongodb_name():
    """Retrieves the MongoDB name from environment variables."""
    return os.getenv("ATLAS_CLUSTER_NAME")