from flask import Blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

from flask import request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

# Get All Users
@users_bp.route('/all', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        result = [user.to_json() for user in users]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get User by ID
@users_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        user = User.query.get(id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_json()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
