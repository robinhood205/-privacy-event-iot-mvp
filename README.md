# Privacy Event IoT MVP

A lightweight IoT event monitoring system built on AWS serverless architecture.

## 📌 Overview

This project demonstrates an end-to-end IoT data pipeline:

IoT Device → AWS IoT Core → DynamoDB → Lambda → API Gateway → Web Dashboard

The system collects door sensor events and displays real-time status via a web interface.

---

## 🏗 Architecture

### Data Flow

1. Device publishes MQTT messages to AWS IoT Core
2. IoT Rule filters and forwards data to DynamoDB
3. Lambda function queries latest event
4. API Gateway exposes REST endpoint
5. Dashboard fetches and displays event data

---

## 📂 Project Structure

privacy-event-iot-mvp\
├── dashboard\
│   └── index.html
├── screenshots\
│   ├── 1_Serial_started.bmp
│   ├── 2_IoTCoreCert.bmp
│   ├── 2_IoTCorePolicy.bmp
│   ├── 2_IoTCoreThingDetail.bmp
│   ├── 3_DynamoDB.bmp
│   ├── 3_IoTRule.bmp
│   ├── 4_apiGateway.bmp
│   └── 5_dashboard.bmp
├── gateway\
│   ├── 0_main_iot.py
│   ├── 1_main_mqtt.py
│   ├── 2_main_db.py
│   ├── main.py
│   ├── certs\
│   └── MNLib\
│       ├── __init__.py
│       ├── appbase.py
│       ├── apppal.py
│       ├── mwSerial.py
│       ├── parseFmt.py
│       ├── parseFmt_Ascii.py
│       ├── parseFmt_Binary.py
│       └── parseFmt_Line.py
├── infrastructure\
│   ├── infrastruct.txt
├── lambda\
│   └── query_events\
│  	 └── lambda_function.py
├── pyrightconfig.json
└── README.md

dashboard/ # Frontend web interface
gateway/ # Device & MQTT gateway scripts
lambda/ # AWS Lambda functions
infrastructure/ # Phase planning documents
docs/ # Architecture & design documents

## 🔧 Sensor Debugging (CUB Device)

Device firmware publishes MQTT messages with the following structure:

{
  "device_id": "device01",
  "door_state": "close",
  "event_type": "heartbeat",
  "lqi": 119,
  "power": 32897
}

Debugging Steps:
1. Local serial output verification
2. MQTT publish confirmation
3. AWS IoT test client validation
4. DynamoDB item inspection
