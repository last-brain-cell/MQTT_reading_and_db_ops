import json
import csv

from pymongo import MongoClient
import paho.mqtt.client as mqtt


# Connect to the MongoDB database
db_client = MongoClient("mongodb://127.0.0.1:27017/")
db = db_client["Product_Management"]
collection = db["products"]

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
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)

    if message.topic == "Inbound":
        handle_inbound(data=data)

    if message.topic == "Outbound":
        handle_outbound(data=data)

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

def handle_outbound(data):
    [collection.delete_one({"PRODUCT": f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}"}) for rfid_item in data["RFID"]]
    print("Documents Deleted")

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
        'MACH_DESC': "not found",
        'MAKER_DESC': "not found",
        'MATERIAL': "not found",
        'PART_NO': "not found",
        'ROB': "not found",
    }
    return matched_item


# MQTT Broker Configuration
mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = "192.168.1.20"

# MQTT Client Configuration
client = mqtt.Client("RFID", clean_session=False)
print("MQTT Broker: {}".format(mqttBroker))
client.on_connect = on_connect
client.on_message = on_message  # Message listener

client.connect(mqttBroker)

client.loop_forever()