from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

workspaces = [
    {
        'id': 1,
        'name': 'Alpha',
        'model': 'Auditorium',
        'available': True
    },
    {
        'id': 2,
        'name': 'ICT_1030B',
        'model': 'Meeting room',
        'available': False
    }
]


@app.route('/workspaces', methods=['GET'])
def get_workspaces():
    return jsonify({'data': workspaces})


@app.route('/workspaces/<int:workspace_id>', methods=['GET'])
def get_workspace(workspace_id):
    workspace = next((workspace for workspace in workspaces if workspace['id'] == workspace_id), None)

    if workspace:
        return jsonify(workspace)

    return jsonify({'message': 'workspace not found'}), HTTPStatus.NOT_FOUND


@app.route('/workspaces', methods=['POST'])
def create_workspace():
    data = request.get_json()

    name = data.get('name')
    model = data.get('model')

    workspace = {
        'id': len(workspaces) + 1,
        'name': name,
        'model': model,
        'available': False
    }

    workspaces.append(workspace)

    return jsonify(workspace), HTTPStatus.CREATED


@app.route('/workspaces/<int:workspace_id>', methods=['PUT'])
def update_workspace(workspace_id):
    workspace = next((workspace for workspace in workspaces if workspace['id'] == workspace_id), None)

    if not workspace:
        return jsonify({'message': 'workspace not found'}), HTTPStatus.NOT_FOUND

    data = request.get_json()

    workspace.update(
        {
            'name': data.get('name'),
            'model': data.get('model'),
        }
    )

    return jsonify(workspace)


@app.route('/workspaces/<int:workspace_id>', methods=['DELETE'])
def delete_workspace(workspace_id):
    workspace = next((workspace for workspace in workspaces if workspace['id'] == workspace_id), None)

    if not workspace:
        return jsonify({'message': 'workspace not found'}), HTTPStatus.NOT_FOUND

    workspaces.remove(workspace)

    return '', HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run()