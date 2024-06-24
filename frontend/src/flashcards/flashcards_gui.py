import customtkinter as ctk
from .flashcards_model import FlashcardModel, FlashcardSetModel
import tkinter as tk
import sys
import os

# Add the common directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'searchbar')))

from searchbar import SearchBar

class FlashcardsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.searchbar = SearchBar(self, search_handler=self.search_flashcards)
    def search_flashcards(self, query):
        tk.messagebox.showinfo("Search", f"Searching for: {query}")