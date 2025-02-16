# Network Security System

## Table of Contents
- [Notes](#notes)
- [Setup Conda Environment](#setup-conda-environment)
- [Using Git](#using-git)
- [Data](#data)
- [Environment File](#environment-file)
- [Libraries Used](#libraries-used)
- [Database MongoDB](#database-mongodb)
- [Classifiers](#classifiers)
- [Metrics](#metrics)
- [Coding Steps](#coding-steps)
- [Coding Files](#coding-files)
- [Data Ingestion](#data-ingestion)
- [Data Validation](#data-validation)
- [Data Transformation](#data-transformation)
- [Model Trainer](#model-trainer)

## Notes
* If you have added `.github/workflows/main.yml` then disable the workflows in the GitHub repository settings till the correct code is added

## Setup Conda Environment
To set up the Conda environment for this project, follow these steps:

1. **Create the Conda environment**:
    ```bash
    # list all the Conda environments
    conda env list
    # create a new Conda environment
    conda create --name <name> python=3.10
    # if you want to create the conda environment in a specific location
    conda create --prefix </path/to/conda>/env <name> python=3.10
    ```

2. **Activate the Conda environment**:
    ```bash
    conda activate <name>
    # activate the conda environment in a specific location
    conda activate </path/to/conda>/env
    ```
3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Deactivate the Conda environment**:
    ```bash
    conda deactivate
   # deactivate the conda environment in a specific location
    conda deactivate </path/to/conda>/env
    ```
5. **Delete the Conda environment**:
    ```bash
    # list all the conda environments
    conda env list 
    # delete the conda environment
    conda remove --name <name> --all
    # delete the conda environment in a specific location
    conda remove --prefix </path/to/conda>/env --all
    ```
6. **Clean the Conda environment**:
    ```bash
   # use this carefully as it will remove all the packages from the environment
    conda clean --all
    ```
7. **My Conda environment**:
    ```bash
    conda env list
    conda create --name ml python=3.10
    conda activate ml
    pip install -r requirements.txt
    conda deactivate
    conda remove --name ml --all
    conda clean --all
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
* MongoDB Atlas is a fully managed cloud database service that makes it easy to deploy, operate, and scale MongoDB databases.
* Steps
  * Create a MongoDB Atlas account.
  * Deploy your cluster with the below options
    * Tier: Free
    * Name: Cluster0
    * Cloud Provider & Region: AWS & us-east-1
  * Click `Create Deployment`
  * Allowlist your IP address (this is automatically done for you)
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

### Classifiers
* We use the following algorithms to train the model:
* This is defined in the `ModelTrainer` class in the `components/model_trainer.py` file
* **Logistic Regression**: A statistical model that uses a logistic function to model a binary dependent variable, making predictions based on the probability of a certain class or event.
* **Decision Tree Classifier**: A flowchart-like tree structure where internal nodes represent features (or attributes), branches represent decision rules, and each leaf node represents an outcome.
* **K-Nearest Neighbors (KNN) Classifier**: A simple, instance-based learning algorithm that classifies new cases based on a majority vote of its neighbors, with the case being assigned to the class most common among its K nearest neighbors.
* **Random Forest Classifier**: An ensemble learning method that constructs a multitude of decision trees during training and outputs the class that is the mode of the classes or the mean prediction of the individual trees.
* **Gradient Boosting Classifier**: A machine learning technique for regression and classification problems that produces a prediction model in the form of an ensemble of weak prediction models, typically decision trees, optimized to reduce errors in a step-by-step manner.
* **AdaBoost Classifier**: Short for Adaptive Boosting, a machine learning meta-algorithm that combines multiple weak classifiers to form a strong classifier, by focusing on errors made by previous classifiers and giving more weight to challenging cases.

### Metrics
* When working on a classification problem using scikit-learn (sklearn) in Python, it's important to evaluate the performance of your model using various metrics.
* In this project we are using f1 score, precision, recall defined in `ClassificationMetricArtifact` class in `entity/artifact_entity.py` file
* Here are some common metrics you might consider:

1. **Accuracy**: Measures the proportion of correctly classified instances out of the total instances. Useful when classes are balanced.
    ```python
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_true, y_pred)
    ```

2. **Confusion Matrix**: Provides a summary of prediction results, including true positives, true negatives, false positives, and false negatives.
    ```python
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_true, y_pred)
    ```

3. **Precision**: Measures the proportion of positive predictions that are actually correct. Useful when the cost of false positives is high.
    ```python
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    from sklearn.metrics import precision_score
    precision = precision_score(y_true, y_pred, average='weighted')
    ```

4. **Recall (Sensitivity)**: Measures the proportion of actual positives that are correctly identified. Useful when the cost of false negatives is high.
    ```python
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    from sklearn.metrics import recall_score
    recall = recall_score(y_true, y_pred, average='weighted')
    ```

5. **F1 Score**: The harmonic mean of precision and recall. Useful when you need a balance between precision and recall.
    ```python
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    from sklearn.metrics import f1_score
    f1 = f1_score(y_true, y_pred, average='weighted')
    ```

6. **ROC AUC Score**: Measures the area under the receiver operating characteristic (ROC) curve. Useful for binary classification problems.
    ```python
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    from sklearn.metrics import roc_auc_score
    roc_auc = roc_auc_score(y_true, y_pred)
    ```

7. **Log Loss**: Measures the performance of a classification model where the prediction output is a probability value between 0 and 1.
    ```python
    y_true = [0, 1, 1, 0, 1]
    y_pred_proba = [0, 1, 0, 0, 1]
    from sklearn.metrics import log_loss
    log_loss_value = log_loss(y_true, y_pred_proba)
    ```

* Each metric provides unique insights into different aspects of your model's performance. 
* The choice of which metrics to use depends on the specific requirements and characteristics of the classification problem

## MLFlow
* Before running the model evaluation pipeline or the model prediction pipeline, make sure the **mlflow server is running**
* Make sure the correct **mlflow uri** is set in the config file **config.yaml**
* Add **mlflow** package to the **requirements.txt** file or install it manually using `pip install mlflow`
  * The other packages needed are given in the **requirements.txt** file
* Make sure the mlflow server port does not conflict with any other port on your machine
* Make sure the mlflow server port does not conflict with Flask server port on your machine
* Run the mlflow server using the following command
* Open the terminal and run the following command
```bash
# mlflow server will be running on localhost: 127.0.0.1 and on port: 8080
mlflow server --host 127.0.0.1 --port 8080
```
* Access the mlflow server at http://127.0.0.1:8080/ 
* Run the MLFlow and Flask in two different terminals

## Project steps
* The project is divided into multiple steps
* Load the data into the mongodb database [optional as this usually is done by the data engineering team]
* Data Ingestion
  * Read the data from the mongodb database and save them into csv files
* Data Validation
  * Validate the data after data ingestion
  * Check for schema validation and data drift
* Data Transformation
  * Transform the data after data validation
  * Replace the *NaN* values in the data
  * Create the train and test data arrays
  * Apply the preprocessing object to the test data
  * Save the transformed data in the numpy array format
  * Save the preprocessing object in the pickle format
    * The preprocessing object is saved in 
      * `artifacts/data_transformation/transformed_object` 
      * `artifacts/final_models`
  * Balance the data using SMOTETomek [optional]
* Model Trainer
  * Train the model using the transformed data
  * Read the model and hyperparameters from the config file `model_params/model_params.yaml`
  * Track the model metrics using MLFlow
  * Save the model in the pickle format
  * Save the model in the `artifacts/model_trainer/trained_model` folder
  * Save the model in the `artifacts/final_models` folder

## Coding Steps
* Constants
* Configuration
* Entity
  * Config Entity
* Entity
  * Artifact Entity
* Components
* Pipeline
* Main


## Coding Files
### Data Ingestion
* For data ingestion we read the data from the `MongoDB` database, split and save them into `CSV` files
* **Step1**: Add constants to `constants/__init__.py` file
* **Step2**: Add **GENERAL** and **DATA INGESTION** constants to `constants/training_pipeline/__init__.py` file
* **Step3**: Add **TrainingPipelineConfig** class to `config/configuration.py` file
* **Step4**: Add **DataIngestionConfig** class to `entity/config_entity.py` file
  * In here we create `DataIngestionConfig` class with the below attributes as class variables
  * These variables contain the folder and file paths for the data ingestion process
    * data_ingestion_dir
    * feature_store_file_path
    * training_file_path
    * testing_file_path
  * Using the above variables, we create below file structure
  ```plaintext
  artifacts/
  └── data_ingestion/
      ├── feature_store/
      │   └── phisingData.csv
      └── ingested/
          ├── train_data.csv
          └── test_data.csv
  ```
  * We also add database and collection name as class variables
    * collection_name
    * database_name
    * train_test_split_ratio
* **Step5**: Add **DataIngestionArtifact** class to `entity/artifact_entity.py` file with paths to test and train data
* **Step6**: Add **DataIngestion** class to `components/data_ingestion.py` file
  * In here we create `DataIngestion` class
* **Step7**: Add **DataIngestion** class to `pipeline/data_ingestion.py` file
* **Step8**: Add the pipeline to the `main.py` file and run the pipeline

### Data Validation
* We get the data from the `data ingestion artifact` pipeline and validate the data
#### Schema Validation
* Schema validation allows you to define the structure of data columns and numerical columns in each collection.
* Add `data_schema/schema.yaml` file with the below sections
  * columns
    * Contains the column names and their data types
  * numerical_columns
    * Contains the numerical column names
* We use this file to validate our data after data ingestion as part of the data validation process

#### Data Drift
* Data drift
    * Data drift refers to the changes in data distribution over time, which can affect the performance of machine learning models
    * When the data that a model was trained on no longer represents the real-world data it is currently exposed to, the model's predictions can become less accurate or even invalid.
    * There are two primary types of data drift:
      * **Covariate Shift**: The distribution of the input features changes over time.
      * **Concept Drift**: The relationship between the input features and the target variable changes over time.
    * We check for drift in the data by comparing the data distribution of the training and testing data
    * We calculate the drift for each column and if the drift is greater than the threshold then we consider it as drift
    * We save the drift report in the `drift_report` folder
    * The drift report contains the drift status for each column true or false, the p_value and the threshold
    * If the drift is greater than the threshold then we consider it as drift
    * The drift is calculated using the `ks_2samp` function from the `scipy` library
    * The `ks_2samp` function returns the p_value and the statistic value
    * If the p_value is less than the threshold then we consider it as drift

#### Other validations
* Below are some of the various things we do to validate the data
  * Schema Validation
  * Data drift
  * Number of columns
  * Check numerical columns

#### Coding Steps
* **Step1**: Add **schema file path** and  **DATA VALIDATION** constants to `constants/training_pipeline/__init__.py` file
* **Step2**: Add **DataValidationConfig** class to `entity/config_entity.py` file
  * In here we create `DataValidationConfig` class with as class variables for valid, invalid and drift report folders
  * Using the above variables we create below file structure
  ```plaintext
    artifacts/
    ├── data_validation/
    │   ├── validated/
    │   │   ├── train_data.csv
    │   │   └── test_data.csv
    │   ├── invalid/
    │   │   ├── train_data.csv
    │   │   └── test_data.csv
    │   └── drift_report/
    │       └── drift_report.yaml

  ```
* **Step3**: Add **DataValidationArtifact** class to `entity/artifact_entity.py` file with paths to test and train data
* **Step4**: Add **DataValidation** class to `components/data_validation.py` file
  * In here we create `DataValidation` class
  * The validation is written in the function `initiate_data_validation`
    * Both the schema and drift are validated and final status based on both values is saved in the `DataValidationArtifact` object `validation_status` attribute
    * For drift if there is no drift then `True` is returned else `False`
      * i.e. The drift on all the columns should be less than the threshold and should be `False`
  * We use `read_yaml` and `write_yaml` from `utils.py` to read the schema and write drift report yaml files respectively
* **Step5**: Add **DataValidation** class to `pipeline/data_validation.py` file
* **Step6**: Add the pipeline to the `main.py` file and run the pipeline

### Data Transformation
#### Steps
* Get the `data validation artifact` and transform the data
* Delete the `target` column from the train dataset 
* Replace the `NaN` values in the train dataset using imputer techniques (Robust Scalar, Simple Imputer)
  * Here we are using `KNNImputer` to replace the `NaN` values
  * The K-Nearest Neighbors (KNN) Imputer is a technique used to fill in missing values in a dataset.
  * KNN Imputer method helps to preserve the underlying patterns in the data and provides a more reliable way to handle missing values compared to simpler methods like mean or median imputation.
  * Here's how it works:
    * Identify Missing Values: The KNN imputer detects which entries in the dataset are missing. 
    * Select Neighbors: For each missing value, it identifies the 'k' nearest data points (neighbors) based on the distance metric (like Euclidean distance) using the available data. 
    * Impute Missing Values: The missing value is then imputed (filled in) by taking the average (or most frequent value, depending on the problem) of the neighboring data points.
* Create the train data array
* Create a preprocessing object pickle file for the model
* Apply the preprocessing using the pickle file to the test dataset 
* **[Optionally]** Use `SMOTETomek` on the train and test dataset to balance the data if needed 
  * SMOTETomek is a technique used in machine learning to address class imbalance in datasets
  * We are not using this as we already have balanced data
* Save the transformed data in csv format
* We use `fit_transform` on the train data and `transform` on the test data this avoids data leakage
* We create the below file structure
  ```plaintext
  artifacts/
  ├── data_transformation/
  │   ├── transformed/
  │   │   ├── train.npy
  │   │   └── test.npy
  │   └── transformed_object/
  │       └── preprocessing.pkl
  ```
* The `.npy` file is a binary file format used in Python for storing numpy arrays. 
* The `Data Transformation Artifact` is returned at the end with the paths to the transformed data and preprocessing pickle object

#### Coding Steps
* **Step1**: Add **DATA TRANSFORMATION** constants to `constants/training_pipeline/__init__.py` file
* **Step2**: Add **DataTransformationConfig** class to `entity/config_entity.py` file
  * In here we create `DataTransformationConfig` class with as class variables for transformed and preprocessing folders
* **Step3**: Add **DataTransformationArtifact** class to `entity/artifact_entity.py` file with paths to test and train data
* **Step4**: Add **DataTransformation** class to `components/data_transformation.py` file
  * In here we create `DataTransformation` class
  * In the `utils` module we have the below functions to manage the numpy array and pickle object
    * `save_numpy_array_data` to save the numpy array
    * `load_numpy_array_data` to load the numpy array
    * `save_object` to save the pickle object
    * `load_object` to load the pickle object 
  * Extract the dependent and independent features from the train and test data
  * The target column has unique values 1 and -1 this is converted to 1 and 0
* **Step5**: Add **DataTransformation** class to `pipeline/data_transformation.py` file
* **Step6**: Add the pipeline to the `main.py` file and run the pipeline

### Model Trainer
#### Steps
* Get the data and pre-processor pickle from the `data transformation artifact` and train the model
* This module contains 
  * Model Trainer Config: Contains the model name and model file path and other details we use after training the model
  * Model Trainer Component: Contains the model training code
  * Model Trainer Artifact: Contains the model output details like a model pickle file path
* Get the data using the model config
* Load the data from the numpy arrays
* Split the data into train and test data
* Split into dependent and independent features
* Train the model using the training data
  * Multiple models can be trained and the best model can be selected using the model evaluation metrics and best score
* Save the model using the pickle object by combining with the preprocessor pickle file
* We create the below file structure
  ```plaintext
    artifacts/
    └── model_trainer/
        ├── trained_model/
        │   └── model.pkl
        ├── final_models/
        │   └── model.pkl
        │   └── preprocessing.pkl
        └── saved_models/
            └── model.pkl
  ```

#### Coding Steps
* **Step1**: Add **MODEL TRAINER** constants to `constants/training_pipeline/__init__.py` file
* **Step2**: Add **ModelTrainerConfig** class to `entity/config_entity.py` file
  * In here we create `ModelTrainerConfig` class with as class variables for model and model file paths
* **Step3**: Add **ModelTrainerArtifact** and **ClassificationMetricArtifact** class to `entity/artifact_entity.py`
  * ClassificationMetricArtifact contains the classification metrics like accuracy, precision, recall, f1 score and confusion matrix
* **Step4**: Add **ModelTrainer** class to `components/model_trainer.py` file
  * In here we create `ModelTrainer` class
  * Add `track_mlflow` function to track the model metrics using MLFlow
  * The final best model is saved in the `artifacts/final_models` folder
* **Step5**: Add **ModelTrainer** class to `pipeline/model_trainer.py` file