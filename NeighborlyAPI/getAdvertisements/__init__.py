import logging
import os
import azure.functions as func
import pymongo
import json
import requests
from bson.json_util import dumps

def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        url = os.environ["dbConnectionFinal"]
        client = pymongo.MongoClient(url)
        database = client['finalcosmosdblab2']
        collection = database['advertisements']

        logic_app_url = "https://prod2-26.southeastasia.logic.azure.com:443/workflows/9f1ba924a8b04182ab1900efbaec2a9b/triggers/When_a_HTTP_request_is_received/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=9KnmJl-qGe8K7VGr4wKRjbKO_cnP1jrNYEicoGM77Qo"

        result = collection.find({})
        result = dumps(result)

        # Sending message in the body to the Logic App
        message_body = {
            "message": "This is a notification from getAdvertisements Function.",
            "data": result
        }

        triggerLogicApp = requests.post(logic_app_url, json=message_body)        
        if triggerLogicApp.status_code in (200, 202):
            return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
        else:
            logging.error(f"Failed to trigger Logic App. Status code: {triggerLogicApp.status_code}, Response: {triggerLogicApp.text}")
            return func.HttpResponse(f"Failed to trigger Logic App. Status code: {triggerLogicApp.status_code}, Response: {triggerLogicApp.text}", status_code=500)
    except:
        print("could not connect to mongodb")
        return func.HttpResponse("could not connect to mongodb",
                                 status_code=400)

