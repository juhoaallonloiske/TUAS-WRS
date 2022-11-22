
workspace_list = []


def get_last_id():
    if workspace_list:
        last_workspace = workspace_list[-1]
    else:
        return 1
    return last_workspace.id + 1


class Workspace:

    def __init__(self, name, model):
        self.id = get_last_id()
        self.name = name
        self.model = model
        self.is_public = False

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'is_public': self.is_public
        }
