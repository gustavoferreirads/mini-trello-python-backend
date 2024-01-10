import graphene

from model.column import Column
from service.column_service import ColumnService


class Board(graphene.ObjectType):
    id = graphene.String()
    title = graphene.String()
    color = graphene.String()
    columns = graphene.List(lambda: Column)  # Use lambda for self-reference

    def resolve_columns(self, info):
        board_id = self.get('id')
        return ColumnService.get_columns(board_id)
