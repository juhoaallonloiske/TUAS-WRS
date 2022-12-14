from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.reservation import Reservation
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from schemas.reservation import ReservationSchema

reservation_schema = ReservationSchema()
reservation_list_schema = ReservationSchema(many=True)


class ReservationListResource(Resource):

    def get(self):

        reservations = Reservation.get_all_active()

        return reservation_list_schema.dump(reservations).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()

        data, errors = reservation_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        reservation = Reservation(**data)
        reservation.user_id = current_user
        reservation.save()

        return reservation_schema.dump(reservation).data, HTTPStatus.CREATED

    @jwt_required
    def patch(self, reservation_id):

        json_data = request.get_json()

        data, errors = reservation_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.date = data.get('date') or reservation.date
        reservation.start = data.get('start') or reservation.start
        reservation.end = data.get('end') or reservation.end

        reservation.save()

        return reservation_schema.dump(reservation).data, HTTPStatus.OK


class ReservationResource(Resource):

    @jwt_optional
    def get(self, reservation_id):
        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if reservation.is_active is False and reservation.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return reservation_schema.dump(reservation).data, HTTPStatus.OK

    @jwt_required
    def put(self, reservation_id):

        json_data = request.get_json()

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.date = json_data['date']
        reservation.start = json_data['start']
        reservation.end = json_data['end']
        reservation.workspaceId = json_data['workspaceId']

        reservation.save()

        return reservation_schema.dump(reservation).data, HTTPStatus.OK

    @jwt_required
    def delete(self, reservation_id):

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.delete()

        return {}, HTTPStatus.NO_CONTENT


class ReservationActiveResource(Resource):

    @jwt_required
    def put(self, reservation_id):
        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.is_active = True
        reservation.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, reservation_id):
        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.is_active = False
        reservation.save()

        return {}, HTTPStatus.NO_CONTENT
