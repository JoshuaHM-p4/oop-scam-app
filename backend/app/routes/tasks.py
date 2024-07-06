from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from sqlalchemy import desc
from datetime import datetime
tasks_bp = Blueprint('tasks', __name__, url_prefix='/task')

from app.models import Task, UserTask

# get all tasks
'''
    This route should return all tasks for the user wheter its completed or not if the status or sort query 
    parameter is not provided. If the status query parameter is provided, it should return all tasks with the
    provided status (Not-Started, In-Progress, Completed). If the sort query is date, it returns all tasks sorted
    by date. If the sort query is priority, it returns all tasks sorted by priority.
    Example:
    GET /tasks -> returns all tasks for the user
    GET /tasks?status=Not-Started -> returns all tasks with status Not-Started
    GET /tasks?status=In-Progress -> returns all tasks with status In-Progress
    GET /tasks?status=Completed -> returns all tasks with status Completed
    GET /tasks?sort=date -> returns all tasks sorted by date
    GET /tasks?sort=priority -> returns all tasks sorted by priority
    or double query parameters
    GET /tasks?status=Not-Started&sort=date -> returns all tasks with status Not-Started and sorted by date
    GET /tasks?status=In-Progress&sort=priority -> returns all tasks with status In-Progress and sorted by priority
'''
@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_user_task():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'message': 'User not found'}), 404
        task_sort = request.args.get('sort')
        task_status = request.args.get('status') # Not-Started, In-Progress, Completed
        user_tasks = UserTask.query.filter_by(user_id=user_id).all()
        tasks = []
        for user_task in user_tasks:
            task = Task.query.filter_by(id=user_task.task_id).first()
            if task_status:
                if task.status == task_status:
                    tasks.append(task)
            else:
                tasks.append(task)
        if task_sort == 'priority':
            tasks = sorted(tasks, key=lambda x: x.priority)
        elif task_sort == 'date':
            tasks = sorted(tasks, key=lambda x: x.date)
        return jsonify([task.to_json() for task in tasks]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400    
    # try:
    #     user_id = get_jwt_identity()
    #     if not user_id:
    #         return jsonify({'message': 'User not found'}), 404
    #     task_sort = request.args.get('sort')
    #     task_status = request.args.get('status') # Not-Started, In-Progress, Completed
    #     if task_sort == 'priority':
    #         if task_status:
    #             tasks = Task.query.filter_by(user_id=user_id, status=task_status).order_by(Task.priority).all()
    #         else:
    #             tasks = Task.query.filter_by(user_id=user_id).order_by(desc(Task.priority)).all()
    #     elif task_sort == 'date':
    #         if task_status:
    #             tasks = Task.query.filter_by(user_id=user_id, status=task_status).order_by(Task.date).all()
    #         else:
    #             tasks = Task.query.filter_by(user_id=user_id).order_by(Task.date).all()
    #     else:
    #         if task_status:
    #             tasks = Task.query.filter_by(user_id=user_id, status=task_status).all()
    #         else:
    #             tasks = Task.query.filter_by(user_id=user_id).all()
    #     return jsonify([task.to_json() for task in tasks]), 200
    # except Exception as e:
    #     return jsonify({'message': str(e)}), 400
    
# create task
'''
    This route should create a task for the user. The user_id should be extracted from the JWT token. The name, date,
    type, status, and priority are required fields. The priority should be High, Medium, or Low. If the priority is High,
    the value should be 1, if the priority is Medium, the value should be 2, and if the priority is Low, the value should be 3.
    Example:
    POST /create-task
    {
        "name": "Task 1",
        "date": "2021-07-21",
        "type": "Work",
        "status": "Not-Started",
        "priority": "High"
    }
'''
@tasks_bp.route('/create-task', methods=['POST'])
@jwt_required()
def create_task():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'message': 'User not found'}), 404
        data = request.get_json()
        name = data.get('name')
        date = data.get('date')
        type = data.get('type')
        status = data.get('status')
        priority = data.get('priority')
        if not name or not date or not type or not status or not priority:
            return jsonify({'message': 'Name, Date, Type, Status, and Priority are required'}), 400
       
        if priority == 'High':
            priority = 1
        elif priority == 'Medium':
            priority = 2
        elif priority == 'Low':
            priority = 3
        else:
            return jsonify({'message': 'Priority should be High, Medium, or Low'}), 400
        task = Task(user_id=user_id, name=name, date=date, type=type, status=status, priority=priority)
        db.session.add(task)
        db.session.commit()
        user_task = UserTask(user_id=user_id, task_id=task.id)
        db.session.add(user_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# delete task
'''
    This route should delete a task for the user. The user_id should be extracted from the JWT token. The task_id should
    be provided in the URL. If the task is not found, it should return a 404 status code with the message "Task not found".
    If the user is not found, it should return a 404 status code with the message "User not found". If the task is found
    and deleted successfully, it should return a 200 status code with the message "Task deleted successfully".
    Example:
    DELETE /delete-task/1 -> deletes task with id 1
'''
@tasks_bp.route('/delete-task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'message': 'User not found'}), 404
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# finish task
'''
    This route should finish a task for the user. The user_id should be extracted from the JWT token. The task_id should
    be provided in the URL. If the task is not found, it should return a 404 status code with the message "Task not found".
    If the user is not found, it should return a 404 status code with the message "User not found". If the task is found
    and finished successfully, it should return a 200 status code with the message "Task finished successfully".
    Example:
    Before finishing the task
    {
        name: 'Task 1',
        user_id: 1,
        date: '2021-07-21',
        type: 'Work',
        status: 'Not-Started',
        priority: 1
    }
    PUT /finish-task/1 -> finishes task with id 1
    After finishing the task
    {
        name: 'Task 1',
        user_id: 1,
        date: '2021-07-21',
        type: 'Work',
        status: 'Completed',
        priority: 1,
        is_finished_by: 1, # user_id
        is_finished_at: '2021-07-21'
'''
@tasks_bp.route('/finish-task/<int:task_id>', methods=['PUT'])
@jwt_required()
def finish_task(task_id):
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'message': 'User not found'}), 404
        user_task = UserTask.query.filter_by(user_id=user_id, task_id=task_id).first()
        if not user_task:
            return jsonify({'message': 'Task not found'}), 404
        task = Task.query.filter_by(id=task_id).first()
        task.status = 'Completed'
        task.is_finished_by = user_id
        print(str(datetime.now()).split(' ')[0])
        task.is_finished_at = str(datetime.now()).split(' ')[0]
        db.session.commit()
        return jsonify({'message': 'Task finished successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# unfinish task
'''
    This route should unfinish a task for the user. The user_id should be extracted from the JWT token. The task_id should
    be provided in the URL. If the task is not found, it should return a 404 status code with the message "Task not found".
    If the user is not found, it should return a 404 status code with the message "User not found". If the task is found
    and unfinished successfully, it should return a 200 status code with the message "Task unfinished successfully".
    Example:
    Before unfinishing the task
    {
        name: 'Task 1',
        user_id: 1,
        date: '2021-07-21',
        type: 'Work',
        status: 'Completed',
        priority: 1,
        is_finished_by: 1,
        is_finished_at: '2021-07-21'
    }
    PUT /unfinish-task/1 -> unfinishes task with id 1
    After unfinishing the task
    {
        name: 'Task 1',
        user_id: 1,
        date: '2021-07-21',
        type: 'Work',
        status: 'Not-Started',
        priority: 1
    }
'''
@tasks_bp.route('/unfinish-task/<int:task_id>', methods=['PUT'])
@jwt_required()
def unfinish_task(task_id):
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'message': 'User not found'}), 404
        user_task = UserTask.query.filter_by(user_id=user_id, task_id=task_id).first()
        if not user_task:
            return jsonify({'message': 'Task not found'}), 404
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        task.status = 'Not-Started'
        task.is_finished_by = None
        task.is_finished_at = None
        db.session.commit()
        return jsonify({'message': 'Task unfinished successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    

# update task
'''
    This route should update a task for the user. The user_id should be extracted from the JWT token. The task_id should
    be provided in the URL. If the task is not found, it should return a 404 status code with the message "Task not found".
    If the user is not found, it should return a 404 status code with the message "User not found". The name, date, type,
    status, and priority are required fields. The priority should be High, Medium, or Low. If the priority is High, the value
    should be 1, if the priority is Medium, the value should be 2, and if the priority is Low, the value should be 3. If the
    priority is not High, Medium, or Low, it should return a 400 status code with the message "Priority should be High, Medium,
    or Low". If the task is found and updated successfully, it should return a 200 status code with the message "Task updated
    successfully".
    Example:
    Before updating the task
    {
        name: 'Task 1',
        user_id: 1,
        date: '2021-07-21',
        type: 'Work',
        status: 'Not-Started',
        priority: 1
    }
    PUT /update-task/1
    {
        "name": "Task One",
        "date": "2021-07-22",
        "type": "Personal",
        "status": "In-Progress",
        "priority": 2
    }
'''
@tasks_bp.route('/update-task/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'message': 'User not found'}), 404
        user_task = UserTask.query.filter_by(user_id=user_id, task_id=task_id).first()
        if not user_task:
            return jsonify({'message': 'Task not found'}), 404
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        data = request.get_json()
        name = data.get('name')
        date = data.get('date')
        type = data.get('type')
        status = data.get('status')
        priority = data.get('priority')
        if not name or not date or not type or not status or not priority:
            return jsonify({'message': 'Name, Date, Type, Status, and Priority are required'}), 400
        if priority == 'High':
            priority = 1
        elif priority == 'Medium':
            priority = 2
        elif priority == 'Low':
            priority = 3
        else:
            return jsonify({'message': 'Priority should be High, Medium, or Low'}), 400
        task.name = name
        task.date = date
        task.type = type
        task.status = status
        task.priority = priority
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# get task by id
'''
    This route should return a task for the user by the task_id. The user_id should be extracted from the JWT token. If the
    task is not found, it should return a 404 status code with the message "Task not found". If the user is not found, it should
    return a 404 status code with the message "User not found". If the task is found, it should return a 200 status code with
    the task data.
    Example:
    GET /task/1 -> returns task with id 1
'''
@tasks_bp.route('/task/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task_by_id(task_id):
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'message': 'User not found'}), 404
        user_task = UserTask.query.filter_by(user_id=user_id, task_id=task_id).first()
        if not user_task:
            return jsonify({'message': 'Task not found'}), 404
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        return jsonify(task.to_json()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400