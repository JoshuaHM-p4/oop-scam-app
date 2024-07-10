import tkinter as tk
import customtkinter as ctk
from .notes_model import NoteModel, NotebookModel

class PageViewer(ctk.CTkToplevel):
    """
    A window that allows the user to view and edit the pages of a notebook.
    """
    def __init__(self, parent, notebook: NotebookModel):
        super().__init__(parent)
        self.title(notebook.title)
        self.geometry("400x300")
        self.configure(fg_color="#141A1F")

        self.notebook = notebook 
        self.pages = notebook.notes
        self.current_page_index = 0

        self.create_widgets()  

    def create_widgets(self): 
        # Add widgets for the page viewer
        self.title_label = ctk.CTkLabel(self, text=self.notebook.title, font=("Arial", 16), text_color="white")
        self.title_label.pack(pady=10)

        self.content_text = ctk.CTkTextbox(self, wrap="word")
        self.content_text.pack(pady=10, expand=True, fill="both")
        self.content_text.insert("1.0", f"Page {self.current_page_index + 1}\n")  # Start with "Page 1"
        self.content_text.focus_set()  # Make the text box editable

        # Add navigation buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.prev_button = ctk.CTkButton(button_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side="left", padx=10)

        self.page_label = ctk.CTkLabel(button_frame, text=f"Page {self.current_page_index + 1} of {len(self.pages)}", text_color="white")
        self.page_label.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(button_frame, text="Next", command=self.next_page)
        self.next_button.pack(side="left", padx=10)

        self.back_button = ctk.CTkButton(button_frame, text="Back", command=self.go_back)
        self.back_button.pack(side="left", padx=10)

    def next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.pages[self.current_page_index] = self.content_text.get("1.0", tk.END)
            self.current_page_index += 1
            self.update_page()

    def prev_page(self):
        if self.current_page_index > 0:
            self.pages[self.current_page_index] = self.content_text.get("1.0", tk.END)
            self.current_page_index -= 1
            self.update_page()

    def update_page(self):
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", self.pages[self.current_page_index])
        self.page_label.configure(text=f"Page {self.current_page_index + 1} of {len(self.pages)}")

    def go_back(self):
        self.pages[self.current_page_index] = self.content_text.get("1.0", tk.END)
        self.destroy()
