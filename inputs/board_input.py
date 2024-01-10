import graphene


class CreateBoardInput(graphene.InputObjectType):
    title = graphene.String()
    color = graphene.String(required=True)


class UpdateBoardInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    title = graphene.String(required=True)


class GetBoardInput(graphene.InputObjectType):
    id = graphene.String(required=True)
