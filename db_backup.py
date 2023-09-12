import urllib.request
import pymongo.errors
from pymongo import MongoClient
import datetime
from pytz import timezone
from time import sleep
import certifi as certifi
from pprint import pprint

# Local Database
db_client = MongoClient("mongodb://127.0.0.1:27017/")
db = db_client["Product_Management"]
collection = db["products"]
messages = db["Messages"]

# Deployed Database for Backup
db_client2 = MongoClient("mongodb+srv://Naad:naad2002@cluster0.7redvzp.mongodb.net/", tlsCAFile=certifi.where())
db_console = db_client2["Product_Management_backup"]
collection_products = db_console["products"]
collection_console = db_console["Console_Messages"]

def connect():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

def backup_collections():
    try:
        [collection_console.update_one({"_id": message["_id"]}, {"$set": message}, upsert=True) for message in messages.find()]

        for product in collection.find():
            # product_id = product["PRODUCT"]
            # zone = product["Zone"]
            # # product_id_filter = {"PRODUCT": product_id, "Zone": zone}
            product_id_filter = {"_id": product["_id"]}
            try:
                collection_products.update_one(product_id_filter, {"$set": product}, upsert=True)
            except pymongo.errors.DuplicateKeyError:
                pass

        timestamp = datetime.datetime.now(timezone("Asia/Kolkata"))
        print(f"Backup completed at {timestamp}")

    except Exception as e:
        print("Error during Backup")
        pprint(({"ERROR": e}))


while True:
    if connect():
        backup_collections()
    sleep(10)  # Backup Every 10 seconds
