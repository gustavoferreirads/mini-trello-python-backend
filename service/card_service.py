import datetime
import uuid

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from db.dynamodb_config import get_dynamodb_resource
from db.dynamodb_utils import get_item, put_item, update_item, delete_item

dynamodb = get_dynamodb_resource()


class CardService:
    TABLE_NAME = 'Cards'

    @staticmethod
    def get_card(card_id):
        try:
            return get_item(CardService.TABLE_NAME, {'id': card_id})
        except ClientError as e:
            print(f"Could not get card: {e}")
            return None

    @staticmethod
    def get_cards(column_id):
        table = dynamodb.Table(CardService.TABLE_NAME)
        try:
            response = table.scan(FilterExpression=Key('column_id').eq(column_id))
            return sorted(response.get('Items', []), key=lambda x: x['pos'])
        except ClientError as e:
            print(f"Could not get column: {e}")
            return None

    @staticmethod
    def delete_card(card_id):
        try:
            return delete_item(CardService.TABLE_NAME, {'id': card_id})
        except ClientError as e:
            print(f"Could not get card: {e}")
            return None

    @staticmethod
    def create_card(card):
        new_card = {
            'id': str(uuid.uuid4()),
            'title': card.title,
            'pos': card.pos,
            'column_id': card.column_id,
            'board_id': card.board_id,
            'created_at': datetime.datetime.utcnow().isoformat()
        }
        try:
            put_item(CardService.TABLE_NAME, new_card)
            return new_card
        except ClientError as e:
            print(f"Could not create card: {e}")
            return None

    @staticmethod
    def update_card(cardToUpdate):
        try:
            # Initialize parts of the update expression and attribute values
            update_parts = []
            expression_attribute_values = {}

            if cardToUpdate['title'] is not None:
                update_parts.append("title=:t")
                expression_attribute_values[':t'] = cardToUpdate.title

            if cardToUpdate['description'] is not None:
                update_parts.append("description=:d")
                expression_attribute_values[':d'] = cardToUpdate.description

            if cardToUpdate['pos'] is not None:
                update_parts.append("pos=:p")
                expression_attribute_values[':p'] = cardToUpdate['pos']

            if cardToUpdate['column_id'] is not None:
                update_parts.append("column_id=:c")
                expression_attribute_values[':c'] = cardToUpdate['column_id']

            if cardToUpdate['board_id'] is not None:
                update_parts.append("board_id=:b")
                expression_attribute_values[':b'] = cardToUpdate['board_id']

            update_expression = "set " + ", ".join(update_parts)

            if update_parts:
                update_item(
                    CardService.TABLE_NAME,
                    {'id': cardToUpdate['id']},
                    update_expression,
                    expression_attribute_values
                )
                return CardService.get_card(cardToUpdate['id'])
            else:
                print("No attributes to update.")
                return cardToUpdate  # or return None, depending on desired behavior

        except ClientError as e:
            print(f"Could not update card: {e}")
            return None

    @staticmethod
    def move_card(card_id, to_card_id, column_id):
        try:

            origin_card = CardService.get_card(card_id)
            if not origin_card:
                print("Origin card not found")
                return None

            to_column_id = column_id
            target_position = 0

            if to_card_id is not None:
                target_card = CardService.get_card(to_card_id)

                if not target_card:
                    print("Target card not found")
                    return None

                to_column_id = target_card['column_id']
                target_position = target_card['pos']
                CardService._update_card_positions(to_column_id, target_position)

            column_id = origin_card['column_id']

            cardToUpdate = {
                'id': card_id,
                'pos': target_position,
                'column_id': to_column_id,
                'title': None,
                'description': None,
                'board_id': None
            }

            CardService.update_card(cardToUpdate)

            # Reorder the original column if different from the target column
            if column_id != to_column_id:
                CardService.reorder_column_cards(column_id, 'pos')

        except ClientError as e:
            print(f"Error moving card: {e}")
            return None


    @staticmethod
    def _update_card_positions(column_id, start_position):
        table = dynamodb.Table(CardService.TABLE_NAME)

        try:
            response = table.scan(
                FilterExpression=Key('column_id').eq(column_id) & Key('pos').gte(start_position)
            )

            with table.batch_writer() as batch:
                for item in response['Items']:
                    new_position = item['pos'] + 1
                    item['pos'] = new_position
                    batch.put_item(Item=item)

        except ClientError as e:
            print(f"Error updating card positions: {e}")

    @staticmethod
    def reorder_column_cards(column_id, key):
        table = dynamodb.Table(CardService.TABLE_NAME)
        # Reordering all cards in a specified column
        try:
            response = table.scan(
                FilterExpression=Key('column_id').eq(column_id)
            )

            print(response['Items'])

            orderByKey = 'pos'

            if key is not None:
                orderByKey = key

            with table.batch_writer() as batch:
                new_position = 0
                default_date = datetime.datetime.min.isoformat()
                for item in sorted(response['Items'], key=lambda x: x.get(orderByKey, default_date)):
                    item['pos'] = new_position
                    batch.put_item(Item=item)
                    new_position += 1

        except ClientError as e:
            print(f"Error reordering cards: {e}")
