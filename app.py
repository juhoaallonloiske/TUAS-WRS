from flask import Flask, jsonify, request
from http import HTTPStatus
from flask_restful import Api

from resources.workspace import WorkspaceListResource, WorkspaceResource, WorkspacePublicResource

app = Flask(__name__)
api = Api(app)


api.add_resource(WorkspaceListResource, '/workspaces')
api.add_resource(WorkspaceResource, '/workspaces/<int:workspace_id>')
api.add_resource(WorkspacePublicResource, '/workspaces/<int:workspace_id>/public')

if __name__ == '__main__':
    app.run(port=5000, debug=True)



