import customtkinter as ctk
from .flashcards_model import FlashcardModel, FlashcardSetModel
class FlashcardsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller