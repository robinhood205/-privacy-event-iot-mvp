#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
from datetime import datetime
from awscrt import mqtt
from awsiot import mqtt_connection_builder

# =============================
# TWELITE LIBRARY
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "MNLib"))

from apppal import AppPAL

# =============================
# AWS IoT CONFIG
# =============================
AWS_ENDPOINT = "YOUR AWS ENDPOINT"
THING_NAME = "device01"
TOPIC = "iot/dev/device01/events"

ROOT_CA   = os.path.join(BASE_DIR, "certs/AmazonRootCA1.pem")
CERT_FILE = os.path.join(BASE_DIR, "certs/device01.cert.pem")
KEY_FILE  = os.path.join(BASE_DIR, "certs/device01.private.key")

# =============================
# MQTT SETUP (awsiot)
# =============================
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=AWS_ENDPOINT,
    cert_filepath=CERT_FILE,
    pri_key_filepath=KEY_FILE,
    ca_filepath=ROOT_CA,
    client_id=THING_NAME,
    clean_session=False,
    keep_alive_secs=30,
)

print("Connecting...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

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

            if Data is None:
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
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "lqi": Data.get("LQI"),
                        "power": Data.get("Power")
                    }

                    mqtt_connection.publish(
                        topic=TOPIC,
                        payload=json.dumps(event),
                        qos=mqtt.QoS.AT_LEAST_ONCE
                    )

                    print("Published:", event)

                    last_state = current_state

        time.sleep(0.1)

    except KeyboardInterrupt:
        break

print("Disconnecting...")
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Gateway stopped.")
