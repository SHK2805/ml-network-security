import sys
import sys

import certifi
from dotenv import load_dotenv

from src.network_security.constants.training_pipeline import (data_ingestion_database_name,
                                                              data_ingestion_collection_name)
from src.network_security.exception.exception import CustomException
from src.network_security.pipeline.training_pipeline import TrainingPipeline
from src.network_security.utils.environment import get_mongodb_uri, get_mongodb_name

# Fixing the ImportError
# ImportError: cannot import name 'MutableMapping' from 'collections'
# add this before MongoClient import
import collections
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
collections.Sequence = collections.abc.Sequence
# add fix before importing MongoClient
from pymongo.mongo_client import MongoClient

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run # this will run the app using python app.py
from starlette.responses import RedirectResponse
from fastapi.responses import PlainTextResponse


ca = certifi.where()
load_dotenv()
mongo_db_url = get_mongodb_uri()
mongo_db_name = get_mongodb_name()

# mongodb client
mongodb_client = MongoClient(mongo_db_url, tlsCAFile=ca)
# mongodb database
mongodb_database = mongodb_client[data_ingestion_database_name]
mongodb_collection = mongodb_database[data_ingestion_collection_name]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# templates
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

# home page
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run()
        return PlainTextResponse("Training is successful")
    except Exception as e:
        raise CustomException(e,sys)

@app.get("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        return PlainTextResponse("Prediction is successful")
    except Exception as e:
        raise CustomException(e,sys)

if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)



