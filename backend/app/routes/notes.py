from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db

from app.models import User, Note, Notebook, UserNotebook, QuickNote, UserQuickNotes

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

# for fetching all of the users and shared quick notes
@notes_bp.route('/quick-notes', methods=['GET'])
@jwt_required()
def get_user_quick_notes():
    try:
    # get the user id from the jwt token
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # list to store the quick notes that will be returned
        quick_notes = [] 
        # get all the quick notes that the user has created
        user_quick_notes = UserQuickNotes.query.filter_by(user_id=user.id).all()
        # loop through the user_quick_notes and get the quick note data
        for user_quick_note in user_quick_notes:
            quick_note = QuickNote.query.get(user_quick_note.quick_note_id)
            quick_note_data = quick_note.to_json()
            data_to_be_append = {
                'quick_note_id': quick_note_data.get('id'),
                'title': quick_note_data.get('title'),
                'content': quick_note_data.get('content'),
                'owner_id': quick_note_data.get('owner_id'), # owner_id is the user id of the user who created the quick note
                'is_owner': True # is_owner is a boolean that indicates if the user is the owner of that quick note
            }
            # if the owner_id of the quick note is not the same as the user id, set is_owner to False
            if quick_note_data.get('owner_id') != user.id:
                data_to_be_append['is_owner'] = False # is_owner is a boolean that indicates if the user is the owner of that quick note
            quick_notes.append(data_to_be_append)
        return jsonify(quick_notes), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# for fetching a specific quick note
@notes_bp.route('/quick-note/<int:quick_note_id>', methods=['GET'])
@jwt_required()
def get_quick_note(quick_note_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the quick note object
        quick_note = QuickNote.query.get(quick_note_id)
        # if the quick note does not exist, return a 404
        if not quick_note:
            return jsonify({'message': 'Quick note not found'}), 404
        # get the quick note data
        is_user_access = UserQuickNotes.query.filter_by(user_id=user.id, quick_note_id=quick_note_id).first()
        if not is_user_access:
            return jsonify({'message': 'Unauthorized'}), 401
        quick_note_data = quick_note.to_json()
        data_to_be_returned = {
            'quick_note_id': quick_note_data.get('id'),
            'title': quick_note_data.get('title'),
            'content': quick_note_data.get('content'),
            'owner_id': quick_note_data.get('owner_id'),
            'is_owner': True 
        }
        # if is_user_access is None, return Unauthorized
        return jsonify(data_to_be_returned), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# for creating a quick note
@notes_bp.route('/quick-note', methods=['POST'])
@jwt_required()
def create_user_notes():
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the data from the request
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        # if the title or content is missing, return a 400
        if not title or not content:
            return jsonify({'message': 'Title and content are required'}), 400
        # create a new quick note
        new_quick_note = QuickNote(title=title, content=content, owner_id=user.id)
        db.session.add(new_quick_note)
        db.session.commit()
        quick_note_id = new_quick_note.id
        new_user_quick_note = UserQuickNotes(user_id=user.id, quick_note_id=new_quick_note.id)
        # add the new quick note to the database
        db.session.add(new_user_quick_note)
        db.session.commit()
        # return a 201 response
        return jsonify({'message': 'Quick note created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# for updating a quick note
@notes_bp.route('/quick-note/<int:quick_note_id>', methods=['PUT'])
@jwt_required()
def update_quick_note(quick_note_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        is_user_access = UserQuickNotes.query.filter_by(user_id=user.id, quick_note_id=quick_note_id).first()
        # if the user does not have access to the quick note, return a 403
        if not is_user_access:
            return jsonify({'message': 'You do not have access to this quick note'}), 403 
        # get the quick note object
        quick_note = QuickNote.query.get(quick_note_id)
        # if the quick note does not exist, return a 404
        if not quick_note:
            return jsonify({'message': 'Quick note not found'}), 404
        # get the data from the request
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        # if the title or content is missing, return a 400
        if not title or not content:
            return jsonify({'message': 'Title and content are required'}), 400
        # update the quick note
        quick_note.title = title
        quick_note.content = content
        db.session.commit()
        # return a 200 response
        return jsonify({'message': 'Quick note updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    

# for deleting a quick note
@notes_bp.route('/quick-note/<int:quick_note_id>', methods=['DELETE'])
@jwt_required()
def delete_quick_note(quick_note_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the quick note object
        quick_note = QuickNote.query.get(quick_note_id)
        # if the quick note does not exist, return a 404
        if not quick_note:
            return jsonify({'message': 'Quick note not found'}), 404
        is_user_access = UserQuickNotes.query.filter_by(user_id=user.id, quick_note_id=quick_note_id).first()
        # if the user does not have access to the quick note, return a 403
        if not is_user_access:
            return jsonify({'message': 'You do not have access to delete this quick note'}), 403
        # delete the quick note
        db.session.delete(quick_note)
        db.session.commit()
        # return a 200 response
        return jsonify({'message': 'Quick note deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# for sharing a quick note
@notes_bp.route('/quick-note/share/<int:quick_note_id>', methods=['POST'])
@jwt_required()
def share_quick_note(quick_note_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the quick note object
        quick_note = QuickNote.query.get(quick_note_id)
        # if the quick note does not exist, return a 404
        if not quick_note:
            return jsonify({'message': 'Quick note not found'}), 404
        # get the data from the request
        data = request.get_json()
        email = data.get('email')
        # if the email is missing, return a 400
        if not email:
            return jsonify({'message': 'Email is required'}), 400
        # get the user with the email
        user_to_share_with = User.query.filter_by(email=email).first()
        # if the user does not exist, return a 404
        if not user_to_share_with:
            return jsonify({'message': 'User not found'}), 404
        # create a new user quick note
        new_user_quick_note = UserQuickNotes(user_id=user_to_share_with.id, quick_note_id=quick_note.id)
        # add the new user quick note to the database
        db.session.add(new_user_quick_note)
        db.session.commit()
        # return a 200 response
        return jsonify({'message': 'Quick note shared successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    

@notes_bp.route('/quick-note/unshare/<int:quick_note_id>', methods=['POST'])
@jwt_required()
def unshare_quick_note(quick_note_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the quick note object
        quick_note = QuickNote.query.get(quick_note_id)
        # if the quick note does not exist, return a 404
        if not quick_note:
            return jsonify({'message': 'Quick note not found'}), 404
        if quick_note.owner_id != user.id:
            return jsonify({'message': 'You do not have access to unshare this quick note'}), 403
        # get the data from the request
        data = request.get_json()
        email = data.get('email')
        # if the email is missing, return a 400
        if not email:
            return jsonify({'message': 'Email is required'}), 400
        # get the user with the email
        user_to_unshare_with = User.query.filter_by(email=email).first()
        # if the user does not exist, return a 404
        if not user_to_unshare_with:
            return jsonify({'message': 'User not found'}), 404
        # get the user quick note object
        user_quick_note = UserQuickNotes.query.filter_by(user_id=user_to_unshare_with.id, quick_note_id=quick_note.id).first()
        # if the user quick note does not exist, return a 404
        if not user_quick_note:
            return jsonify({'message': 'User quick note not found'}), 404
        # delete the user quick note
        db.session.delete(user_quick_note)
        db.session.commit()
        # return a 200 response
        return jsonify({'message': 'Quick note unshared successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
################################# Notebook #################################

# for creating a notebook
@notes_bp.route('/notebook', methods=['POST'])
@jwt_required()
def create_notebook():
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the data from the request
        data = request.get_json()
        title = data.get('title')
        # if the title is missing, return a 400
        if not title:
            return jsonify({'message': 'Title is required'}), 400
        # create a new notebook
        new_notebook = Notebook(title=title, owner_id=user.id)
        db.session.add(new_notebook)
        db.session.commit()
        # create a new user notebook
        new_user_notebook = UserNotebook(user_id=user.id, notebook_id=new_notebook.id)
        db.session.add(new_user_notebook)
        db.session.commit()
        # return a 201 response
        return jsonify({'message': 'Notebook created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    

# for fetching all the notebooks
@notes_bp.route('/notebooks', methods=['GET'])
@jwt_required()
def get_notebooks():
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # list to store the notebooks that will be returned
        notebooks = []
        # get all the user notebooks
        user_notebooks = UserNotebook.query.filter_by(user_id=user.id).all()
        # loop through the user notebooks and get the notebook data
        for user_notebook in user_notebooks:
            notebook = Notebook.query.get(user_notebook.notebook_id)
            notebook_data = {
                'notebook_id': notebook.id,
                'title': notebook.title,
                'owner_id': notebook.owner_id,
                'is_owner': False
            }
            # if the owner_id of the notebook is the same as the user id, set is_owner to True
            if notebook.owner_id == user.id:
                notebook_data['is_owner'] = True
            notebooks.append(notebook_data)
        return jsonify(notebooks), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    

# for creating note in a notebook
@notes_bp.route('/note/<int:notebook_id>', methods=['POST'])
@jwt_required()
def create_note(notebook_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the data from the request
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        # if the notebook_id, title or content is missing, return a 400
        if not notebook_id or not title or not content:
            return jsonify({'message': 'Notebook id, title and content are required'}), 400
        # get the notebook object
        notebook = Notebook.query.get(notebook_id)
        # if the notebook does not exist, return a 404
        if not notebook:
            return jsonify({'message': 'Notebook not found'}), 404
        # create a new note
        new_note = Note(notebook_id=notebook.id, title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        # return a 201 response
        return jsonify({'message': 'Note created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    

# for fetching all the notes in a notebook
@notes_bp.route('/notes/<int:notebook_id>', methods=['GET'])
@jwt_required()
def get_notes(notebook_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the notebook object
        notebook = Notebook.query.get(notebook_id)
        # if the notebook does not exist, return a 404
        if not notebook:
            return jsonify({'message': 'Notebook not found'}), 404
        # list to store the notes that will be returned
        notes = []
        # get all the notes in the notebook
        notes_in_notebook = Note.query.filter_by(notebook_id=notebook.id).all()
        # loop through the notes and get the note data
        for note in notes_in_notebook:
            note_data = {
                'note_id': note.id,
                'title': note.title,
                'content': note.content
            }
            notes.append(note_data)
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# for updating a note in a notebook
@notes_bp.route('/note/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the note object
        note = Note.query.get(note_id)
        # if the note does not exist, return a 404
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        # check if the user has access to the notebook
        is_access = UserNotebook.query.filter_by(user_id=user.id, notebook_id=note.notebook_id).first()
        # if the user does not have access to the notebook, return a 403
        if not is_access:
            return jsonify({'message': 'You do not have access to this notebook'}), 403
        # get the data from the request
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        # if the title or content is missing, return a 400
        if not title or not content:
            return jsonify({'message': 'Title and content are required'}), 400
        # update the note
        note.title = title
        note.content = content
        db.session.commit()
        # return a 200 response
        return jsonify({'message': 'Note updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# for deleting a note in a notebook
@notes_bp.route('/note/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the note object
        note = Note.query.get(note_id)
        # if the note does not exist, return a 404
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        # check if the user has access to the notebook
        is_access = UserNotebook.query.filter_by(user_id=user.id, notebook_id=note.notebook_id).first()
        # if the user does not have access to the notebook, return a 403
        if not is_access:
            return jsonify({'message': 'You do not have access to this notebook'}), 403
        # delete the note
        db.session.delete(note)
        db.session.commit()
        # return a 200 response
        return jsonify({'message': 'Note deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# for sharing a notebook
@notes_bp.route('/notebook/share/<int:notebook_id>', methods=['POST'])
@jwt_required()
def share_notebook(notebook_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the notebook object
        notebook = Notebook.query.get(notebook_id)
        # if the notebook does not exist, return a 404
        if not notebook:
            return jsonify({'message': 'Notebook not found'}), 404
        is_owner = notebook.owner_id == user.id
        # if the user is not the owner of the notebook, return a 403
        if not is_owner:
            return jsonify({'message': 'You do not have access to share this notebook'}), 403
        # get the data from the request
        data = request.get_json()
        email = data.get('email')
        # if the email is missing, return a 400
        if not email:
            return jsonify({'message': 'Email is required'}), 400
        # get the user with the email
        user_to_share_with = User.query.filter_by(email=email).first()
        # if the user does not exist, return a 404
        if not user_to_share_with:
            return jsonify({'message': 'User not found'}), 404
        # create a new user notebook
        new_user_notebook = UserNotebook(user_id=user_to_share_with.id, notebook_id=notebook.id)
        db.session.add(new_user_notebook)
        db.session.commit()
        # return a 200 response
        return jsonify({'message': 'Notebook shared successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# for unsharing a notebook
@notes_bp.route('/notebook/unshare/<int:notebook_id>', methods=['POST'])
@jwt_required()
def unshare_notebook(notebook_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the notebook object
        notebook = Notebook.query.get(notebook_id)
        # if the notebook does not exist, return a 404
        if not notebook:
            return jsonify({'message': 'Notebook not found'}), 404
        is_owner = notebook.owner_id == user.id
        # if the user is not the owner of the notebook, return a 403
        if not is_owner:
            return jsonify({'message': 'You do not have access to unshare this notebook'}), 403
        # get the data from the request
        data = request.get_json()
        email = data.get('email')
        # if the email is missing, return a 400
        if not email:
            return jsonify({'message': 'Email is required'}), 400
        # get the user with the email
        user_to_unshare_with = User.query.filter_by(email=email).first()
        # if the user does not exist, return a 404
        if not user_to_unshare_with:
            return jsonify({'message': 'User not found'}), 404
        # get the user notebook object
        user_notebook = UserNotebook.query.filter_by(user_id=user_to_unshare_with.id, notebook_id=notebook.id).first()
        # if the user notebook does not exist, return a 404
        if not user_notebook:
            return jsonify({'message': 'User notebook not found'}), 404
        # delete the user notebook
        db.session.delete(user_notebook)
        db.session.commit()
        # return a 200 response
        return jsonify({'message': 'Notebook unshared successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
# for deleting a notebook
@notes_bp.route('/notebook/<int:notebook_id>', methods=['DELETE'])
@jwt_required()
def delete_notebook(notebook_id):
    try:
        # get the user id from the jwt token
        user_id = get_jwt_identity()
        # get the user object
        user = User.query.get(user_id)
        # if the user does not exist, return a 404
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # get the notebook object
        notebook = Notebook.query.get(notebook_id)
        # if the notebook does not exist, return a 404
        if not notebook:
            return jsonify({'message': 'Notebook not found'}), 404
        is_owner = notebook.owner_id == user.id
        # if the user is not the owner of the notebook, return a 403
        if not is_owner:
            return jsonify({'message': 'You do not have access to delete this notebook'}), 403
        # delete the notebook
        db.session.delete(notebook)
        db.session.commit()
        # return a 200 response
        return jsonify({'message': 'Notebook deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    



    