import json

import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

def get_post(event, context):
    postId = event['queryStringParameters']['postId']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    if postId=="*":
        result = table.scan()
    else:
        result = table.query(
            KeyConditionExpression=Key('id').eq(postId)
        )
    
    response = {
        "statusCode": 200,
		"headers": {
			"Access-Control-Allow-Origin" : "*"
		},
        "body": json.dumps(result['Items'])
    }

    return response