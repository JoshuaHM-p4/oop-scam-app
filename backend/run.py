from app import create_app, db, socketio
import sqlalchemy as sa
from app.models import User, Flashcard, FlashcardSet, UserFlashcardSet
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'db': db, 'User': User, 'FlashcardSet': FlashcardSet, 'Flashcard': Flashcard, "UserFlashcardSet": UserFlashcardSet}

@app.route('/')
def index():
    return "Server is running"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_room')
def handle_join_room(data):
    user_id = data['user_id']
    room = data['room']
    join_room(room)
    print(f'User {user_id} joined room {room}')

@socketio.on('leave_room')
def handle_leave_room(data):
    user_id = data['user_id']
    room = data['room']
    leave_room(room)
    print(f'User {user_id} left room {room}')

@socketio.on('note_update')
def handle_note_update(data):
    print('Note update received')
    text = data['text']
    room = data['room']
    emit('note_received', text, room=room)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)