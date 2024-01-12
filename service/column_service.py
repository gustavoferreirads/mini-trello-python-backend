import uuid

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from db.dynamodb_config import get_dynamodb_resource
from db.dynamodb_utils import delete_item

dynamodb = get_dynamodb_resource()


class ColumnService:
    TABLE_NAME = 'Columns'

    @staticmethod
    def get_column(column_id):
        table = dynamodb.Table(ColumnService.TABLE_NAME)
        try:
            response = table.get_item(Key={'id': column_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Could not get column: {e}")
            return None

    @staticmethod
    def get_columns(board_id):
        table = dynamodb.Table(ColumnService.TABLE_NAME)
        try:
            response = table.scan(FilterExpression=Key('board_id').eq(board_id))
            return sorted(response.get('Items', []), key=lambda x: x['pos'])

        except ClientError as e:
            print(f"Could not get column: {e}")
            return None

    @staticmethod
    def create_column(t):
        table = dynamodb.Table(ColumnService.TABLE_NAME)

        try:
            new_column = {
                'id': str(uuid.uuid4()),
                'title': t.title,
                'pos': t.pos,
                'board_id': t.board_id,
            }

            table.put_item(Item=new_column)
            return new_column
        except ClientError as e:
            print(f"Could not create column: {e}")
            return None

    @staticmethod
    def update_column(column_id, title, pos):
        table = dynamodb.Table(ColumnService.TABLE_NAME)
        try:
            table.update_item(
                Key={'id': column_id},
                UpdateExpression="set title=:n, pos=:p",
                ExpressionAttributeValues={
                    ':n': title,
                    ':p': pos,
                },
                ReturnValues="UPDATED_NEW"
            )
            return ColumnService.get_column(column_id)
        except ClientError as e:
            print(f"Could not update column: {e}")
            return None

    @staticmethod
    def delete_column(id):
        try:
            return delete_item(ColumnService.TABLE_NAME, {'id': id})
        except ClientError as e:
            print(f"Could not get card: {e}")
            return None

    @staticmethod
    def move_column(column_id, to_column_id, ):
        try:
            origin_column = ColumnService.get_column(column_id)
            if not origin_column:
                print("Target column not found")
                return None

            target_column = ColumnService.get_column(to_column_id)
            if not target_column:
                print("Target column not found")
                return None
            target_pos = target_column['pos']
            oring_pos = origin_column['pos']
            ColumnService.update_column(column_id, origin_column['title'], target_pos)
            ColumnService.update_column(to_column_id,  target_column['title'],oring_pos)

        except ClientError as e:
            print(f"Error moving column: {e}")
            return None
