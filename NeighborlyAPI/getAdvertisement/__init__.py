import os
import azure.functions as func
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId

def main(req: func.HttpRequest) -> func.HttpResponse:

    # example call http://localhost:7071/api/getAdvertisement/?id=5eb6cb8884f10e06dc6a2084

    id = req.params.get('id')
    print("--------------->", id)
    
    if id:
        try:
            url = os.environ["dbConnectionFinal"]
            client = pymongo.MongoClient(url)
            database = client['finalcosmosdblab2']
            collection = database['advertisements']
            
            query = {'_id': id}
            result = collection.find_one(query)
            if not result:
                try:
                    obj_id = ObjectId(id)
                    query = {'_id': obj_id}
                    result = collection.find_one(query)
                except Exception as e:
                    return func.HttpResponse("Invalid ID format.", status_code=400)

            if result:
                print(query)
                print("----------result--------")
                result = dumps(result)
                print(result)
                return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
            else:
                return func.HttpResponse("No advertisement found.", status_code=404)

        except:
            return func.HttpResponse("Database connection error.", status_code=500)
    else:
        return func.HttpResponse("Please pass an id parameter in the query string.", status_code=400)