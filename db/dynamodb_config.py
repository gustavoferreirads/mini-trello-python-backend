import os
import boto3


def get_dynamodb_resource():
    dynamodb_port = os.getenv('DYNAMODB_PORT', '8000')  # Default to 8000 if not set

    dynamodb_endpoint = f'http://localhost:{dynamodb_port}'

    if os.getenv('ENVIRONMENT') == 'production':
        return boto3.resource('dynamodb')
    else:
        return boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint)
