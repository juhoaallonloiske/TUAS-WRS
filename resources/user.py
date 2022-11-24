from flask import request
from flask_restful import Resource
from http import HTTPStatus

from utils import hash_password
from models.user import User
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required


class MeResource(Resource):

    @jwt_required
    def get(self):

        user = User.get_by_id(id=get_jwt_identity())

        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }

        return data, HTTPStatus.OK


class UserResource(Resource):

    @jwt_optional
    def get(self, name):
        user = User.get_by_username(name=name)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        else:
            data = {
                'id': user.id,
                'name': user.name,
            }
        return data, HTTPStatus.OK


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        name = json_data.get('name')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')

        if User.get_by_username(name):
            return {'message': 'name already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)

        user = User(
            name=name,
            email=email,
            password=password
        )

        user.save()

        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }

        return data, HTTPStatus.CREATED

