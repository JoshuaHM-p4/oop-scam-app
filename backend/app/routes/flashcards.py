from flask import Blueprint, request, jsonify

from app import db
from app.models import FlashcardSet, Flashcard

flashcards_bp = Blueprint('flashcards', __name__, url_prefix='/flashcards')


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
def get_flashcard_set():
    flashcard_sets = FlashcardSet.query.all()
    result = [flashcard_set.to_json() for flashcard_set in flashcard_sets]
    return jsonify(result), 200

@flashcards_bp.route('/flashcard_sets/<int:id>', methods=['GET'])
def get_flashcard_set_details(id):
    flashcard_set = FlashcardSet.query.get(id)

    if flashcard_set is None:
        return jsonify({'error', f'Flashcard Set ID {id} not found.'}), 404

    return jsonify(flashcard_set.to_json()), 200

@flashcards_bp.route('/flashcard_sets', methods=['POST'])
def create_flashcard_set():
    try:
        data = request.get_json()

        required_fields = ['name', 'user_id']

        for field in required_fields:
            if not data.get(field, ""):
                return jsonify({'error': f'Missing {field} field'}), 400

        name = data.get('name')
        user_id = data.get('user_id')

        new_flashcard_set = FlashcardSet(name=name, user_id=user_id)
        db.session.add(new_flashcard_set)
        db.session.commit()

        return jsonify({"msg": "Flashcard set created successfully.", "data":new_flashcard_set.to_json()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while creating the flashcard set: {e}'}), 500

@flashcards_bp.route('/flashcard_sets/<int:id>', methods=['PATCH'])
def update_flashcard_set(id):
    try:
        # Get the flashcard set from the database
        flashcard_set = FlashcardSet.query.get(id)

        if flashcard_set is None:
            return jsonify({"error": f"Flashcard Set ID: {id} not found."}), 404

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
def delete_flashcard_set(id):
    try:
        flashcard_set = FlashcardSet.query.get(id)
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
def get_flashcards(flashcard_set_id):
    try:
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)
        if flashcard_set is None:
            return jsonify({'error': f'Flashcard Set ID {flashcard_set_id} not found.'}), 404

        flashcards = Flashcard.query.filter_by(flashcard_set_id=flashcard_set_id).all()
        result = [flashcard.to_json() for flashcard in flashcards]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"And error has occurred while getting flashcard set ID {flashcard_set_id}: {e}"})

@flashcards_bp.route('/flashcard_sets/<int:flashcard_set_id>/flashcards/<int:id>', methods=['GET'])
def get_flashcard_details(flashcard_set_id, id):
    flashcard = Flashcard.query.get(id)

    if flashcard is None:
        return jsonify({'error', f'Flashcard ID {id} not found.'}), 404

    return jsonify(flashcard.to_json()), 200

@flashcards_bp.route('/flashcard_sets/<int:flashcard_set_id>/flashcards', methods=['POST'])
def create_flashcard(flashcard_set_id):
    try:
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)

        if flashcard_set is None:
            return jsonify({'error': f'Flashcard Set ID {flashcard_set_id} not found.'}), 404

        data = request.get_json()

        required_fields = ['word', 'definition']

        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field} field'}), 400

        word = data.get('word')
        definition = data.get('definition')

        new_flashcard = Flashcard(word=word, definition=definition, flashcard_set_id=flashcard_set_id)
        db.session.add(new_flashcard)
        db.session.commit()

        return jsonify(new_flashcard.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while creating flashcard: {e}"}), 500

@flashcards_bp.route('/flashcard_sets/<int:flashcard_set_id>/flashcards/<int:flashcard_id>', methods=['PATCH'])
def update_flashcard(flashcard_set_id, flashcard_id):
    try:
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)

        if flashcard_set is None:
            return jsonify({'error': f'Flashcard Set ID {flashcard_set_id} not found.'}), 404

        flashcard = Flashcard.query.filter_by(flashcard_set_id=flashcard_set_id, id=flashcard_id).first()

        if flashcard is None:
            return jsonify({'error': f'Flashcard ID {flashcard_id} not found.'}), 404

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
def delete_flashcard(flashcard_set_id, flashcard_id):
    try:
        flashcard_set = FlashcardSet.query.get(flashcard_set_id)

        if flashcard_set is None:
            return jsonify({'error': f'Flashcard Set ID {flashcard_set_id} not found.'}), 404

        flashcard = Flashcard.query.filter_by(flashcard_set_id=flashcard_set_id, id=flashcard_id).first()

        if flashcard is None:
            return jsonify({'error': f'Flashcard ID {flashcard_id} not found.'}), 404

        db.session.delete(flashcard)
        db.session.commit()
        return jsonify({'msg': f'Flashcard ID {flashcard_id} deleted successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while deleting the flashcard: {e}'}), 500
