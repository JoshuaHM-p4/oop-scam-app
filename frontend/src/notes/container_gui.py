import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import sys
import os
import json
import requests
import threading

# Append paths to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

# Import necessary modules
from config import APP_NAME, BACKGROUND_COLOR, NOTES_ENDPOINT, API_BASE_URL
from .notes_model import NoteModel, NotebookModel

class Container(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.current_note_index = 0

        self.fetch_lock = threading.Lock()
        self.add_lock = threading.Lock()
        self.delete_lock = threading.Lock()

        self.setup_ui()

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=2)
        self.display_notebooks()

    def display_notebooks(self, empty=False):
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
        elif empty:
            no_notebooks_label = ctk.CTkLabel(self, text="No notebooks found.", font=("Arial", 20), fg_color=BACKGROUND_COLOR)
            no_notebooks_label.pack(fill="both", expand=True)

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

    def fetch_notebooks(self):
        self.master.notebooks = []

        def get_request():
            if not self.fetch_lock.acquire(blocking=False):
                print('Fetch request already in progress.')
                return

            lock_acquired = True
            try:
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
                    show_as_empty = bool(not notebooks)
                    self.after(0, self.display_notebooks, show_as_empty)
                    self.after(0, self.master.connect)
                else:
                    messagebox.showerror("Error", "Failed to fetch notebooks.")

            except ConnectionError:
                messagebox.showerror("Error", "Failed to connect to the server.")
            finally:
                if lock_acquired:
                    self.fetch_lock.release()

        threading.Thread(target=get_request).start()

    def add_notebook(self, title):
        def post_request():
            if not self.add_lock.acquire(blocking=False):
                print('Add request already in progress.')
                return

            lock_acquired = True

            try:
                data = {"title": title}
                response = requests.post(url=NOTES_ENDPOINT + "/notebook",
                    headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
                    json=data
                )
                if response.status_code != 201:
                    messagebox.showerror("Error", response.json()['message'])
                    return
                notebook = response.json()['notebook']
                test_notebook = NotebookModel(id=notebook['id'], owner_id=notebook['user_id'], title=notebook['title']) # Example notes
                self.master.notebooks.append(test_notebook)
                self.after(0, self.display_notebooks)
            except ConnectionError:
                messagebox.showerror("Error", "Failed to connect to the server.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                if lock_acquired:
                    self.add_lock.release()

        threading.Thread(target=post_request).start()


    def delete_notebook(self, notebook, index):

        def delete_request():
            if not self.delete_request.acquire(blocking=False):
                print('Delete request already in progress.')
                return

            lock_acquired = True

            try:
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
                    self.after(0, self.display_notebooks)
            except ConnectionError:
                messagebox.showerror("Error", "Failed to connect to the server.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                if lock_acquired:
                    self.add_lock.release()

        threading.Thread(target=delete_request).start()
