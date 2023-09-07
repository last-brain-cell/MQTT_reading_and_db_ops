import paho.mqtt.client as mqtt
from random import choice
import random
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")


client = mqtt.Client("publish", clean_session=False)
client.on_connect = on_connect
broker_address = "mqtt.eclipseprojects.io"
# mqttBroker = "192.168.1.20"
client.connect(broker_address)

# item_data = [
#     {
#         "TimeStamp": "2023-02-15 14:30:45",
#         "Device": "PDA2",
#         "Location": "ZONE1-4-12",
#         "Box": "C-012",
#         "RFID": [
#             {"EPC": "301A8D1BE25D0AC001CF4DFC", "COMPANY": "XYZ Corp", "PRODUCT": "123456", "SERIALNO": "78901234"},
#             {"EPC": "301A94B9E264118001CF4E6B", "COMPANY": "ABC Inc", "PRODUCT": "987654", "SERIALNO": "56789012"}
#         ]
#     },
#     {
#         "TimeStamp": "2023-01-01 12:00:01",
#         "Device": "PDA1",
#         "Location": "ZONE3-6-32",
#         "Box": "B-043",
#         "RFID": [
#             {"EPC": "301A8D1BE25D0AC001CF4DFB", "COMPANY": "BWS", "PRODUCT": "9008171", "SERIALNO": "30363131"},
#             {"EPC": "301A94B9E264118001CF4E6A", "COMPANY": "CAS", "PRODUCT": "9015366", "SERIALNO": "30363242"},
#             {"EPC": "301AB363E26EC2C001CF2CD1", "COMPANY": "FOS", "PRODUCT": "9026315", "SERIALNO": "30354641"}
#         ]
#     },
#     {
#         "TimeStamp": "2023-03-20 09:15:22",
#         "Device": "PDA3",
#         "Location": "ZONE2-5-21",
#         "Box": "D-075",
#         "RFID": [
#             {"EPC": "301A8D1BE25D0AC001CF4DFD", "COMPANY": "GHI Ltd", "PRODUCT": "246810", "SERIALNO": "13579246"},
#             {"EPC": "301A94B9E264118001CF4E6C", "COMPANY": "JKL Co", "PRODUCT": "864209", "SERIALNO": "20210409"}
#         ]
#     },
#     {
#         "TimeStamp": "2023-04-10 17:45:03",
#         "Device": "PDA4",
#         "Location": "ZONE4-2-14",
#         "Box": "E-021",
#         "RFID": [
#             {"EPC": "301A8D1BE25D0AC001CF4DFE", "COMPANY": "MNO Enterprises", "PRODUCT": "555555", "SERIALNO": "12312312"},
#             {"EPC": "301A94B9E264118001CF4E6D", "COMPANY": "PQR Industries", "PRODUCT": "999999", "SERIALNO": "98765432"}
#         ]
#     }
# ]

# seen = []

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

    if int(input("Enter 0 for inbound and 1 for outbound.")) == 1:
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