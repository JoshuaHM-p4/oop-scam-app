import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import sys
import os
import json
import requests

# Append paths to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'searchbar')))  # src/common/searchbar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

# Import necessary modules
from config import APP_NAME, BACKGROUND_COLOR, NOTES_ENDPOINT
from searchbar import SearchBar  # Import SearchBar class
from .notes_model import NoteModel, NotebookModel
from .notes_page_view import PageViewer

class NotebookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = self.controller.user

        self.notebooks: list[NotebookModel] = []
        self.current_notebook_id = None

        self.top_menu = TopMenu(self)
        self.container = Container(self)
        self.configure(fg_color=BACKGROUND_COLOR,
                       corner_radius=10)
        self.grid_configure(padx=10, pady=10)
    
    def tkraise(self):
        self.container.fetch_notebooks()
        self.container.display_notebooks()
        super().tkraise()

class Container(ctk.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.current_note_index = 0
        self.setup_ui()
        self.user = self.master.user

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=(0,3))
        # self.fetch_notebooks()
        self.display_notebooks()

    # def setup_ui(self):
    #     self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
    #     self.pack(fill="both", expand=True, padx=2, pady=(0,3))

    #     # Create canvas and scrollbar
    #     self.canvas = tk.Canvas(self, highlightthickness=0, bg=BACKGROUND_COLOR)
    #     self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
    #     self.canvas.configure(yscrollcommand=self.scrollbar.set)

    #     self.scrollbar.pack(side="right", fill="y")
    #     self.canvas.pack(side="left", fill="both", expand=True)

    #     self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#141A1F")

    #     self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

    #     self.scrollable_frame.bind(
    #         "<Configure>",
    #         lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    #     )

    #     self.display_notebooks()

    def fetch_notebooks(self): 
        response = requests.get(
            url=NOTES_ENDPOINT + "/notebooks",
            headers={"Authorization": f"Bearer {self.master.controller.access_token}"}
        )

        self.master.notebooks = []

        if response.status_code == 200: 
            notebooks = response.json()
            print(notebooks)
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

        for i, notebook in enumerate(self.master.notebooks):

            # notebook.title: str
            # notebook.notes: list

            row, col = divmod(i, 2)

            # Assuming ctk and Image are properly imported and BACKGROUND_COLOR is defined
            ribbon_image = ctk.CTkImage(Image.open("assets/images/note_placeholder.png"), size=(200, 300))
            notebook_button = ctk.CTkButton(self, image=ribbon_image, text="", fg_color=BACKGROUND_COLOR, hover_color="#222B36", command=lambda i=i: self.view_notebook(i))
            notebook_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Configure the grid to center the content
            self.rowconfigure(row, weight=1)
            self.columnconfigure(col, weight=1)

            # Center the image
            notebook_button.grid_columnconfigure(col, weight=1)
            notebook_button.grid_rowconfigure(row, weight=1)

    def add_notebook(self, title="New Notebook"):
        data = {"title": title}
        response = requests.post(
            url=NOTES_ENDPOINT + "/notebook",
            headers={"Authorization": f"Bearer {self.master.controller.access_token}"},
            json=data
        )
        if response.status_code != 201:
            messagebox.showerror("Error", "Failed to create notebook.")
            return
        notebook = response.json()['notebook']
        print(self.user.user_id)
        test_notebook = NotebookModel(id=notebook.id, owner_id=notebook.owner_id, title=title) # Example notes
        self.master.notebooks.append(test_notebook)
        self.display_notebooks()
        self.save_notebooks()

    def view_notebook(self, index):
        self.current_note_index = index
        notebook = self.master.notebooks[self.current_note_index]

        viewer = PageViewer(self, notebook)
        viewer.grab_set()

    def edit_notebook_title(self, index, new_title):
        if new_title.strip() == "":
            messagebox.showerror("Error", "Title cannot be empty.")
            return
        self.master.notebooks[index].title = new_title
        self.display_notebooks()

    def delete_notebook(self, index):
        del self.master.notebooks[index]
        self.display_notebooks()

class TopMenu(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR)
        self.pack(fill="x", padx=2, pady=(9,0))

        # Add the SearchBar to the TopMenu
        self.search_bar = SearchBar(self, search_handler=self.search_notebooks)
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(11,0), pady=5)

        self.create_button = ctk.CTkButton(self, text="Create", fg_color="#222B36", hover_color="#141A1F", command=self.create_notebook)
        self.create_button.pack(side="left", padx=10)

        self.edit_button = ctk.CTkButton(self, text="Edit", fg_color="#222B36", hover_color="#141A1F", command=self.edit_notebook)
        self.edit_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(self, text="Delete", fg_color="#222B36", hover_color="#141A1F", command=self.delete_notebook)
        self.delete_button.pack(side="left", padx=10)

    def search_notebooks(self, query):
        # Example search handler
        matching_notebooks = [notebook for notebook in self.master.notebooks if query.lower() is notebook.title.lower()]
        if matching_notebooks:
            titles = "\n".join(notebook.title for notebook in matching_notebooks)
            messagebox.showinfo("Search Results", f"Found the following notebooks:\n{titles}")
        else:
            messagebox.showinfo("Search Results", "No matching notebooks found.")

    def create_notebook(self):
        title = simpledialog.askstring("Notebook Title", "Enter the title of the new notebook:")
        if title:
            self.master.container.add_notebook(title)

    def edit_notebook(self):
        def select_notebook():
            selected_index = notebook_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "No notebook selected.")
                return
            selected_index = selected_index[0]
            new_title = title_entry.get()
            self.master.container.edit_notebook_title(selected_index, new_title)
            edit_window.destroy()

        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Edit Notebook")
        edit_window.geometry("300x200")
        edit_window.configure(fg_color="#141A1F")

        title_label = ctk.CTkLabel(edit_window, text="New Title:", text_color="white")
        title_label.pack(pady=10)

        title_entry = ctk.CTkEntry(edit_window)
        title_entry.pack(pady=5)

        notebook_listbox = tk.Listbox(edit_window)
        notebook_listbox.pack(pady=5, fill="both", expand=True)

        for i, notebook in enumerate(self.master.notebooks):
            notebook_listbox.insert(tk.END, notebook.title)

        save_button = ctk.CTkButton(edit_window, text="Save", command=select_notebook)
        save_button.pack(pady=10)

    def delete_notebook(self):
        selected_index = simpledialog.askinteger("Delete Notebook", "Enter the index of the notebook to delete:")
        if selected_index is not None and 0 <= selected_index < len(self.master.notebooks):
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{self.master.notebooks[selected_index].title}'?")
            if confirm:
                self.master.container.delete_notebook(selected_index)

class _TestingApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(APP_NAME)
        self.geometry("800x600")


        notebook_frame = NotebookFrame(self, self)
        notebook_frame.pack(fill="both", expand=True)

# class NotebookModel:
#     def __init__(self, id, owner_id, title, notes):
#         self.id = id
#         self.owner_id = owner_id
#         self.title = title
#         self.notes = notes



if __name__ == "__main__":
    app = _TestingApp()
    app.mainloop()

