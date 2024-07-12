from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from app import db
from app.models import FlashcardSet, Flashcard, UserFlashcardSet

flashcards_bp = Blueprint('flashcards', __name__, url_prefix='/flashcards')

"""########################################## Sharing Flashcard ##########################################
# ENDPOINT

"""


# Share Flashcard Set with a Single User
@flashcards_bp.route('/share_flashcard_set/<int:flashcard_set_id>/<int:shared_user_id>', methods=['POST'])
@jwt_required()
def share_flashcard_set(flashcard_set_id, shared_user_id):
    try:
        # Ensure the current user owns the flashcard set
        current_user_id = get_jwt_identity()
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)

        if flashcard_set.user_id != current_user_id: # The current user requesting to share is not the owner
            return jsonify({'error': 'You do not have permission to share this flashcard set.'}), 403

        # Create a new UserFlashcardSet entry to represent the share
        new_share = UserFlashcardSet(user_id=shared_user_id, flashcard_set_id=flashcard_set.id)
        db.session.add(new_share)
        db.session.commit()
        return jsonify({"msg": "Flashcard set shared successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while sharing the flashcard set: {e}"}), 500

# Share Flashcard Set with Multiple Users
@flashcards_bp.route('/share_flashcard_set/<int:flashcard_set_id>', methods=['POST'])
@jwt_required()
def share_flashcard_set_users(flashcard_set_id):
    try:
        # Ensure the current user owns the flashcard set
        current_user_id = get_jwt_identity()
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)

        if flashcard_set is None:
            return jsonify({'error': 'Flashcard set not found.'}), 404

        if flashcard_set.user_id != current_user_id:
            return jsonify({'error': 'You do not have permission to share this flashcard set.'}), 403

        # Retrieve the list of user IDs from the request JSON
        shared_user_ids = request.json.get('user_ids', [])
        if not shared_user_ids:
            return jsonify({'error': 'No user IDs provided for sharing.'}), 400

        # Create a new UserFlashcardSet entry for each user ID in the list
        for shared_user_id in shared_user_ids:
            new_share = UserFlashcardSet(user_id=shared_user_id, flashcard_set_id=flashcard_set.id)
            db.session.add(new_share)

        db.session.commit()
        return jsonify({"msg": "Flashcard set shared successfully with all specified users."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while sharing the flashcard set: {e}"}), 500

@flashcards_bp.route('/unshare_flashcard_set/<int:flashcard_set_id>', methods=['DELETE'])
@jwt_required()
def unshare_flashcard_set(flashcard_set_id):
    try:
        current_user_id = get_jwt_identity()
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)

        if flashcard_set is None:
            return jsonify({'error': 'Flashcard set not found.'}), 404

        if flashcard_set.user_id != current_user_id:
            return jsonify({'error': 'You do not have permission to unshare this flashcard set. Try deleting instead.'}), 403

        # Retrieve the list of user IDs from the request JSON
        shared_user_ids = request.json.get('user_ids', [])
        if not shared_user_ids:
            return jsonify({'error': 'No user IDs provided for unsharing.'}), 400

        # Filter UserFlashcardSet for the given flashcard_set_id and user_ids
        user_flashcard_sets = UserFlashcardSet.query.filter(
            UserFlashcardSet.user_id.in_(shared_user_ids),
            UserFlashcardSet.flashcard_set_id == flashcard_set_id
        ).all()

        if not user_flashcard_sets:
            return jsonify({'error': 'No shared flashcard sets found for the provided user IDs.'}), 404

        # Delete the filtered UserFlashcardSet records
        for user_flashcard_set in user_flashcard_sets:
            db.session.delete(user_flashcard_set)

        db.session.commit()

        return jsonify({'message': 'Flashcard set unshared successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while unsharing the flashcard set: {e}"}), 500

"""########################################## Flashcard Sets ##########################################
# ENDPOINTS

Getting all flashcard sets:
GET /flashcards/flashcard_sets

Getting a specific flashcard set details:
GET /flashcards/flashcard_sets/<id>

Creating a flashcard set:
POST /flashcards/flashcard_sets

Updating a flashcard set:
PATCH /flashcards/flashcard_sets/<id>

Deleting a flashcard set:
DELETE /flashcards/flashcard_sets/<id>
"""



@flashcards_bp.route('/flashcard_sets', methods=['GET'])
@jwt_required()
def get_flashcard_set():
    flashcard_sets = FlashcardSet.query.all()

    name_query = request.args.get('name', '')

    current_user_id = get_jwt_identity()

    # Get the flashcard Sets owned by the User
    flashcard_sets = FlashcardSet.query.join(UserFlashcardSet).filter((FlashcardSet.user_id == current_user_id) | (UserFlashcardSet.user_id == current_user_id)).all()
    result = [flashcard_set.to_json() for flashcard_set in flashcard_sets]
    result = [flashcard_set for flashcard_set in result if name_query.lower() in flashcard_set['name'].lower()] # Filter by name

    return jsonify(result), 200

@flashcards_bp.route('/flashcard_sets/<int:id>', methods=['GET'])
@jwt_required()
def get_flashcard_set_details(id):
    try:
        current_user_id = get_jwt_identity()
        flashcard_set = FlashcardSet.query.get(id)

        if flashcard_set is None:
            return jsonify({'error': f'Flashcard Set ID {id} not found.'}), 404

        # Check if the user owns the flashcard set using UserFlashcardSet
        user_flashcard_set = UserFlashcardSet.query.filter_by(user_id=current_user_id, flashcard_set_id=id).first()
        if user_flashcard_set is None:
            return jsonify({'error': 'You do not have permission to view this flashcard set.'}), 403

        return jsonify(flashcard_set.to_json()), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred while getting flashcard set ID {id}: {e}'}), 500

@flashcards_bp.route('/flashcard_sets', methods=['POST'])
@jwt_required()
def create_flashcard_set():
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()

        # Data Validation
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Missing name field'}), 400

        # Create Flashcard Set
        new_flashcard_set = FlashcardSet(name=name, user_id=current_user_id)
        db.session.add(new_flashcard_set)
        db.session.commit()

        # Associate the Current User with the Flashcard Set
        user_flashcard_set = UserFlashcardSet(user_id=current_user_id, flashcard_set_id=new_flashcard_set.id)
        db.session.add(user_flashcard_set)
        db.session.commit()

        return jsonify({"msg": "Flashcard set created successfully.", "data":new_flashcard_set.to_json()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while creating the flashcard set: {e}'}), 500

@flashcards_bp.route('/flashcard_sets/<int:id>', methods=['PATCH'])
@jwt_required()
def update_flashcard_set(id):
    try:
        # Get the flashcard set from the database
        flashcard_set = FlashcardSet.query.get(id)
        current_user_id = get_jwt_identity()

        # Check if the flashcard set by the ID exists
        if flashcard_set is None:
            return jsonify({"error": f"Flashcard Set ID: {id} not found."}), 404

        # Check if the user owns the flashcard set or shared using UserFlashcardSet
        user_flashcard_set = UserFlashcardSet.query.filter_by(user_id=current_user_id, flashcard_set_id=id).first()
        if user_flashcard_set is None:
            return jsonify({'error': 'You do not have permission to update this flashcard set.'}), 403

        # Get the new name from the request
        data = request.get_json()

        # Update the flashcard set with the new name, set as old values if none
        flashcard_set.name = data.get('name', flashcard_set.name)

        db.session.commit()

        return jsonify({"msg": "Flashcard set updated successfully.", "data": flashcard_set.to_json()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error has occured while updating the flashcard set: {e}"}), 500

@flashcards_bp.route('/flashcard_sets/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_flashcard_set(id):
    try:
        flashcard_set = FlashcardSet.query.get(id)
        owner = flashcard_set.user_id
        current_user_id = get_jwt_identity()

        # Check if the user is the owner of the flashcard set
        if owner != current_user_id:
            return jsonify({"error": "You do not have permission to delete this flashcard set."}), 403

        # Check if the flashcard set exists
        if flashcard_set is None:
            return jsonify({"error": f"Flashcard Set ID {id} not found."}), 404
        db.session.delete(flashcard_set)
        db.session.commit()

        return jsonify({"msg": "Flashcard set deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while deleting the flashcard set: {e}"}), 500

"""########################################## Flashcards ##########################################
# ENDPOINTS

Getting all flashcards from a set:
GET /flashcards/flashcard_sets/<flashcard_set_id>/flashcards

Getting a specific flashcard set details from a set:
GET /flashcards/flashcard_sets/<flashcard_set_id>/flashcards/<flashcard_id>

Creating a flashcard in a set:
POST /flashcards/flashcard_sets/<flashcard_set_id>/flashcards

Updating a flashcard in a set:
PATCH /flashcards/flashcard_sets/<flashcard_set_id>/flashcards/<flashcard_id>

Deleting a flashcard in a set:
DELETE /flashcards/flashcard_sets/<flashcard_set_id>/flashcards/<flashcard_id>
"""

@flashcards_bp.route('/flashcard_sets/<int:flashcard_set_id>/flashcards', methods=['GET'])
@jwt_required()
def get_flashcards(flashcard_set_id):
    try:
        current_user_id = get_jwt_identity()
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)

        if flashcard_set is None:
            return jsonify({'error': f'Flashcard Set ID {flashcard_set_id} not found.'}), 404

        # Check if the user owns the flashcard set or shared using UserFlashcardSet
        user_flashcard_set = UserFlashcardSet.query.filter_by(user_id=current_user_id, flashcard_set_id=flashcard_set_id).first()
        if user_flashcard_set is None:
            return jsonify({'error': 'You do not have permission to view this flashcard from this set.'}), 403

        # Get the flashcards by the specified flashcard_set_id
        flashcards = Flashcard.query.filter_by(flashcard_set_id=flashcard_set_id).all()
        result = [flashcard.to_json() for flashcard in flashcards]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"And error has occurred while getting flashcard set ID {flashcard_set_id}: {e}"})

@flashcards_bp.route('/flashcard_sets/<int:flashcard_set_id>/flashcards/<int:id>', methods=['GET'])
@jwt_required()
def get_flashcard_details(flashcard_set_id, id):
    current_user_id = get_jwt_identity()

    # Check if the Flashcard is under the Flashcard Set
    flashcard = Flashcard.query.filter_by(id=id, flashcard_set_id=flashcard_set_id).first()
    if flashcard is None:
        return jsonify({'error': f'Flashcard ID {id} not found in Set {flashcard_set_id}.'}), 404

    # Check if the user owns the flashcard set or shared using UserFlashcardSet
    user_flashcard_set = UserFlashcardSet.query.filter_by(user_id=current_user_id, flashcard_set_id=flashcard_set_id).first()
    if user_flashcard_set is None:
        return jsonify({'error': 'You do not have permission to view this flashcard from this set.'}), 403

    if flashcard is None:
        return jsonify({'error', f'Flashcard ID {id} not found.'}), 404

    return jsonify(flashcard.to_json()), 200

@flashcards_bp.route('/flashcard_sets/<int:flashcard_set_id>/flashcards', methods=['POST'])
@jwt_required()
def create_flashcard(flashcard_set_id):
    try:
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)
        current_user_id = get_jwt_identity()

        if flashcard_set is None:
            return jsonify({'error': f'Flashcard Set ID {flashcard_set_id} not found.'}), 404

        # Check if the user owns the flashcard set or shared using UserFlashcardSet
        user_flashcard_set = UserFlashcardSet.query.filter_by(user_id=current_user_id, flashcard_set_id=flashcard_set_id).first()
        if user_flashcard_set is None:
            return jsonify({'error': 'You do not have permission to create a flashcard from this set.'}), 403

        # Get Request
        data = request.get_json()

        # Data Validation
        required_fields = ['word', 'definition']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field} field'}), 400

        # Retrieve Data
        word = data.get('word')
        definition = data.get('definition')

        # Create New Flashcard
        new_flashcard = Flashcard(word=word, definition=definition, flashcard_set_id=flashcard_set_id)
        db.session.add(new_flashcard)
        db.session.commit()

        return jsonify(new_flashcard.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while creating flashcard: {e}"}), 500

@flashcards_bp.route('/flashcard_sets/<int:flashcard_set_id>/flashcards/<int:flashcard_id>', methods=['PATCH'])
@jwt_required()
def update_flashcard(flashcard_set_id, flashcard_id):
    try:
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)
        current_user_id = get_jwt_identity()

        if flashcard_set is None:
            return jsonify({'error': f'Flashcard Set ID {flashcard_set_id} not found.'}), 404

        # Check if the user owns the flashcard set or shared using UserFlashcardSet
        user_flashcard_set = UserFlashcardSet.query.filter_by(user_id=current_user_id, flashcard_set_id=flashcard_set_id).first()
        if user_flashcard_set is None:
            return jsonify({'error': 'You do not have permission to create a flashcard from this set.'}), 403

        # Check if the Flashcard is under the Flashcard Set
        flashcard = Flashcard.query.filter_by(id=flashcard_id, flashcard_set_id=flashcard_set_id).first()
        if flashcard is None:
            return jsonify({'error': f'Flashcard ID {flashcard_id} not found in Set {flashcard_set_id}.'}), 404

        # Retrieve Request and Update
        data = request.get_json()
        flashcard.word = data.get('word', flashcard.word)
        flashcard.definition = data.get('definition', flashcard.definition)
        db.session.commit()

        return jsonify(
            {
            "msg": f"Flashcard {flashcard_id} of Set ID {flashcard_set_id} updated successfully.",
            "data": flashcard.to_json()
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while updating the flashcard: {e}'}), 500

@flashcards_bp.route('/flashcard_sets/<int:flashcard_set_id>/flashcards/<int:flashcard_id>', methods=['DELETE'])
@jwt_required()
def delete_flashcard(flashcard_set_id, flashcard_id):
    try:
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)
        current_user_id = get_jwt_identity()
        owner = flashcard_set.user_id

        if flashcard_set is None:
            return jsonify({'error': f'Flashcard Set ID {flashcard_set_id} not found.'}), 404

        if owner != current_user_id:
            return jsonify({'error': 'You do not have permission to delete a flashcard in this set.'}), 403

        # Check if the Flashcard is under the Flashcard Set
        flashcard = Flashcard.query.filter_by(id=id, flashcard_set_id=flashcard_set_id).first()
        if flashcard is None:
            return jsonify({'error': f'Flashcard ID {id} not found in Set {flashcard_set_id}.'}), 404

        # Delete
        db.session.delete(flashcard)
        db.session.commit()
        return jsonify({'msg': f'Flashcard ID {flashcard_id} deleted successfully.'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while deleting the flashcard: {e}'}), 500
