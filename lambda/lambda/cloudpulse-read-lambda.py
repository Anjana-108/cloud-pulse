import json
import os
import boto3
from decimal import Decimal

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(items, default=decimal_default)
        }

    except Exception as error:
        print(f"Error reading DynamoDB: {error}")

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Failed to retrieve asset data",
                "error": str(error)
            })
        }
