import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import openpyxl

file_path = "HHDG - SpareInventory - excel.xlsx"
db_client = MongoClient("mongodb://127.0.0.1:27017/")

# Loading the Excel file using openpyxl
try:
    workbook = openpyxl.load_workbook(file_path)
    print("Workbook loaded successfully.")
except FileNotFoundError:
    print(f"The file '{file_path}' does not exist.")
except Exception as e:
    print(f"An error occurred while opening the file: {str(e)}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\nlistening for info...")
        client.subscribe('Inbound')
        print("Subscribed to 'Inbound' topic")
        client.subscribe('Outbound')
        print("Subscribed to 'Outbound' topic")
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    extracted_data = parse_data(data)
    append_to_database(data, extracted_data)

def append_to_database(data, extracted_data):
    db = db_client["Product_Management"]
    collection = db["products"]

    new_entry = {
        "Location": data.get("Location", ""),
        "Box": data.get("Box", ""),
        "RFID": [],
    }

    for rfid_entry in data.get("RFID", []):
        product_id = rfid_entry.get("PRODUCT")
        extracted_data_entry = extracted_data.get(product_id, {})
        merged_entry = {**rfid_entry, **extracted_data_entry}
        new_entry["RFID"].append(merged_entry)

    collection.insert_one(new_entry)
    print(f"{data.get('Box', '')} added to database")

def process(product_id):
    sheet = workbook["main"]
    for row in sheet.iter_rows(min_row=2, values_only=True):
        mach_desc, maker_desc, material, material_desc, part_no, rob = row[2:8]
        if material and material.endswith(product_id):
            return {
                "MACH_DESC": mach_desc,
                "MAKER_DESC": maker_desc,
                "MATERIAL": material,
                "MATERIAL_DESC": material_desc,
                "PART_NO": part_no,
                "ROB": rob
            }
    return None

def parse_data(data):
    extracted_data = {}  # storing extracted data for all RFID entries
    for rfid_entry in data.get("RFID", []):
        product_id = rfid_entry.get("PRODUCT")
        extracted_data_entry = process(product_id)
        if extracted_data_entry:
            extracted_data[product_id] = extracted_data_entry

    return extracted_data  # extracted data for all RFID entries


mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = "192.168.1.20"

client = mqtt.Client("data")
client.on_connect = on_connect
client.on_message = on_message  # message listener

client.connect(mqttBroker)
client.loop_forever()
