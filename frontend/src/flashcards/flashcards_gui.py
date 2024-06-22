import tkinter as tk
from .flashcards_model import FlashcardsModel, FlashcardSetModel

class FlashcardsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller