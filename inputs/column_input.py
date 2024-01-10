import graphene


class SaveColumnInput(graphene.InputObjectType):
    id = graphene.String()
    title = graphene.String(required=True)
    column_id = graphene.String()
    pos = graphene.Int(required=True)
    board_id = graphene.String()


class MoveColumnInput(graphene.InputObjectType):
    column_id = graphene.String(required=True)
    to_column_id = graphene.String(required=True)


class SortColumnCardsInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    key = graphene.String(required=True)
