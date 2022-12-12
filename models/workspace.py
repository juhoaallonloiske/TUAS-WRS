from extensions import db


class Workspace(db.Model):
    __tablename__ = 'workspace'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    is_public = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    '''def data?? s.108'''

    @classmethod
    def get_all_by_user(cls, user_id, visibility='public'):
        if visibility == 'public':
            return cls.query.filter_by(user_id=user_id, is_public=True).all()
        elif visibility == 'private':
            return cls.query.filter_by(user_id=user_id, is_public=False)
        else:
            return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_public=True).all()

    @classmethod
    def get_by_id(cls, workspace_id):
        return cls.query.filter_by(id=workspace_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

