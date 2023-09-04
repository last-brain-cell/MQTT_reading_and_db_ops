import paho.mqtt.client as mqtt
from random import choice
import random
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")


client = mqtt.Client()
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
    zone = int(input("Enter Zone: "))
    level = int(input("Enter Level: "))
    box = int(input("Enter Box: "))
    scan = {
        "TimeStamp": "2023-02-15 14:30:45",
        "Device": "PDA2",
        "Location": f"Zone{zone}-{level}-{box}",
        "Box": f"B-{box}",
        "RFID": [
            {"EPC": "301A8D1BE25D0AC001CF4DFC", "COMPANY": "GEORIM ENGINEERING CO., LTD.", "PRODUCT": "9008171", "SERIALNO": "78901234"},
            {"EPC": "301A94B9E264118001CF4E6B", "COMPANY": "GEORIM ENGINEERING CO., LTD.", "PRODUCT": "9008176", "SERIALNO": "56789012"},
            {"EPC": "301A94B9E264118001CF4E6B", "COMPANY": "SAMGONG CO., LTD", "PRODUCT": "9026384", "SERIALNO": "56789012"},
            {"EPC": "301A94B9E264118001CF4E6B", "COMPANY": "SAMGONG CO., LTD", "PRODUCT": "9026344", "SERIALNO": "56789012"},
        ]
    }
    message = json.dumps(scan)
    topic = choice(["Inbound", "Outbound"])
    client.publish(topic, message)
    print(message)


while True:
    user_input = input("Press Enter to simulate a test scan")
    if user_input == "":
        send_item_data()
    else:
        break
