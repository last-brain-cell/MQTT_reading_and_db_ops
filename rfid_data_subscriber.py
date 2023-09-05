import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import openpyxl

# Define the file path for the Excel file
file_path = "HHDG - SpareInventory - excel.xlsx"

# Connect to the MongoDB database
db_client = MongoClient("mongodb://127.0.0.1:27017/")

# Loading the Excel file using openpyxl
try:
    workbook = openpyxl.load_workbook(file_path)
    print("Workbook loaded successfully.")
except FileNotFoundError:
    print(f"The file '{file_path}' does not exist.")
except Exception as e:
    print(f"An error occurred while opening the file: {str(e)}")

# MQTT Connection Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\nlistening for info...")
        client.subscribe('Inbound')
        print("Subscribed to 'Inbound' topic")
        client.subscribe('Outbound')
        print("Subscribed to 'Outbound' topic")
    else:
        print("Connection failed")

# MQTT Message Callback
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    extracted_data = parse_data(data)
    append_to_database(data, extracted_data)

# Function to append data to the MongoDB database
# def append_to_database(data, extracted_data):
    # db = db_client["Product_Management"]
    # collection = db["products"]
    #
    # # Filter to find a document with the same "Location" and "Box" values
    # filter_query = {
    #     "Location": data.get("Location", ""),
    #     "Box": data.get("Box", ""),
    # }
    #
    # # Try to find an existing document
    # existing_document = collection.find_one(filter_query)
    #
    # if existing_document:
    #     existing_rfid_entries = existing_document.get("RFID", [])
    #
    #     existing_rfid_entries_map = {entry.get("PRODUCT"): index for index, entry in enumerate(existing_rfid_entries)}
    #
    #     # Update or add new RFID entries
    #     for rfid_entry in data.get("RFID", []):
    #         product_id = rfid_entry.get("PRODUCT")
    #         extracted_data_entry = extracted_data.get(product_id, {})
    #
    #         if product_id in existing_rfid_entries_map:
    #             index = existing_rfid_entries_map[product_id]
    #             existing_rfid_entries[index].update({**rfid_entry, **extracted_data_entry})
    #         else:
    #             existing_rfid_entries.append({**rfid_entry, **extracted_data_entry})
    #
    #     collection.update_one(filter_query, {"$set": {"RFID": existing_rfid_entries}})
    #     print(f"Updated existing document for {data.get('Box', '')} in the database")
    # else:
    #     # Create a new entry
    #     new_entry = {
    #         "Location": data.get("Location", ""),
    #         "Box": data.get("Box", ""),
    #         "RFID": [
    #             {**rfid_entry, **extracted_data.get(rfid_entry["PRODUCT"], {})}
    #             for rfid_entry in data.get("RFID", [])
    #         ]
    #     }
    #     collection.insert_one(new_entry)
    #     print(f"Added new document for {data.get('Box', '')} to the database")
    # Function to append data to the MongoDB database

# Function to append data to the MongoDB database
def append_to_database(data, extracted_data):
    db = db_client["Product_Management"]
    collection = db["products"]

    # Extract location and box from the data
    location = data.get("Location", "")
    box = data.get("Box", "")
    product_ids = [entry["PRODUCT"] for entry in data["RFID"]]

    # Filter to find all documents containing any of the product IDs in the RFID data
    filter_query = {
        "RFID.PRODUCT": {"$in": product_ids},
    }

    # Find all documents matching the filter query
    matching_documents = collection.find(filter_query)

    for existing_document in matching_documents:
        existing_rfid_entries = existing_document.get("RFID", [])

        # Create a set to keep track of existing product IDs in this box
        existing_product_ids = set(entry.get("PRODUCT") for entry in existing_rfid_entries)

        # Check if all new products match the existing ones
        all_new_products_exist = all(product_id in existing_product_ids for product_id in product_ids)

        if all_new_products_exist:
            # If all new products already exist in this box, delete the entire entry
            collection.delete_one({"_id": existing_document["_id"]})
            print(f"Deleted existing document for {existing_document['Box']} at {existing_document['Location']} from the database")
        else:
            # Create a list to store updated RFID entries
            updated_rfid_entries = []

            # Update or add new RFID entries
            for rfid_entry in data.get("RFID", []):
                product_id = rfid_entry.get("PRODUCT")
                extracted_data_entry = extracted_data.get(product_id, {})

                if product_id in existing_product_ids:
                    # If the product already exists in this box, remove it
                    existing_rfid_entries = [entry for entry in existing_rfid_entries if entry.get("PRODUCT") != product_id]
                else:
                    # Check if the product exists in other boxes at the same location
                    for existing_box_document in collection.find({
                        "Location": location,
                        "Box": {"$ne": box},
                        "RFID.PRODUCT": product_id
                    }):
                        # Remove the product from other boxes at the same location
                        existing_box_rfid_entries = existing_box_document.get("RFID", [])
                        existing_box_rfid_entries = [entry for entry in existing_box_rfid_entries if
                                                     entry.get("PRODUCT") != product_id]
                        # Update the existing box document
                        collection.update_one({"_id": existing_box_document["_id"]},
                                              {"$set": {"RFID": existing_box_rfid_entries}})

                    # Add the new RFID entry to this box
                    updated_rfid_entries.append({**rfid_entry, **extracted_data_entry})

            # Extend the existing entries with the updated RFID entries
            existing_rfid_entries.extend(updated_rfid_entries)

            # Update the existing box document
            collection.update_one({"_id": existing_document["_id"]}, {"$set": {"RFID": existing_rfid_entries}})
            print(f"Updated existing document for {existing_document['Box']} at {existing_document['Location']} in the database")

    # If no matching documents are found, create a new entry
    new_entry_query = {
        "Location": location,
        "Box": box,
    }
    if not collection.find_one(new_entry_query):
        new_entry = {
            "Location": location,
            "Box": box,
            "RFID": [
                {**rfid_entry, **extracted_data.get(rfid_entry["PRODUCT"], {})}
                for rfid_entry in data.get("RFID", [])
            ]
        }
        collection.insert_one(new_entry)
        print(f"Added new document for {box} at {location} to the database")


# Function to process product data
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

# Function to parse incoming data and extract information
def parse_data(data):
    extracted_data = {}  # Storing extracted data for all RFID entries
    for rfid_entry in data.get("RFID", []):
        product_id = rfid_entry.get("PRODUCT")
        extracted_data_entry = process(product_id)
        if extracted_data_entry:
            extracted_data[product_id] = extracted_data_entry

    return extracted_data  # Extracted data for all RFID entries


# MQTT Broker Configuration
mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = "192.168.1.20"

# MQTT Client Configuration
client = mqtt.Client("data")
client.on_connect = on_connect
client.on_message = on_message  # Message listener

# Connect to the MQTT broker
client.connect(mqttBroker)
client.loop_forever()
