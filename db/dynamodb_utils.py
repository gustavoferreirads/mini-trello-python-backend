import logging

from botocore.exceptions import ClientError

from db.dynamodb_config import get_dynamodb_resource

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

dynamodb = get_dynamodb_resource()


def get_item(table_name, key):
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key=key)
        return response.get('Item')
    except ClientError as e:
        logger.error(f"Could not get item from {table_name}: {e}")
        print(f"Could not get item: {e}")
        return None


def put_item(table_name, item):
    table = dynamodb.Table(table_name)
    try:
        table.put_item(Item=item)
        return item
    except ClientError as e:
        logger.error(f"Could not get item from {table_name}: {e}")
        print(f"Could not put item: {e}")
        return None


def update_item(table_name, key, update_expression, expression_attribute_values):
    table = dynamodb.Table(table_name)
    try:
        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return get_item(table_name, key)
    except ClientError as e:
        logger.error(f"Could not get item from {table_name}: {e}")
        print(f"Could not update item: {e}")
        return None


def delete_item(table_name, key):
    table = dynamodb.Table(table_name)
    try:
        response = table.delete_item(Key=key)
        return response
    except ClientError as e:
        logger.error(f"Could not delete item from {table_name}: {e}")
        return None
