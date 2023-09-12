import json
import csv
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import sys
import locale
import datetime
from pytz import timezone

new_locale = 'en_US.UTF-8'
locale.setlocale(locale.LC_ALL, new_locale)

# Connect to the MongoDB database
db_client = MongoClient("mongodb://127.0.0.1:27017/")
db = db_client["Product_Management"]
collection = db["products"]
messages_collection = db["Messages"]

file_path = "HHDG - SpareInventory.xlsx - HHDG - SpareInventory.csv"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\nlistening for info on ...")
        connected = True
        client.subscribe('Inbound')
        print("Subscribed to 'Inbound' topic")
        client.subscribe('Outbound')
        print("Subscribed to 'Outbound' topic")
    else:
        print("Connection failed")
        connected = False

def on_message(client, userdata, message):
    print(sys.getdefaultencoding())
    print(message.payload)
    print("UserData: {}".format(userdata))
    print("Client: {}".format(client))
    time_stamp = datetime.datetime.now(timezone('Asia/Kolkata'))

    try:
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)

        try:
            if message.topic == "Inbound":
                out = handle_inbound(data=data)
            if message.topic == "Outbound":
                out = handle_outbound(data=data)
            else:
                out = {"message": "No message yet on subscribed topics"}
            messages_collection.insert_one({"status": 'successful run without errors', "Timestamp": time_stamp} | out | {"payload": data})

        except Exception as e:
            print(e)
            messages_collection.insert_one({
                "status": 'EXCEPTION / ERROR',
                "Timestamp": time_stamp,
                "Error Message": e,
            })
    except Exception as e:
        messages_collection.insert_one({
            "status": 'EXCEPTION / ERROR',
            "Timestamp": time_stamp,
            "Error Message": e,
        })


def handle_inbound(data):
    for rfid_item in data["RFID"]:
        product = rfid_item | extract_info(product_id=f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}") | {
            "Zone": data["Location"],
            "Box": "B-{}".format(data["Location"].split("-")[2]),
            "ZONE": int(data["Location"].split("-")[0].replace("Zone", "")),
            "LEVEL": int(data["Location"].split("-")[1]),
            "BOX": data["Location"].split("-")[2],
        }

        product_id_filter = {"PRODUCT": f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}"}
        collection.update_one(product_id_filter, {"$set": product}, upsert=True)
    print("Documents Updated/ Inserted")
    return {'message': "Documents Updated/ Inserted", "topic": "Inbound"}


def handle_outbound(data):
    for rfid_item in data["RFID"]:
        product = rfid_item | extract_info(product_id=f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}") | {
            "Zone": "Zone0-0-0",
            "Box": "B-{}".format("0"),
            "ZONE": 0,
            "LEVEL": 0,
            "BOX": "0",
        }

        product_id_filter = {"PRODUCT": f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}"}
        collection.update_one(product_id_filter, {"$set": product}, upsert=True)
    print("Documents added to Zone0-0-0")
    return {'message': "Documents added to Zone0-0-0", "topic": "Outbound"}

def extract_info(product_id):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            match = row["MATERIAL"]

            if product_id == match:
                matched_item = {
                    'PRODUCT': product_id,
                    'MACH_DESC': row['MACH_DESC'],
                    'MAKER_DESC': row['MAKER_DESC'],
                    'MATERIAL': row['MATERIAL'],
                    'MATERIAL_DESC': row['MATERIAL_DESC'],
                    'PART_NO': row['PART_NO'],
                    'ROB': row['ROB'],
                }
                return matched_item

    matched_item = {
        'PRODUCT': product_id,
        'MACH_DESC': "unavailable",
        'MAKER_DESC': "unavailable",
        'MATERIAL': "unavailable",
        'MATERIAL_DESC': "unavailable",
        'PART_NO': "unavailable",
        'ROB': "unavailable",
    }
    return matched_item


# MQTT Broker Configuration
# mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = "192.168.1.20"
mqttBroker = "localhost"

# MQTT Client Configuration
client = mqtt.Client("RFID", clean_session=False)
print("MQTT Broker: {}".format(mqttBroker))
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqttBroker)

client.loop_forever()