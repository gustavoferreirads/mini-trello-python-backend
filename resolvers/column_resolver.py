import graphene

from inputs.column_input import SaveColumnInput, MoveColumnInput, SortColumnCardsInput
from model.column import Column
from service.card_service import CardService
from service.column_service import ColumnService


class ColumnQuery(graphene.ObjectType):
    Columns = graphene.List(Column, board_id=graphene.String(required=True))

    def resolve_columns(self, info, board_id):
        return ColumnService.get_columns(board_id)


class SaveColumn(graphene.Mutation):
    class Arguments:
        data = SaveColumnInput(required=True)

    Output = Column

    def mutate(self, info, data):
        if data.id is None:
            return ColumnService.create_column(data)

        return ColumnService.update_column(data.id, data.title, data.pos)


class MoveColumn(graphene.Mutation):
    class Arguments:
        data = MoveColumnInput(required=True)

    Output = Column

    def mutate(self, info, data):
        ColumnService.move_column(data.column_id, data.to_column_id)
        column = ColumnService.get_column(data.column_id)
        return column


class DeleteColumn(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    Output = Column

    def mutate(self, info, id):
        column = ColumnService.get_column(id)
        ColumnService.delete_column(id)
        return column


class SortCardsBy(graphene.Mutation):
    class Arguments:
        data = SortColumnCardsInput(required=True)

    Output = Column

    def mutate(self, info, data):
        CardService.reorder_column_cards(data.id, data.key)
        return ColumnService.get_column(data.id)


class ColumnMutation(graphene.ObjectType):
    save_column = SaveColumn.Field()
    remove_column = DeleteColumn.Field()
    move_column = MoveColumn.Field()
    sort_cards = SortCardsBy.Field()
