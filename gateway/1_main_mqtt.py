import os
import json
import time
import ssl
import paho.mqtt.client as mqtt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AWS_ENDPOINT = "YOUR AWS ENDPOINT"
THING_NAME = "device01"

ROOT_CA = os.path.join(BASE_DIR, "certs/AmazonRootCA1.pem")
CERT_FILE = os.path.join(BASE_DIR, "certs/device01.cert.pem")
KEY_FILE = os.path.join(BASE_DIR, "certs/device01.private.key")

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code:", reason_code)
    payload = {"source": "python", "status": "connected"}
    client.publish("iot/dev/device01/events", json.dumps(payload))
    print("Published:", payload)

def on_log(client, userdata, level, buf):
    print("LOG:", buf)

client = mqtt.Client(client_id=THING_NAME, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_log = on_log

client.tls_set(
    ca_certs=ROOT_CA,
    certfile=CERT_FILE,
    keyfile=KEY_FILE,
    tls_version=ssl.PROTOCOL_TLSv1_2
)
print("Connecting to:", AWS_ENDPOINT)
client.connect(AWS_ENDPOINT, 8883)
client.loop_start()

time.sleep(5)
