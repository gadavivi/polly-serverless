import boto3
import os
import uuid
import logging
import json


def new_post(event, context):
    data = json.loads(event['body'])
    if 'text' not in data or "voice" not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    recordId = str(uuid.uuid4())

    voice = data["voice"]
    text = data["text"]

    # Creating new record in DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    table.put_item(
        Item={
            'id': recordId,
            'text': text,
            'voice': voice,
            'status': 'PROCESSING'
        }
    )

    # Sending notification about new post to SNS
    client = boto3.client('sns')
    client.publish(
        TopicArn=os.environ['ARN_TOPIC'],
        Message=recordId
    )

    response = {
        "statusCode": 200,
		"headers": {
        "Access-Control-Allow-Origin" : "*"
      },
        "body": json.dumps({'id': recordId})
    }

    return response
