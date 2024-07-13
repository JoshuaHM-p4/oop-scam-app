import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import sys
import os
import json
import requests
import socketio

# Append paths to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'searchbar')))  # src/common/searchbar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

# Import necessary modules
from config import APP_NAME, BACKGROUND_COLOR, NOTES_ENDPOINT, API_BASE_URL
from searchbar import SearchBar  # Import SearchBar class
from .notes_model import NoteModel, NotebookModel
from .notes_page_view import PageViewer

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

        sio.connect(API_BASE_URL)
        sio.on('note_received', self.note_received)
        sio.on('notebook_received', self.notebook_received)
        self.current_room = None

    def tkraise(self):
        self.container.fetch_notebooks()
        self.container.display_notebooks()
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
            self.container.fetch_notebooks()
            self.container.display_notebooks()

    def send_notebook_update(self, data):
        sio.emit('notebook_update', {'notebook_id': data['notebook_id'], "user_id": data['user_id']})
        print('Sent notebook update:', data)

    def send_note_update(self, data):
        sio.emit('note_update', {'content': data, 'room': self.current_room})
        print('Sent note update:', data)

    def view_notebook(self, index, notebook):
        self.top_menu.pack_forget()
        self.container.pack_forget()
        self.notebook_page = NotebookPage(self, index, notebook)

    def back_to_notebooks(self):
        self.notebook_page.pack_forget()
        self.top_menu.pack(fill="x", padx=2, pady=(20,0))
        self.container.pack(fill="both", expand=True, padx=2, pady=2)
        self.container.display_notebooks()


class Container(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.current_note_index = 0
        self.setup_ui()

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=2)
        self.display_notebooks()

    def fetch_notebooks(self):
        response = requests.get(
            url=NOTES_ENDPOINT + "/notebooks",
            headers={"Authorization": f"Bearer {self.master.controller.access_token}"}
        )

        self.master.notebooks = []

        if response.status_code == 200:
            notebooks = response.json()
            for notebook in notebooks:
                self.master.notebooks.append(NotebookModel(
                id=notebook['notebook_id'],
                owner_id=notebook['owner_id'],
                title=notebook['title']
        ))
        else:
            messagebox.showerror("Error", "Failed to fetch notebooks.")

    def display_notebooks(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.master.notebooks:
            self.frame_scroll_container = ctk.CTkScrollableFrame(self, fg_color=BACKGROUND_COLOR)
            self.frame_scroll_container.pack(fill="both", expand=True, pady=(0,20))


            num_columns = 2  # Number of columns to display notebooks in

            for i, notebook in enumerate(self.master.notebooks):
                row, col = divmod(i, num_columns)

                # Assuming ctk and Image are properly imported and BACKGROUND_COLOR is defined
                ribbon_image = ctk.CTkImage(Image.open("assets/images/notebook.png"), size=(300, 300))

                notebook_button = ctk.CTkButton(self.frame_scroll_container,
                                                image=ribbon_image,
                                                width=300,
                                                height=300,
                                                text="",
                                                corner_radius=20,
                                                fg_color=BACKGROUND_COLOR,
                                                hover_color="#222B36",
                                                command=lambda i=i: self.view_notebook(i),
                                                compound="top")

                text_title = ctk.CTkLabel(notebook_button, text=notebook.title, font=("Arial", 20), fg_color="#E9E8F9", bg_color="#E9E8F9",
                                          text_color="black")
                text_title.place(relx=0.5, rely=0.5, anchor="center")
                if self.master.delete_mode:
                    # notebook_button.configure(hover_color="red", command=lambda i=i: self.delete_notebook(i))
                    notebook_button.configure(hover_color="red", command=lambda i=i: self.delete_notebook(notebook=self.master.notebooks[i], index=i))


                notebook_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Configure the grid to have equal weight for all columns
            for col in range(num_columns):
                self.frame_scroll_container.columnconfigure(col, weight=1)

            # Ensure all rows have equal weight
            for row in range((len(self.master.notebooks) + num_columns - 1) // num_columns):
                self.frame_scroll_container.rowconfigure(row, weight=1)
        else:
            no_notebooks_label = ctk.CTkLabel(self, text="No notebooks found.", font=("Arial", 20), fg_color=BACKGROUND_COLOR)
            no_notebooks_label.pack(fill="both", expand=True)

    def add_notebook(self, title):
        data = {"title": title}
        response = requests.post(
            url=NOTES_ENDPOINT + "/notebook",
            headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
            json=data
        )
        if response.status_code != 201:
            messagebox.showerror("Error", response.json()['message'])
            return
        notebook = response.json()['notebook']
        test_notebook = NotebookModel(id=notebook['id'], owner_id=notebook['user_id'], title=notebook['title']) # Example notes
        self.master.notebooks.append(test_notebook)
        messagebox.showinfo("Success", f"Notebook: {title} created successfully.")
        self.display_notebooks()

    def view_notebook(self, index):
        self.current_note_index = index
        notebook = self.master.notebooks[self.current_note_index]

        # Fetch notes for the selected notebook
        # <fetch notes for the selected notebook>
        self.master.view_notebook(self.current_note_index, notebook)

    # di na ata kailangan
    def edit_notebook_title(self, index, new_title):
        if new_title.strip() == "":
            messagebox.showerror("Error", "Title cannot be empty.")
            return
        self.master.notebooks[index].title = new_title
        self.display_notebooks()

    def delete_notebook(self, notebook, index):
        notebook_id = notebook.id
        notebook_title = notebook.title # Assuming each notebook has a 'title' attribute
        # Confirmation dialog
        response = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the '{notebook_title}' notebook?")
        if response:  # If user clicks 'Yes'
            # del self.master.notebooks[index]
            response = requests.delete(
                url=NOTES_ENDPOINT + f"/notebook/{notebook_id}",
                headers={"Authorization": f"Bearer {self.master.controller.access_token}"}
            )
            if response.status_code != 200:
                messagebox.showerror("Error", response.json()['message'])
            del self.master.notebooks[index]
            self.display_notebooks()

class TopMenu(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR)
        self.pack(fill="x", padx=2, pady=(20,0))

        # Add the SearchBar to the TopMenu
        self.search_bar = SearchBar(self, search_handler=self.search_notebooks)
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(20,0), pady=5)

        self.trash_img = ctk.CTkImage(Image.open("assets/images/trash_white.png"), size=(25, 25))
        self.plus_img = ctk.CTkImage(Image.open("assets/images/plus.png"), size=(25, 25))
        self.create_button = ctk.CTkButton(self, text="", fg_color="#222B36", command=self.create_notebook,
                                           height=37, corner_radius=20,
                                           image=self.plus_img
                                           )
        self.create_button.pack(side="left", padx=(20,0), fill="x")

        self.delete_button = ctk.CTkButton(self, text="", fg_color="#222B36", command=self.delete_notebook,
                                           height=37, corner_radius=20,

                                           image=self.trash_img
                                           )
        self.delete_button.pack(side="left", padx=(20), fill="x")

    def search_notebooks(self, query):
        # Example search handler
        matching_notebooks = [notebook for notebook in self.master.notebooks if query.lower() is notebook.title.lower()]
        if matching_notebooks:
            titles = "\n".join(notebook.title for notebook in matching_notebooks)
            messagebox.showinfo("Search Results", f"Found the following notebooks:\n{titles}")
        else:
            messagebox.showinfo("Search Results", "No matching notebooks found.")

    def create_notebook(self):
        dialog = ctk.CTkInputDialog(title="Create Notebook", text="Enter the title of the notebook:")
        title = dialog.get_input()
        if title:
            self.master.container.add_notebook(title)

    def delete_notebook(self):
        self.delete_button.configure(fg_color="red", text="Cancel", command=self.cancel_delete, hover_color="red")
        self.master.delete_mode = True
        self.master.container.display_notebooks()

    def cancel_delete(self):
        self.delete_button.configure(fg_color="#222B36", text="", command=self.delete_notebook, hover_color="#222B36")
        self.master.delete_mode = False
        self.master.container.display_notebooks()

class _TestingApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(APP_NAME)
        self.geometry("800x600")

        notebook_frame = NotebookFrame(self, self)
        notebook_frame.pack(fill="both", expand=True)

class NotebookPage(ctk.CTkFrame):
    def __init__(self, master, index, notebook, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.index = index
        self.notebook = notebook

        self.notebook_title = self.notebook.title
        self.content_dict = {}
        self.current_page = 1  # Start with page 1
        self.fetch_notes()
        self.total_pages = len(self.content_dict)
        self.master.join_room(f"note-{self.content_dict[self.current_page]['note_id']}")

        self.setup_ui()
        self.update_content()
        self.update_button_states()

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=2)

        self.return_img = ctk.CTkImage(Image.open("assets/images/back_arrow.png"), size=(25, 25))
        self.add_img = ctk.CTkImage(Image.open("assets/images/plus.png"), size=(25, 25))
        self.save_img = ctk.CTkImage(Image.open("assets/images/save.png"), size=(25, 25))

        self.notebook_title = ctk.CTkEntry(self, fg_color=BACKGROUND_COLOR, height=1, font=("Arial", 20), placeholder_text="Title:", width=200)
        self.notebook_title.pack( padx=10, pady=10, anchor="center")
        self.notebook_title.insert(0, self.notebook.title)

        self.top_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.top_frame.pack(fill="x", pady=(10,0))

        self.back_button = ctk.CTkButton(self.top_frame, text="", command= self.master.back_to_notebooks,
                                         image=self.return_img, width=25, height=25, corner_radius=20,
                                         fg_color=BACKGROUND_COLOR, hover_color="#222B36", border_width=0)
        self.back_button.pack(side="left", padx=10, expand=True, anchor="w")

        # self.label_notebook_title = ctk.CTkLabel(self.top_frame, text="Notebook Page", font=("Arial", 20), fg_color="red")
        # self.label_notebook_title.pack(side="left", padx=10, pady=10, expand=True, anchor="center")

        self.right_frame = ctk.CTkFrame(self.top_frame, fg_color=BACKGROUND_COLOR)
        self.right_frame.pack(side="left", padx=10,  expand=True, anchor="e")

        self.share_img = ctk.CTkImage(Image.open("assets/images/share.png"), size=(25, 25))
        self.share_button = ctk.CTkButton(self.right_frame, text="", image=self.share_img,
                                            width=25, height=25, corner_radius=20,
                                            fg_color=BACKGROUND_COLOR, hover_color="#222B36", border_width=0,
                                            command=self.share_notebook)
        self.share_button.pack(side="left", anchor="e")

        self.add_page_button = ctk.CTkButton(self.right_frame, text="", command= self.add_page,
                                             image=self.add_img, width=25, height=25, corner_radius=20,
                                             fg_color=BACKGROUND_COLOR, hover_color="#222B36", border_width=0)
        self.add_page_button.pack(side="left", anchor="e")

        self.save_button = ctk.CTkButton(self.right_frame, text="", command= self.save_page,
                                         image=self.save_img, width=25, height=25, corner_radius=20,
                                         fg_color=BACKGROUND_COLOR, hover_color="#222B36", border_width=0)
        self.save_button.pack(side="left",  anchor="e")

        # Title textbox
        self.title_entry = ctk.CTkEntry(self, fg_color=BACKGROUND_COLOR, height=1, font=("Arial", 20), placeholder_text="Title:",
                                          border_width=0, corner_radius=0)
        self.title_entry.pack(fill="x", padx=10, pady=10)

        self.title_entry.insert(0, self.content_dict[self.current_page]['title'])

        # Content textbox
        self.content_textbox = ctk.CTkTextbox(self, fg_color="white", height=1, text_color="black", border_width=0, corner_radius=0)
        self.content_textbox.pack(fill="both", expand=True, padx=10)
        # self.content_textbox.insert("0.0", "Some example text!\n" * 50)

        self.content_textbox.bind("<KeyRelease>", lambda event: self.master.send_note_update(self.content_textbox.get("1.0", "end-1c")))

        self.lower_frame = ctk.CTkFrame(self, height=20, fg_color=BACKGROUND_COLOR)
        self.lower_frame.pack(fill="x", padx=10, pady=10)

        self.previous_img_active = ctk.CTkImage(Image.open("assets/images/left_arrow.png"), size=(25, 25))
        self.next_img_active = ctk.CTkImage(Image.open("assets/images/right_arrow.png"), size=(25, 25))

        self.previous_img_disabled = ctk.CTkImage(Image.open("assets/images/left_arrow_disabled.png"), size=(25, 25))
        self.next_img_disabled = ctk.CTkImage(Image.open("assets/images/right_arrow_disabled.png"), size=(25, 25))


        self.left_button = ctk.CTkButton(self.lower_frame, text="",
                                         fg_color=BACKGROUND_COLOR,
                                         image=self.previous_img_disabled,
                                         width=25,
                                         height=25,
                                         command = self.previous_page,
                                        )
        self.left_button.pack(side="left", padx=10, expand=True)

        self.page_container = ctk.CTkFrame(self.lower_frame, fg_color=BACKGROUND_COLOR, corner_radius=20, border_width=1)
        self.page_container.pack(side="left", padx=10, expand=True)

        self.page_number = ctk.CTkLabel(self.page_container, text=f"Page {self.current_page} of {self.total_pages}", font=("Arial", 18), fg_color=BACKGROUND_COLOR)
        self.page_number.pack(fill="both", expand=True, padx=10, pady=5)

        self.page_number.bind("<Button-1>", lambda event: self.create_jump_to_page_popup())

        self.right_button = ctk.CTkButton(self.lower_frame, text="",
                                          fg_color=BACKGROUND_COLOR,
                                          image=self.next_img_active,
                                          width=25,
                                          height=25,
                                          command=self.next_page)
        self.right_button.pack(side="left", padx=10, expand=True)


    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_content()
            self.update_button_states()
            self.master.join_room(f"note-{self.content_dict[self.current_page]['note_id']}")

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_content()
            self.update_button_states()
            self.master.join_room(f"note-{self.content_dict[self.current_page]['note_id']}")

    def update_button_states(self):
    # Enable or disable buttons based on the current page
        if self.current_page > 1:
            self.left_button.configure(state="normal", image=self.previous_img_active)
        else:
            self.left_button.configure(state="disabled", image=self.previous_img_disabled)

        if self.current_page < self.total_pages:
            self.right_button.configure(state="normal", image=self.next_img_active)
        else:
            self.right_button.configure(state="disabled", image=self.next_img_disabled)

            # Update the page number label
            self.page_number.configure(text=f"Page {self.current_page}")

    def update_content(self):
        # Fetch and display content for the current page
        note = self.content_dict[self.current_page]
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, note['title'])
        self.content_textbox.delete("1.0", "end")
        self.content_textbox.insert("1.0", note['content'])
        # Update the page number label
        self.page_number.configure(text=f"Page {self.current_page} of {self.total_pages}")
        for item in self.content_dict:
            print(item, self.content_dict[item])

    def add_page(self):
        notebook_id = self.notebook.id
        response = requests.post(
            url=NOTES_ENDPOINT + f"/note/{notebook_id}",
            headers={"Authorization": f"Bearer {self.master.controller.access_token}"}
        )
        if response.status_code != 201:
            messagebox.showerror("Error", response.json()['message'])
            return
        note = response.json()['note']
        self.total_pages += 1
        self.content_dict[self.total_pages] = {'note_id': note['note_id'], 'content': note['content'], 'title': note['title']}
        self.current_page = self.total_pages
        self.update_content()
        self.update_button_states()
        self.master.join_room(f"note-{note['note_id']}")

    def create_jump_to_page_popup(self):
        dialog = ctk.CTkInputDialog(title="Jump to:", text="Enter the page number:")
        title = dialog.get_input()
        if title:
            self.jump_to_page(title)

    def share_notebook(self):
        dialog = ctk.CTkInputDialog(title="Share Notebook", text="Enter the email of the user you want to share the notebook with:")
        email = dialog.get_input()
        if email:
            response = requests.post(
                url=NOTES_ENDPOINT + f"/notebook/share/{self.notebook.id}",
                headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
                json={"email": email}
            )
            if response.status_code != 200:
                messagebox.showerror("Error", response.json()['message'])
                return
            messagebox.showinfo("Success", f"Notebook shared with {email}")
            user_to_share_with_id = response.json()['user_id']
            # self.master.send_notebook_update({"notebook_id": self.notebook_id, "user_id": user_to_share_with_id})
            self.master.send_notebook_update({"notebook_id": self.notebook.id, "user_id": user_to_share_with_id})

    def jump_to_page(self, page_number_str):
        try:
            page_number = int(page_number_str)
            if 1 <= page_number <= self.total_pages:
                self.current_page = page_number
                self.update_content()  # Assuming this method updates the content for the current page
                self.update_button_states()  # Update the state of navigation buttons
                self.master.join_room(f"note-{self.content_dict[self.current_page]['note_id']}")
            else:
                messagebox.showerror("Error", "Page number out of range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid page number.")

    def save_page(self):
        if self.notebook_title.get() != self.notebook.title:
            self.update_notebook_title()
        note_id = self.content_dict[self.current_page]['note_id']
        if self.title_entry.get() != self.content_dict[self.current_page]['title'] or self.content_textbox.get("1.0", "end-1c") != self.content_dict[self.current_page]['content']:
            response = requests.put(
                url=NOTES_ENDPOINT + f"/note/{note_id}",
                headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
                json={
                    "title": self.title_entry.get(),
                    "content": self.content_textbox.get("1.0", "end-1c")
                }
            )
            if response.status_code != 200:
                messagebox.showerror("Error", response.json()['message'])
                return
            messagebox.showinfo("Save", "Note saved successfully.")
            self.content_dict[self.current_page]['title'] = self.title_entry.get()
            self.content_dict[self.current_page]['content'] = self.content_textbox.get("1.0", "end-1c")

    def update_notebook_title(self):
        print('update_notebook_title')
        notebook_id = self.notebook.id
        response = requests.put(
            url=NOTES_ENDPOINT + f"/notebook-title/{notebook_id}",
            headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
            json={"title": self.notebook_title.get()}
        )
        if response.status_code != 200:
            messagebox.showerror("Error", response.json()['message'])
            return
        self.notebook.title = self.notebook_title.get()
        self.master.notebooks[self.index].title = self.notebook_title.get()
        messagebox.showinfo("Success", "Notebook title updated successfully")

    def fetch_notes(self):
        notebook_id = self.notebook.id
        response = requests.get(
            url=NOTES_ENDPOINT + f"/notes/{notebook_id}",
            headers={"Authorization": f"Bearer {self.master.controller.access_token}"}
        )
        if response.status_code != 200:
            messagebox.showerror("Error", response.json()['message'])
            return
        page_number = 1
        for note in response.json():
            self.content_dict[page_number] = note # {'content': note['content'], 'title': note['title']}
            page_number += 1


    #     self.notebooks: list[NotebookModel] = []
    #     self.current_notebook_id = None
    #     self.delete_mode = False

    #     self.top_menu = TopMenu(self)
    #     self.container = Container(self)

    #     self.configure(fg_color=BACKGROUND_COLOR,
    #                    corner_radius=10)
    #     self.grid_configure(padx=10, pady=10)

    # def tkraise(self):
    #     self.container.fetch_notebooks()
    #     self.container.display_notebooks()
    #     super().tkraise()

# class NotebookModel:
#     def __init__(self, id, owner_id, title, notes):
#         self.id = id
#         self.owner_id = owner_id
#         self.title = title
#         self.notes = notes



if __name__ == "__main__":
    app = _TestingApp()
    app.mainloop()

