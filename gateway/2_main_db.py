#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import ssl
import time
from datetime import datetime
import paho.mqtt.client as mqtt

# TWELITE library
#sys.path.append('./MNLib/')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "MNLib"))

from apppal import AppPAL

# =============================
# AWS IoT CONFIG
# =============================
AWS_ENDPOINT = "YOUR AWS ENDPOINT"
THING_NAME = "device01"
TOPIC = "iot/dev/device01/events"

ROOT_CA = os.path.join(BASE_DIR, "certs/AmazonRootCA1.pem")
CERT_FILE = os.path.join(BASE_DIR, "certs/device01.cert.pem")
KEY_FILE = os.path.join(BASE_DIR, "certs/device01.private.key")

# =============================
# MQTT SETUP
# =============================
client = mqtt.Client(client_id=THING_NAME)

client.tls_set(
    ca_certs=ROOT_CA,
    certfile=CERT_FILE,
    keyfile=KEY_FILE,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

client.connect(AWS_ENDPOINT, 8883)
client.loop_start()

time.sleep(2)

# =============================
# TEST PAYLOAD
# =============================
payload = {
    "device_id": "device01",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "event_type": "test",
    "power": 3001
}

result = client.publish(TOPIC, json.dumps(payload))

print("Published:", payload)
print("Publish result code:", result.rc)

time.sleep(5)
client.loop_stop()
client.disconnect()

"""
client.publish("iot/dev/device01/events", json.dumps({"test": "hello"}))

print("Test message sent")
time.sleep(3)

# =============================
# SERIAL INIT
# =============================

PAL = AppPAL(port="COM4", baud=115200, tout=0.05, sformat="Ascii")

print("Gateway started...")

last_state = None

# =============================
# MAIN LOOP
# =============================
while True:
    try:
        if PAL.ReadSensorData():
            Data = PAL.GetDataDict()

            if Data is None:  # ← 追加
                continue

            # Only handle open/close (PALID == 1)
            if Data.get("PALID") == 1:
                current_state = "open" if Data["HALLIC"] == 1 else "close"

                # Publish only if state changed
                if current_state != last_state:

                    event = {
                        "version": "1.0",
                        "deviceId": THING_NAME,
                        "eventType": "access_state_changed",
                        "state": current_state,
                        "eventTime": Data["ArriveTime"].isoformat(),
                        "lqi": Data.get("LQI"),
                        "power": Data.get("Power")
                    }

                    payload = json.dumps(event)

                    client.publish(TOPIC, payload, qos=1)

                    print("Published:", payload)

                    last_state = current_state

        time.sleep(0.1)

    except KeyboardInterrupt:
        break

client.loop_stop()
client.disconnect()
print("Gateway stopped.")
"""
