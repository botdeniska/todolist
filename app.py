from datetime import datetime

from flask import Flask, jsonify, request

import db

app = Flask(__name__, static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

ROOT_URL = "/todo/api/v1.0/tasks"


@app.route(f'{ROOT_URL}', methods=['GET'])
def get_tasks():
    with db.get_session() as session:
        return jsonify([task.as_dict() for task in db.get_all_tasks(session)]), 200


@app.route(f'{ROOT_URL}/<task_id>', methods=['GET'])
def get_task(task_id: int):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify(message="Invalid task_id"), 400
    with db.get_session() as session:
        task = db.get_task(session, task_id)
        if task:
            return jsonify(task.as_dict()), 200
    return jsonify(message="No such task"), 404


@app.route(f'{ROOT_URL}', methods=['POST'])
def create_task():
    payload = request.get_json()
    try:
        title = payload["title"]
        description = payload["description"]
        date = payload["date"]
    except KeyError:
        return jsonify(message="Please provide title, description and date"), 400
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return jsonify(message="Please provide yyyy-mm-dd date format"), 400

    task = db.Task(title=title, description=description, date=date)
    with db.get_session() as session:
        id_ = db.add_task(session, task)
        return jsonify(message=f"Task id={id_} has been created"), 201


@app.route(f'{ROOT_URL}/<task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify(message="Invalid task_id"), 400
    with db.get_session() as session:
        if db.delete_task(session, task_id):
            return jsonify(message=f"Task id={task_id} has been deleted"), 200
        return jsonify(message="No such task"), 404


@app.route(f'{ROOT_URL}/<task_id>/status', methods=['PUT'])
def change_task_status(task_id: int):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify(message="Invalid task_id or status"), 400
    with db.get_session() as session:
        if db.change_task_status(session, task_id, True):
            return jsonify(message=f"Task id={task_id} marked as ready"), 200
    return jsonify(message="No such task"), 404


if __name__ == '__main__':
    db.init_db()
    app.run(port=8082, debug=True)
