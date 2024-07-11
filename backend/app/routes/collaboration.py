from flask import Blueprint
collaboration_bp = Blueprint('collaboration', __name__, url_prefix='/collaboration')

from flask import request, jsonify
from app import db
from app.models import Team, User, TeamMember, Task, TeamTask
from flask_jwt_extended import jwt_required, get_jwt_identity

# Get all teams
@collaboration_bp.route('/get-user-teams', methods=['GET'])
@jwt_required()
def get_user_teams():
    try:
        user_id = get_jwt_identity()
        user_teams = TeamMember.query.filter_by(user_id=user_id).all()
        if not user_teams:
            return jsonify({"message": "User is not a member of any team"}), 404
        teams = []
        for team in user_teams:
            teams.append(Team.query.filter_by(id=team.team_id).first().to_json())
        return jsonify(teams)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Create a new team
@collaboration_bp.route('/create-team', methods=['POST'])
@jwt_required()
def create_team():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        team_name = data['team_name']
        description = data['description']
        if not team_name or not description:
            return jsonify({"message": "Please provide team name and description"}), 400
        team = Team(team_name=team_name, description=description, owner_id=user_id)
        db.session.add(team)
        db.session.commit()
        team_member = TeamMember(team_id=team.id, user_id=user_id, is_admin=True)
        db.session.add(team_member)
        db.session.commit()
        return jsonify({"message": "Team created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# Add a new member to a team
@collaboration_bp.route('/add-member', methods=['POST'])
@jwt_required()
def add_member():
    try:
        data = request.get_json()
        team_id = data['team_id']
        username = data['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
        team_member = TeamMember.query.filter_by(team_id=team_id, user_id=user.id).first()
        if team_member:
            return jsonify({"message": "User is already a member of this team"}), 400
        team_member = TeamMember(team_id=team_id, user_id=user.id)
        db.session.add(team_member)
        db.session.commit()
        return jsonify({"message": "User added to team successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Remove a member from a team
@collaboration_bp.route('/remove-member', methods=['DELETE'])
@jwt_required()
def remove_member():
    try:
        data = request.get_json()
        team_id = data['team_id']
        username = data['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
        team_member = TeamMember.query.filter_by(team_id=team_id, user_id=user.id).first()
        if not team_member:
            return jsonify({"message": "User is not a member of this team"}), 400
        db.session.delete(team_member)
        db.session.commit()
        return jsonify({"message": "User removed from team successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# make a member an admin
@collaboration_bp.route('/make-admin', methods=['POST'])
@jwt_required()
def make_admin():
    try:
        data = request.get_json()
        team_id = data['team_id']
        username = data['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
        team_member = TeamMember.query.filter_by(team_id=team_id, user_id=user.id).first()
        if not team_member:
            return jsonify({"message": "User is not a member of this team"}), 400
        team_member.is_admin = True
        db.session.commit()
        return jsonify({"message": "User is now an admin"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# remove admin status from a member
@collaboration_bp.route('/remove-admin', methods=['POST'])
@jwt_required()
def remove_admin():
    try:
        data = request.get_json()
        team_id = data['team_id']
        username = data['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
        team_member = TeamMember.query.filter_by(team_id=team_id, user_id=user.id).first()
        if not team_member:
            return jsonify({"message": "User is not a member of this team"}), 400
        team_member.is_admin = False
        db.session.commit()
        return jsonify({"message": "User is no longer an admin"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# delete a team
@collaboration_bp.route('/delete-team', methods=['DELETE'])
@jwt_required()
def delete_team():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "User not found"}), 404
        data = request.get_json()
        team_id = data['team_id']
        team = Team.query.filter_by(id=team_id).first()
        if not team:
            return jsonify({"message": "Team not found"}), 404
        if team.owner_id != user_id:
            return jsonify({"message": "You are not the owner of this team"}), 400
        db.session.delete(team)
        db.session.commit()
        team_members = TeamMember.query.filter_by(team_id=team_id).all()
        for member in team_members:
            db.session.delete(member)
        db.session.commit()
        return jsonify({"message": "Team deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# leave a team
@collaboration_bp.route('/leave-team', methods=['DELETE'])
@jwt_required()
def leave_team():
    try:
        data = request.get_json()
        team_id = data['team_id']
        user_id = get_jwt_identity()
        team_member = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
        if not team_member:
            return jsonify({"message": "User is not a member of this team"}), 400
        db.session.delete(team_member)
        db.session.commit()
        return jsonify({"message": "User left the team successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

################################################ Team Tasks ################################################

# create a task in a team
@collaboration_bp.route('/team/create-task', methods=['POST'])
@jwt_required()
def create_team_task():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        team_id = data['team_id']
        task_name = data['task_name']
        task_description = data['task_description']
        if not task_name or not task_description:
            return jsonify({"message": "Please provide task name and description"}), 400
        is_access = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
        if not is_access:
            return jsonify({"message": "You are not member of this team"}), 400
        task = Task(task_name=task_name, task_description=task_description)
        db.session.add(task)
        db.session.commit()
        team_task = TeamTask(team_id=team_id, task_id=task.id)
        db.session.add(team_task)
        db.session.commit()
        return jsonify({"message": "Task created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# fetch all tasks in a team
@collaboration_bp.route('/team/get-tasks', methods=['GET'])
@jwt_required()
def get_team_tasks():
    try:
        user_id = get_jwt_identity()
        team_id = request.args.get('team_id')
        is_access = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
        if not is_access:
            return jsonify({"message": "You are not member of this team"}), 400
        team_tasks = TeamTask.query.filter_by(team_id=team_id).all()
        tasks = []
        for task in team_tasks:
            tasks.append(Task.query.filter_by(id=task.task_id).first().to_json())
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# delete a task in a team
@collaboration_bp.route('/team/delete-task', methods=['DELETE'])
@jwt_required()
def delete_team_task():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        team_id = data['team_id']
        task_id = data['task_id']
        is_access = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
        if not is_access:
            return jsonify({"message": "You are not member of this team"}), 400
        team_task = TeamTask.query.filter_by(team_id=team_id, task_id=task_id).first()
        if not team_task:
            return jsonify({"message": "Task not found"}), 404
        task = Task.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.delete(team_task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# update a task in a team
@collaboration_bp.route('/team/update-task', methods=['PUT'])
@jwt_required()
def update_team_task():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        team_id = data['team_id']
        task_id = data['task_id']
        task_name = data['task_name']
        task_description = data['task_description']
        is_access = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
        if not is_access:
            return jsonify({"message": "You are not member of this team"}), 400
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({"message": "Task not found"}), 404
        task.task_name = task_name
        task.task_description = task_description
        db.session.commit()
        return jsonify({"message": "Task updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
