import customtkinter as ctk
import sys
import os
import socketio

# Append paths to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

# Import necessary modules
from config import APP_NAME, BACKGROUND_COLOR, NOTES_ENDPOINT, API_BASE_URL
from loading import LoadingFrame
from .notes_model import NoteModel, NotebookModel
from .top_menu_gui import TopMenu
from .container_gui import Container
from .page_gui import NotebookPageFrame

sio = socketio.Client()
class NotebookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.notebooks: list[NotebookModel] = []
        self.current_notebook_id = None
        self.delete_mode = False

        self.top_menu = TopMenu(self)
        self.container = Container(self)

        self.configure(fg_color=BACKGROUND_COLOR,
                       corner_radius=10)
        self.grid_configure(padx=10, pady=10)

        self.current_room = None

    def connect(self):
        sio.connect(API_BASE_URL)
        sio.on('note_received', self.note_received)
        sio.on('notebook_received', self.notebook_received)

    def loading(self):
        self.loading_frame = LoadingFrame(self.container, fg_color = BACKGROUND_COLOR)
        self.loading_frame.pack(expand=True, padx=(50,50), pady=(100,3))

    def update_notebooks(self):
        self.container.fetch_notebooks()

    def tkraise(self):
        self.loading()
        self.update_notebooks()
        super().tkraise()

    def join_room(self, room_name):
        if self.current_room:
            sio.emit('leave_room', {'user_id': self.controller.user.user_id, 'room': self.current_room})
        sio.emit('join_room', {'user_id': self.controller.user.user_id, 'room': room_name})
        self.current_room = room_name

    @sio.event
    def note_received(self, data):
        print('Received note update:', data['content'])
        print('Current room:', data['room'])
        room_id = data['room'].split('-')[1]
        if str(room_id) == str(self.notebook_page.content_dict[self.notebook_page.current_page]['note_id']):
            self.notebook_page.content_textbox.delete("1.0", "end")
            self.notebook_page.content_textbox.insert("1.0", data['content'])
        for page_number, note in self.notebook_page.content_dict.items():
            if str(note['note_id']) == str(room_id):
                self.notebook_page.content_dict[page_number]['content'] = data['content']
                break

    @sio.event
    def notebook_received(self, data):
        print('Received notebook update:', data['notebook_id'])
        print(str(data['user_id']) == str(self.controller.user.user_id))
        print(data['user_id'], type(data['user_id'])) # 1 (right)
        print(self.controller.user.user_id, type(self.controller.user.user_id)) # 0 (wrong)
        if str(data['user_id']) == str(self.controller.user.user_id):
            self.update_notebooks()

    def send_notebook_update(self, data):
        sio.emit('notebook_update', {'notebook_id': data['notebook_id'], "user_id": data['user_id']})
        print('Sent notebook update:', data)

    def send_note_update(self, data):
        sio.emit('note_update', {'content': data, 'room': self.current_room})
        print('Sent note update:', data)

    def view_notebook(self, index, notebook):
        self.top_menu.pack_forget()
        self.container.pack_forget()
        self.notebook_page = NotebookPageFrame(self, index, notebook)
        self.notebook_page.fetch_notes()

    def back_to_notebooks(self):
        self.notebook_page.pack_forget()
        self.top_menu.pack(fill="x", padx=2, pady=(20,0))
        self.container.pack(fill="both", expand=True, padx=2, pady=2)
        self.container.display_notebooks()

if __name__ == "__main__":
    pass
    # app = _TestingApp()
    # app.mainloop()

