from pymongo import MongoClient, InsertOne

import json
import os


def json_call():
    port= input("Please enter port number that you used to connect mongodb: ")
    stri = 'mongodb://localhost:' + port
    client = MongoClient(stri)

    dblist = client.list_database_names()
    if (dblist != None):
        client.drop_database("291db")
        db = client["291db"]
    collist = db.list_collection_names()
    if(collist != None):
        db.drop_collection("dblp")
        data_store = db["dblp"]

    file_name = input("Please enter the .json file name: ")
    file_name = file_name + ".json"
    
    os.system("mongoimport --db 291db --drop --collection dblp --drop --file " + file_name + " --port " + port + " --batchSize 100000")
    a = data_store.update_many({},[{"$set": {"year": {"$toString": "$year"}}}], upsert =True)
    data_store.create_index([("$**","text")], name="searchindex")
    return db
