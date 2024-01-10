import graphene

from inputs.card_input import GetCardsInput, MoveCardInput, SaveCardInput
from model.card import Card
from service.card_service import CardService


class CardQuery(graphene.ObjectType):
    cards = graphene.List(Card, data=GetCardsInput(required=True))

    def resolve_cards(self, info, data):
        return CardService.get_cards(data.column_id)


class SaveCard(graphene.Mutation):
    class Arguments:
        data = SaveCardInput(required=True)

    Output = Card

    def mutate(self, info, data):
        if data.id is not None:
            return CardService.update_card(data)

        new_card = CardService.create_card(data)
        return new_card


class MoveCard(graphene.Mutation):
    class Arguments:
        data = MoveCardInput(required=True)

    Output = Card

    def mutate(self, info, data):
        CardService.move_card(data.card_id, data.to_card_id, data.to_column_id)
        card = CardService.get_card(data.card_id)
        return card


class DeleteCard(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    Output = Card

    def mutate(self, info, id):
        card = CardService.get_card(id)

        CardService.delete_card(id)
        CardService.reorder_column_cards(card['column_id'], 'pos')
        return card


class CardMutation(graphene.ObjectType):
    save_card = SaveCard.Field()
    move_card = MoveCard.Field()
    delete_card = DeleteCard.Field()
