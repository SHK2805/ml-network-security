import os


def get_mongodb_uri():
    """Retrieves the MongoDB URI from environment variables."""
    return os.getenv("ATLAS_MONGODB_URI")