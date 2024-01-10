import graphene


class SaveCardInput(graphene.InputObjectType):
    id = graphene.String()
    title = graphene.String()
    description = graphene.String()
    pos = graphene.Int()
    column_id = graphene.String()
    board_id = graphene.String()


class MoveCardInput(graphene.InputObjectType):
    card_id = graphene.String(required=True)
    to_card_id = graphene.String()
    to_column_id = graphene.String()


class GetCardsInput(graphene.InputObjectType):
    column_id = graphene.String(required=True)
    board_id = graphene.String(required=True)
