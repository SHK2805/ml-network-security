# Network Security System

## Table of Contents
- [Setup Conda Environment](#setup-conda-environment)
- [Using Git](#using-git)
- [Data](#data)
- [Environment File](#environment-file)
- [Libraries Used](#libraries-used)
- [Database MongoDB](#database-mongodb)
- [Coding Steps](#coding-steps)
- [Coding Files](#coding-files)

## Setup Conda Environment
To set up the Conda environment for this project, follow these steps:

1. **Create the Conda environment**:
    ```bash
    conda create --name nss python=3.10
    ```

2. **Activate the Conda environment**:
    ```bash
    conda activate nss
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Deactivate the Conda environment**:
    ```bash
    conda deactivate
    ```

## Using Git
To manage the repository using Git, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    ```

2. **Change the directory to the repository**:
    ```bash
    cd <repository-name>
    ```

3. **Create a new branch**:
    ```bash
    git checkout -b <branch-name>
    ```

4. **Add the changes**:
    ```bash
    git add .
    ```

5. **Commit the changes**:
    ```bash
    git commit -m "<commit message>"
    ```

6. **Push the changes and track the remote branch**:
    ```bash
    git push -u origin <branch-name>
    ```

7. **Create a pull request from the branch to the main branch**:
    ```bash
    git <pull-request>
    ```

8. **Merge the pull request**:
    ```bash
    git merge <branch-name>
    ```

9. **Delete the branch**:
    ```bash
    git branch -d <branch-name>
    ```

10. **Pull the changes from the remote repository**:
    ```bash
    git pull
    ```

## Data
* The data is stored in the `phishingdata` directory.
* The data is stored in the CSV format in the `phishingdata.csv` file.

## Environment File
* Create a new environment file (`.env`) in the root directory.
* This contains the environment variables for the below: 
  * MongoDB connection
* We can use the `python-dotenv` package to load the environment variables from the `.env` file.
* Use the below code to load the environment variables from the `.env` file:
```python
from dotenv import load_dotenv
import os
# Load the environment variables from the .env file
load_dotenv()
var = os.getenv("VAR_NAME")
```

## Libraries Used
* **Certifi** is used to provide Mozilla’s carefully curated collection of Root Certificates for validating the trustworthiness of SSL certificates while verifying the identity of TLS hosts.

## Database MongoDB

#### Create a MongoDB Atlas Account
* We have used MongoDB to store the data.
* The database is created using **MongoDB Atlas** cloud.
* MongoDB Atlas is a fully-managed cloud database service that makes it easy to deploy, operate, and scale MongoDB databases.
* Steps
  * Create a MongoDB Atlas account.
  * Deploy your cluster with below options
    * Tier: Free
    * Name: Cluster0
    * Cloud Provider & Region: AWS & us-east-1
  * Click `Create Deployment`
  * * Whitelist your IP address (this is automatically done for you)
  * Create a database user
    * Give username and password and click `Create Database User`
  * Click `Choose a connection method`
    * Click `Drivers` and select `Python` and `3.6 or later`
    * Copy the pip install command and update the `requirements.txt` file
      * Here: pymongo[srv]==3.6
    * Run the command `pip install -r requirements.txt` to install the required packages for MongoDB in your Conda environment
  * Click `Done`

#### Test connection to MongoDB Atlas
* To connect to the MongoDB Atlas cluster using Python, follow these steps:
* Go to the MongoDB Atlas dashboard.
* Click on the `Clusters` tab.
* Click on the `Connect` button.
* Click on the `Driver` tab.
* Select the `Python` driver and the `3.6 or later` version.
* Under the `Add your connection string into your application code` section, click `View full code sample`.
* Copy the connection string and replace `<password>` with the password of the database user you created.
* Create a new Python script (e.g., `connect_mongodb.py`) in the `scripts` directory.
* Add the connection code to the script
##### Error
* If you get the below error or similar errors while connecting to MongoDB Atlas, follow these steps:
* The issue is the deprecation of some aliases from collections.abc into collections from python 3.10.
* If you can't modify the importations in your scripts because of a third-party import
* As a temporary workaround you can do the aliases manually before importing the problematic third-party lib. 
```bash
ImportError: cannot import name 'MutableMapping' from 'collections'
```
* Check the python version and the collections module using the following code:
```python
import sys
print(sys.version)
import collections
print(dir(collections))
```
* If the collections have **'_collections_abc'** folder then add the below
* If the python version is 3.10 and the collections module does not have the following attributes:
  * MutableMapping
  * MutableSequence
  * MutableSet
  * Sequence
  * Mapping
  * Iterable
* Add the following code to the script to fix it before importing the pymongo module `from pymongo.mongo_client import MongoClient`:
```python
import collections
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
collections.Sequence = collections.abc.Sequence
```
* Connect to MongoDB Atlas
```python
import collections
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
collections.Sequence = collections.abc.Sequence
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://<db_username>:<db_password>@<db_clustername>.3pogr.mongodb.net/?retryWrites=true&w=majority&appName=<db_clustername>"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
```
* Run the script using the following command:
```bash
python scripts/check_mongodb_connection.py
```
* If you get the error `The client driver may require an upgrade`, then upgrade the `pymongo` package using the following command:
```bash
pip install --upgrade pymongo
```

#### Upload data to MongoDB Atlas
* To upload data to the MongoDB Atlas cluster using Python, follow these steps:
* Create a new Python script `push_data_mongodb.py` in the `scripts` directory.
* Add the code to upload the data to the MongoDB Atlas cluster.
* To check if the data is uploaded successfully, follow these steps:
  * Go to the MongoDB Atlas dashboard.
  * Click on the `Clusters` tab.
  * Click on the `Browse Collections` tab.
  * Click on the required collection here `phishingdata`.
  * You should see the data uploaded to the collection.

## Coding Steps
* Constants
* Configuration
* Entity


## Coding Files
* **Step1**: Add constants to `constants/__init__.py` file
* **Step2**: Add **GENERAL** and **DATA INGESTION** constants to `constants/training_pipeline/__init__.py` file
* **Step3**: Add **TrainingPipelineConfig** class to `config/configuration.py` file
* **Step4**: Add **DataIngestion** class to `entity/config_entity.py` file
  * In here we create `DataIngestion` class with the below attributes as class variables
  * These variables contain the folder and file paths for the data ingestion process
    * data_ingestion_dir
    * feature_store_file_path
    * training_file_path
    * testing_file_path
  * Using the above variables we create below file structure
  ```plaintext
  artifacts
  └── data_ingestion
      ├── feature_store
      │   └── phisingData.csv
      └── ingested
          ├── train_data.csv
          └── test_data.csv
  ```
  * We also add database and collection name as class variables
    * collection_name
    * database_name
    * train_test_split_ratio
    


