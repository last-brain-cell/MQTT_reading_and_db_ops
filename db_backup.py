import json
import urllib.request
import pymongo.errors
from pymongo import MongoClient
import datetime
from pytz import timezone
from time import sleep
import certifi as certifi

# Local Database
db_client = MongoClient("mongodb://127.0.0.1:27017/")
db = db_client["Product_Management"]
collection = db["products"]
messages = db["logs"]

# Deployed Database for Backup
db_client2 = MongoClient("mongodb+srv://Naad:naad2002@cluster0.7redvzp.mongodb.net/", tlsCAFile=certifi.where())
db_console = db_client2["Product_Management_backup"]
collection_products = db_console["products"]
collection_console = db_console["logs"]

def connect():
    try:
        urllib.request.urlopen('http://google.com/')
        return True
    except:
        return False

def backup_collections():
    try:
        [collection_console.update_one({"_id": message["_id"]}, {"$set": message}, upsert=True) for message in messages.find()]

        for product in collection.find():
            product_id_filter = {"_id": product["_id"], "PRODUCT": product["PRODUCT"], "Zone": product["Zone"]}
            try:
                collection_products.update_one(product_id_filter, {"$set": product}, upsert=True)
            except pymongo.errors.DuplicateKeyError:
                pass

        timestamp = datetime.datetime.now(timezone("Asia/Kolkata"))
        print(f"Backup completed at {timestamp}")

    except Exception as e:
        print("Error during Backup")
        print(json.dumps({"ERROR": e}))


while True:
    try:
        if connect():
            backup_collections()
        else:
            print("no internet connection")
        sleep(10)
    except KeyboardInterrupt:
        print("Ended")
        break
