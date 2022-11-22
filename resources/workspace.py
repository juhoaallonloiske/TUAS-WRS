from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.workspace import Workspace, workspace_list


class WorkspaceListResource(Resource):

    def get(self):

        data = []

        return {'data': data}, HTTPStatus.OK

    def post(self):

        data = request.get_json()

        workspace = Workspace(name=data['name'],
                              model=data['model'])

        workspace_list.append(workspace)

        return workspace.data, HTTPStatus.CREATED


class WorkspaceResource(Resource):

    def get(self, workspace_id):
        workspace = next((workspace for workspace in workspace_list if workspace.id == workspace_id), None)

        if workspace is None:
            return {'message': 'workspace not found'}, HTTPStatus.NOT_FOUND

        return workspace.data, HTTPStatus.OK

    def put(self, workspace_id):
        data = request.get_json()

        workspace = next((workspace for workspace in workspace_list if workspace.id == workspace_id), None)

        if workspace is None:
            return {'message': 'workspace not found'}, HTTPStatus.NOT_FOUND

        workspace.name = data['name']
        workspace.model = data['model']

        return workspace.data, HTTPStatus.OK



'''Tee ClientListRescource, ClientResource, ReservationListResource, ReservationResource'''



