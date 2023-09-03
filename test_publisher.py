import paho.mqtt.client as mqtt
from random import choice
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")


client = mqtt.Client()
client.on_connect = on_connect
broker_address = "mqtt.eclipseprojects.io"
client.connect(broker_address)

def send_item_data():
    item_data = {
        "TimeStamp": "2023-01-01 12:00:01",
        "Device": "PDA1",
        "Location": "ZONE3-6-32",
        "Box": "B-043",
        "RFID": [
            {"EPC": "301A8D1BE25D0AC001CF4DFB", "COMPANY": "BWS", "PRODUCT": "9008171", "SERIALNO": "30363131"},
            {"EPC": "301A94B9E264118001CF4E6A", "COMPANY": "CAS", "PRODUCT": "9015366", "SERIALNO": "30363242"},
            {"EPC": "301AB363E26EC2C001CF2CD1", "COMPANY": "FOS", "PRODUCT": "9026315", "SERIALNO": "30354641"}
        ]
    }
    message = json.dumps(item_data)
    topic = choice(["Inbound", "Outbound"])
    client.publish(topic, message)
    print(message)


while True:
    user_input = input("Press Enter to an scan item")
    if user_input == "":
        send_item_data()
    else:
        break
