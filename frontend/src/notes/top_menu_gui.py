import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import sys
import os
import json
import threading

# Append paths to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'searchbar')))  # src/common/searchbar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

# Import necessary modules
from config import APP_NAME, BACKGROUND_COLOR, NOTES_ENDPOINT, API_BASE_URL
from searchbar import SearchBar  # Import SearchBar class

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