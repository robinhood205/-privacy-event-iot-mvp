import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('device_events')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def lambda_handler(event, context):

    if event.get("httpMethod") == "OPTIONS":
        return response(200, {})

    try:
        params = event.get("queryStringParameters") or {}
        device_id = params.get("device_id")

        if not device_id:
            return response(400, {"error": "device_id required"})

        db_response = table.query(
            KeyConditionExpression=Key('device_id').eq(device_id),
            ScanIndexForward=False,
            Limit=10
        )

        items = db_response.get("Items", [])

        if not items:
            return response(200, {
                "current_state": "no data",
                "history": []
            })

        latest = items[0]

        # 🔥 关键修正：从 payload 里取值
        payload = latest.get("payload", {})

        result = {
            "device_id": device_id,
            "current_state": payload.get("door_state", "unknown"),
            "event_type": payload.get("event_type", "unknown"),
            "lqi": payload.get("lqi"),
            "power": payload.get("power"),
            "last_update": payload.get("timestamp"),
            "history": items
        }

        return response(200, result)

    except Exception as e:
        return response(500, {"error": str(e)})


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(body, cls=DecimalEncoder)
    }
