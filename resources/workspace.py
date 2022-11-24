from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from models.workspace import Workspace
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional


class WorkspaceListResource(Resource):

    def get(self):

        workspaces = Workspace.get_all_published()

        data = []

        for workspace in workspaces:
            data.append(workspace.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()

        workspace = Workspace(name=json_data['name'],
                              model=json_data['model'],
                              user_id=current_user)

        workspace.save()

        return workspace.data(), HTTPStatus.CREATED


class WorkspaceResource(Resource):

    @jwt_optional
    def get(self, workspace_id):
        workspace = Workspace.get_by_id(workspace_id=workspace_id)

        if workspace is None:
            return {'message': 'workspace not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if workspace.is_public == False and workspace.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return workspace.data(), HTTPStatus.OK

    @jwt_required
    def put(self, workspace_id):

        json_data = request.get_json()

        workspace = Workspace.get_by_id(workspace_id=workspace_id)

        if workspace is None:
            return {'message': 'workspace not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != workspace.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        workspace.name = json_data['name']
        workspace.model = json_data['model']

        workspace.save()

        return workspace.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, workspace_id):
        workspace = Workspace.get_by_id(workspace_id=workspace_id)

        if workspace is None:
            return {'message': 'workspace not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != workspace.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        workspace.delete()

        return {}, HTTPStatus.NO_CONTENT


class WorkspacePublicResource(Resource):

    @jwt_required
    def put(self, workspace_id):
        workspace = Workspace.get_by_id(workspace_id=workspace_id)

        if workspace is None:
            return {'message': 'workspace not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != workspace.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        workspace.is_public = True
        workspace.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, workspace_id):
        workspace = Workspace.get_by_id(workspace_id=workspace_id)

        if workspace is None:
            return {'message': 'workspace not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != workspace.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        workspace.is_public = False
        workspace.save()

        return {}, HTTPStatus.NO_CONTENT


'''Tee ClientListRescource, ClientResource, ReservationListResource, ReservationResource'''



