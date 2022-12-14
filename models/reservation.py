from datetime import *
from extensions import db


class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    workspaceId = db.Column(db.Integer)
    is_active = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    workspace_id = db.Column(db.Integer(), db.ForeignKey("workspace.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @classmethod
    def get_all_active(cls):
        return cls.query.filter_by(is_active=True).all()

    @classmethod
    def get_by_id(cls, reservation_id):
        return cls.query.filter_by(id=reservation_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


