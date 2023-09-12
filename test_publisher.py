import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")


client = mqtt.Client("publish", clean_session=False)
client.on_connect = on_connect

# broker_address = "mqtt.eclipseprojects.io"
# broker_address = "192.168.1.20"
broker_address = "localhost"

client.connect(broker_address, 1883)

def send_item_data():
    zone = int(input('Enter Zone: '))
    level = int(input('Enter Level: '))
    box = input('Enter Box: ')
    scan = {
        "TimeStamp": "2023-02-15 14:30:45",
        "Device": "PDA2",
        "Location": f"Zone{zone}-{level}-{box}",
        "Box": f"B-{box}",
        "RFID": [
            {"SERIALNO": "45324335", "PRODUCT": "9008143", "EPC": "301A94B9E2631C8002B3982F", "COMPANY": "BWS"},
            {"SERIALNO": "45383536", "PRODUCT": "9008144", "EPC": "301A94B9E262860002B47F70", "COMPANY": "BWS"},
            {"SERIALNO": "45373638", "PRODUCT": "9008145", "EPC": "301A94B9E262850002B458C6", "COMPANY": "BWS"},
            {"SERIALNO": "45314431", "PRODUCT": "9008146", "EPC": "301A94B9E2631D4002B3717F", "COMPANY": "BWS"},
            {"SERIALNO": "45373637", "PRODUCT": "9008147", "EPC": "301A94B9E262864002B458C5", "COMPANY": "BWS"},
            {"SERIALNO": "45314431", "PRODUCT": "9008148", "EPC": "301A94B9E263174002B3717F", "COMPANY": "BWS"},
            {"SERIALNO": "45324336", "PRODUCT": "9008149", "EPC": "301A94B9E263170002B39830", "COMPANY": "BWS"},
            {"SERIALNO": "45334334", "PRODUCT": "9008150", "EPC": "301A94B9E2631E4002B3BF3E", "COMPANY": "BWS"},
            {"SERIALNO": "45373636", "PRODUCT": "9008151", "EPC": "301A94B9E26288C002B458C4", "COMPANY": "BWS"},
            {"SERIALNO": "45383537", "PRODUCT": "9008152", "EPC": "301A94B9E262858002B47F71", "COMPANY": "BWS"},
            {"SERIALNO": "45324335", "PRODUCT": "9015365", "EPC": "301A94B9E2631C8002B3982F", "COMPANY": "CAS"},
        ]
    }
    scan1 = {
        "TimeStamp": "2023-02-15 14:30:45",
        "Device": "PDA2",
        "Location": f"Zone{zone}-{level}-{box}",
        "Box": f"B-{box}",
        "RFID": [
            {"SERIALNO": "45324335", "PRODUCT": "9015365", "EPC": "301A94B9E2631C8002B3982F", "COMPANY": "CAS"},
            {"SERIALNO": "45324335", "PRODUCT": "9015364", "EPC": "301A94B9E2631C8002B3982F", "COMPANY": "CAS"},
            {"SERIALNO": "45324335", "PRODUCT": "9023633", "EPC": "301A94B9E2631C8002B3982F", "COMPANY": "BWS"},
            {"SERIALNO": "45324335", "PRODUCT": "9008380", "EPC": "301A94B9E2631C8002B3982F", "COMPANY": "BWS"},
            {"SERIALNO": "45324335", "PRODUCT": "9008239", "EPC": "301A94B9E2631C8002B3982F", "COMPANY": "BWS"},
        ]
    }
    # message = json.dumps(scan)
    message = json.dumps(scan1)

    if int(input("Enter 1 for inbound and 0 for outbound: ")) == 0:
        topic = "Outbound"
    else:
        topic = "Inbound"

    client.publish(topic, message)
    print(message)


while True:
    user_input = input("Press Enter to simulate a test scan")
    if user_input == "":
        send_item_data()
    else:
        break

client.loop_forever()