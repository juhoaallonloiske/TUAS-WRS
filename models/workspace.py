from extensions import db

workspace_list = []


def get_last_id():
    if workspace_list:
        last_workspace = workspace_list[-1]
    else:
        return 1
    return last_workspace.id + 1


class Workspace(db.Model):
    __tablename__ = 'workspace'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100))
    is_public = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    '''Add more data here, e.g. reservation data'''

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'is_public': self.is_public
        }
