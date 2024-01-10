import graphene


class Card(graphene.ObjectType):
    id = graphene.String()
    title = graphene.String()
    description = graphene.String()
    pos = graphene.Int()
    column_id = graphene.String()
    board_id = graphene.String()
    created_at = graphene.String()
