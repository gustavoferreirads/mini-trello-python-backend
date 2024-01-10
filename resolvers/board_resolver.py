import graphene

from inputs.board_input import CreateBoardInput, UpdateBoardInput
from model.board import Board
from service.board_service import BoardService


class BoardQuery(graphene.ObjectType):
    boards = graphene.List(Board)
    board = graphene.Field(Board, id=graphene.String(required=True))

    def resolve_boards(self, info):
        return BoardService.list_boards()

    def resolve_board(self, info, id):
        return BoardService.get_board(id)


class CreateBoard(graphene.Mutation):
    class Arguments:
        data = CreateBoardInput(required=True)

    Output = Board

    def mutate(self, info, data):
        return BoardService.create_board(data)


class UpdateBoard(graphene.Mutation):
    class Arguments:
        data = UpdateBoardInput(required=True)

    Output = Board

    def mutate(self, info, data):
        BoardService.update_board(data)
        return Board(id=data['id'], title=data['title'])


class BoardMutation(graphene.ObjectType):
    create_board = CreateBoard.Field()
    update_board = UpdateBoard.Field()
