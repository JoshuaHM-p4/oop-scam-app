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
        self.delete_mode = False

        self.top_menu = TopMenu(self)
        self.container = Container(self)
        
        self.configure(fg_color=BACKGROUND_COLOR,
                       corner_radius=10)
        self.grid_configure(padx=10, pady=10)
    
    def tkraise(self):
        self.container.fetch_notebooks()
        self.container.display_notebooks()
        super().tkraise()
        
    def view_notebook(self, index, notebook):
        
        self.top_menu.pack_forget()
        self.container.pack_forget()
        self.notebook_page = NotebookPage(self, index, notebook)
    
    def back_to_notebooks(self):
        self.notebook_page.pack_forget()
        self.top_menu.pack(fill="x", padx=2, pady=(20,0))
        self.container.pack(fill="both", expand=True, padx=2, pady=2)
        
            
        

class Container(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        self.master = master
        self.current_note_index = 0
        self.setup_ui()
        self.user = self.master.user

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
            
        self.frame_scroll_container = ctk.CTkScrollableFrame(self, fg_color=BACKGROUND_COLOR)
        self.frame_scroll_container.pack(fill="both", expand=True, pady=(0,20))

        
        num_columns = 2  # Number of columns to display notebooks in

        for i, notebook in enumerate(self.master.notebooks):
            row, col = divmod(i, num_columns)

            # Assuming ctk and Image are properly imported and BACKGROUND_COLOR is defined
            ribbon_image = ctk.CTkImage(Image.open("assets/images/note_placeholder.png"), size=(200, 300))
            
            notebook_button = ctk.CTkButton(self.frame_scroll_container, 
                                            image=ribbon_image, 
                                            text=notebook.title,
                                            corner_radius=20,
                                            fg_color=BACKGROUND_COLOR, 
                                            hover_color="#222B36", 
                                            command=lambda i=i: self.view_notebook(i),
                                            compound="top")
            if self.master.delete_mode:
                notebook_button.configure(hover_color="red", command=lambda i=i: self.delete_notebook(i))
            
            notebook_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Configure the grid to have equal weight for all columns
        for col in range(num_columns):
            self.frame_scroll_container.columnconfigure(col, weight=1)
        
        # Ensure all rows have equal weight
        for row in range((len(self.master.notebooks) + num_columns - 1) // num_columns):
            self.frame_scroll_container.rowconfigure(row, weight=1)

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
        print(notebook)
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
        
        self.setup_ui()
        
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.top_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.top_frame.pack(fill="x")
        
        self.back_button = ctk.CTkButton(self.top_frame, text="Back", command= self.master.back_to_notebooks)
        self.back_button.pack(side="left", padx=10, pady=10, expand=True, anchor="w")
        
        self.label_notebook_title = ctk.CTkLabel(self.top_frame, text="Notebook Page", font=("Arial", 20))
        self.label_notebook_title.pack(side="left", padx=10, pady=10, expand=True)
        
        self.save_button = ctk.CTkButton(self.top_frame, text="Save", command= self.save_page)
        self.save_button.pack(side="left", padx=10, pady=10, expand=True, anchor="e")
        
        # Title textbox
        self.title_textbox = ctk.CTkEntry(self, fg_color=BACKGROUND_COLOR, height=1, font=("Arial", 20), placeholder_text="Title:",
                                          border_width=0, corner_radius=0)
        self.title_textbox.pack(fill="x", padx=10, pady=10)
        
        self.title_textbox.insert(0, self.notebook.title)
        
        # Content textbox
        self.content_textbox = ctk.CTkTextbox(self, fg_color="white", height=1, text_color="black", border_width=0, corner_radius=0)
        self.content_textbox.pack(fill="both", expand=True, padx=10)
        self.content_textbox.insert("0.0", "Some example text!\n" * 50)
        
        self.lower_frame = ctk.CTkFrame(self, fg_color="blue", height=20)
        self.lower_frame.pack(fill="x")
        
    def save_page(self):
        pass
        
        

        

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

