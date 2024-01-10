from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView

from resolvers.schema import schema

app = Flask(__name__)
CORS(app)

app.add_url_rule('/', view_func=GraphQLView.as_view('graphqls', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
