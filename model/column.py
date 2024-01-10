import graphene

from model.card import Card
from service.card_service import CardService


class Column(graphene.ObjectType):
    id = graphene.String()
    title = graphene.String()
    pos = graphene.Int()
    cards = graphene.List(Card)
    board_id = graphene.String()

    def resolve_cards(self, info):
        column_id = self.get('id')
        return CardService.get_cards(column_id)
