# Network Security System

## Table of Contents
- [Setup Conda Environment](#setup-conda-environment)
- [Using Git](#using-git)
- [Data](#data)
- [Database MongoDB](#database-mongodb)

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

#### Connect to MongoDB Atlas
* To connect to the MongoDB Atlas cluster using Python, follow these steps:
* Go to the MongoDB Atlas dashboard.
* Click on the `Clusters` tab.
* Click on the `Connect` button.
* Click on the `Driver` tab.
* Select the `Python` driver and the `3.6 or later` version.
* Under the `Add your connection string into your application code` section, click `View full code sample`.
* Copy the connection string and replace `<password>` with the password of the database user you created.
  * Create a new Python script (e.g., `connect_mongodb.py`) in the `scripts` directory.
  * Add the following code to the script:
    ```python
    
    
    from pymongo.mongo_client import MongoClient
    
    uri = "mongodb+srv://<db_username>:<db_password>@<cluster_name>.3pogr.mongodb.net/?retryWrites=true&w=majority&appName=<cluster_name>"
    
    # Create a new client and connect to the server
    client = MongoClient(uri)
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    ```
  * Replace `<connection-string>` with the connection string provided in the MongoDB Atlas dashboard.
  * Run the script using the following command:
    ```bash
    python scripts/connect_mongodb.py
    ```
    


