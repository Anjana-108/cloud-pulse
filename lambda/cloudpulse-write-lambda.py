import json
import os
from decimal import Decimal

import boto3


TABLE_NAME = os.environ["TABLE_NAME"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

sns = boto3.client("sns")


def lambda_handler(event, context):
    try:
        # Incoming CloudPulse MQTT JSON
        data = event

        # Validate required asset ID
        if "asset_id" not in data:
            raise ValueError("asset_id is required")

        # Convert numbers to DynamoDB-compatible Decimal values
        item = json.loads(
            json.dumps(data),
            parse_float=Decimal
        )

        # Store the asset data
        table.put_item(Item=item)

        # Send an alert when tampering is detected
        if data.get("tamper") is True:
            message = (
                f"CloudPulse TAMPER ALERT\n\n"
                f"Asset ID: {data.get('asset_id')}\n"
                f"Status: {data.get('status', 'UNKNOWN')}\n"
                f"Temperature: {data.get('temperature', 'N/A')}\n"
                f"RFID: {data.get('rfid_id', 'N/A')}\n"
                f"Latitude: {data.get('latitude', 'N/A')}\n"
                f"Longitude: {data.get('longitude', 'N/A')}\n"
                f"Timestamp: {data.get('timestamp', 'N/A')}"
            )

            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="CloudPulse Tamper Alert",
                    Message=message
                )
                print("SNS tamper alert sent successfully")

            except Exception as sns_error:
                print(f"SNS alert failed: {sns_error}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Asset data stored successfully",
                "asset_id": str(item["asset_id"])
            })
        }

    except Exception as error:
        print(f"Error: {error}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Failed to process asset data",
                "error": str(error)
            })
        }
