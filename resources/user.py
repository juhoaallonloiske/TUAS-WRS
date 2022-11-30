from flask import request
from flask_restful import Resource
from http import HTTPStatus

from utils import hash_password
from models.user import User
from models.workspace import Workspace
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required

from webargs import fields
from webargs.flaskparser import use_kwargs

from schemas.user import UserSchema
from schemas.workspace import WorkspaceSchema

workspace_list_schema = WorkspaceSchema(many=True)

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))


class UserWorkspaceListResource(Resource):

    @jwt_optional
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, name, visibility):

        user = User.get_by_username(name=name)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'

        workspace = Workspace.get_all_by_user(user_id=user.id, visibility=visibility)

        return workspace_list_schema.dump(workspace).data, HTTPStatus.OK


class MeResource(Resource):

    @jwt_required
    def get(self):

        user = User.get_by_id(id=get_jwt_identity())

        return user_schema.dum(user).data, HTTPStatus.OK


class UserResource(Resource):

    @jwt_optional
    def get(self, name):
        user = User.get_by_username(name=name)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user).data

        else:
            data = user_public_schema.dump(user).data

        return data, HTTPStatus.OK


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('name')):
            return {'message': 'name already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        return user_schema.dump(user).data, HTTPStatus.CREATED

