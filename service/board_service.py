import uuid

from botocore.exceptions import ClientError

from db.dynamodb_config import get_dynamodb_resource
from db.dynamodb_utils import get_item, put_item, update_item

dynamodb = get_dynamodb_resource()


class BoardService:
    TABLE_NAME = 'Boards'

    @staticmethod
    def get_board(board_id):
        return get_item(BoardService.TABLE_NAME, {'id': board_id})

    @staticmethod
    def list_boards():
        table = dynamodb.Table(BoardService.TABLE_NAME)
        try:
            response = table.scan()  # Using scan to retrieve all items
            return response.get('Items', [])
        except ClientError as e:
            print(f"Could not list boards: {e}")
        return None

    @staticmethod
    def create_board(board_data):
        new_board = {
            'id': str(uuid.uuid4()),
            'title': board_data.title,
            'color': board_data.color,
            'columns': []
        }

        put_item(BoardService.TABLE_NAME, new_board)
        return new_board

    @staticmethod
    def update_board(board_id, update_data):
        try:
            update_item(
                BoardService.TABLE_NAME,
                {'id': board_id},
                "set title=:n",
                {
                    ':n': update_data.title,
                }
            )
            return BoardService.get_board(board_id)
        except ClientError as e:
            print(f"Could not update card: {e}")
            return None
