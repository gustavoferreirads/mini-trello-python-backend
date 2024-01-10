import graphene

from resolvers.board_resolver import BoardQuery, BoardMutation
from resolvers.card_resolver import CardQuery, CardMutation
from resolvers.column_resolver import ColumnQuery, ColumnMutation


class Query(BoardQuery, ColumnQuery, CardQuery, graphene.ObjectType):
    pass


class Mutation(BoardMutation, ColumnMutation, CardMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
