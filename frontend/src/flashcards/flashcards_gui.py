import customtkinter as ctk
from .flashcards_model import FlashcardModel, FlashcardSetModel
import tkinter as tk
import sys
import os
from PIL import Image

# Add the common directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'searchbar')))  # src/common/searchbar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

from searchbar import SearchBar
from config import APP_NAME, BACKGROUND_COLOR

class FlashcardsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.top_menu = TopMenu(self)
        self.container = Container(self, self)  # Pass self to Container
        self.flashcard_set_frame = None  # Initialize with None
        self.configure(fg_color=BACKGROUND_COLOR,
                       corner_radius=10)
        self.grid_configure(padx=10, pady=10)
        self.back_button = ctk.CTkButton(self, text="Back", command=self.show_menu_and_container)
        
    def show_menu_and_container(self):
        if self.flashcard_set_frame:
            self.flashcard_set_frame.pack_forget()  # Hide the FlashcardSetFrame
        self.top_menu.pack(fill="x", padx=2, pady=(9, 0))  # Reapply padding
        self.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))  # Reapply padding
        self.back_button.pack_forget()
        
    def show_flashcard_set(self, flashcard_set):
        if self.flashcard_set_frame:
            self.flashcard_set_frame.pack_forget()  # Hide the previous FlashcardSetFrame
        self.back_button.pack(side="top", anchor="nw", padx=13, pady=(10,5))
        self.flashcard_set_frame = FlashcardSetFrame(self, flashcard_set)
        self.flashcard_set_frame.pack(fill="both", expand=True, padx=2, pady=2)
        self.top_menu.pack_forget()
        self.container.pack_forget()


class TopMenu(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.hamburger_is_open : bool= False
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR)
        self.pack(fill="x", padx=2, pady=(9,0))
        # Add the SearchBar to the TopMenu
        self.search_bar = SearchBar(self, search_handler=self.search_flashcards)
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(11,0), pady=5)
    
        self.ribbon_image = ctk.CTkImage(Image.open("assets/images/ribbon.png"), size=(23, 23))
        self.ribbon_image_zoomed = ctk.CTkImage(Image.open("assets/images/ribbon.png"), size=(30, 30))
        self.bookmark_button = ctk.CTkButton(self, text="", 
                                             image=self.ribbon_image, 
                                             command=self.on_bookmark_click,
                                             width=10, 
                                             height=30, 
                                             corner_radius=10, 
                                             fg_color=BACKGROUND_COLOR, 
                                             bg_color=BACKGROUND_COLOR,
                                             hover=True,
                                             )
        self.bookmark_button.pack(side="left", padx=5)
        
        self.hamburger_menu_image = ctk.CTkImage(Image.open("assets/images/hamburger_before.png"), size=(23, 23))
        self.hamburger_menu_image_hovered = ctk.CTkImage(Image.open("assets/images/hamburger_after.png"), size=(23, 23))
        
        self.hamburger_menu_button = ctk.CTkButton(self, text="", 
                                                   image=self.hamburger_menu_image, 
                                                   command=self.on_menu_click,
                                                    width=30, 
                                                    height=30, 
                                                    corner_radius=10, 
                                                    fg_color=BACKGROUND_COLOR, 
                                                    bg_color=BACKGROUND_COLOR,
                                                    hover=True)
        self.hamburger_menu_button.pack(side="left", padx=(0,5))
        self.hamburger_menu_button.bind("<Enter>", self.on_menu_hover_enter)
        self.hamburger_menu_button.bind("<Leave>", self.on_menu_hover_leave)
        
    def on_bookmark_click(self):
        # Create a new Toplevel window
        tk.messagebox.showinfo("Bookmark", "Bookmark button clicked!")
        
    def on_bookmark_hover_enter(self, event):
        # Change the button image to the zoomed version on hover
        self.bookmark_button.configure(image=self.ribbon_image_hovered)

    def on_bookmark_hover_leave(self, event):
        # Revert the button image to the original size when not hovered
        self.bookmark_button.configure(image=self.ribbon_image)  # Ensure self.ribbon_image is the original sized image
    
    def on_menu_click(self):
        #tk.messagebox.showinfo("Menu", "Hamburger menu clicked!")

        if self.hamburger_is_open == False:
            self.hamburger_menu_options = ctk.CTkSegmentedButton(self, 
                                                                 values=["Add Set", "Select Set","Share Set"], 
                                                                 command=self.hamburger_menu_options_click)
            self.hamburger_menu_options.pack(side="left", padx=(0, 13))
            self.hamburger_is_open = True
        elif self.hamburger_is_open == True:
            self.hamburger_menu_options.pack_forget()
            self.hamburger_is_open = False
            

    def hamburger_menu_options_click(self, event):
        print(f"{event} was clicked")
        
    def on_menu_hover_enter(self, event):
        # Change the button image to the zoomed version on hover
        self.hamburger_menu_button.configure(image=self.hamburger_menu_image_hovered)
        
    def on_menu_hover_leave(self, event):
        # Revert the button image to the original size when not hovered
        self.hamburger_menu_button.configure(image=self.hamburger_menu_image) 
    
    def search_flashcards(self, query):
        print(f"Searching for: {query}")
        # self.master.controller.search_flashcards(query)
        
class Container(ctk.CTkScrollableFrame):
    def __init__(self, master, flashcards_frame, **kwargs):  # Accept flashcards_frame
        super().__init__(master, **kwargs)
        self.flashcards_frame = flashcards_frame  # Store the reference
        self.setup_ui()
    
    def setup_ui(self):
        # Assuming fg_color is meant to be a property of the Container class or passed via kwargs
        # If fg_color is intended to be a global or passed variable, ensure it's defined or passed correctly
     # Default to 'white' if fg_color not in kwargs
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=(0,3))
        self.load_flashcard_sets()
        
    # Load flashcard sets from the database
    def load_flashcard_sets(self):
        colors = ["red", "green", "blue", "gray14", "purple", "orange", "pink", "light blue", "grey"]
        
        # Frame for each flashcard set
        for i in range(1, 5):
            frame_color = colors[i % len(colors)]
            frame = ctk.CTkFrame(self, fg_color=frame_color, height=300, corner_radius=10, border_color=frame_color, border_width=20)
            frame.pack(padx=(0, 5), pady=5, fill="both")
            
            label = ctk.CTkLabel(frame, text=f"Set {i}", text_color="black", font=("Arial", 20))
            label.pack(fill='both', expand=True, padx=5, pady=5)
            frame.pack_propagate(False)
            
            label.bind("<Button-1>", lambda event, i=i: self.on_flashcard_set_click(i))
        
    def on_flashcard_set_click(self, set_id):
        print("Flashcard Set", f"Flashcard Set {set_id} clicked!")
        self.flashcards_frame.show_flashcard_set(f"Flashcard Set {set_id}")
        
class FlashcardSetFrame(ctk.CTkFrame):
    def __init__(self, master, flashcard_set=None):
        super().__init__(master)
        self.flashcard_set = flashcard_set
        self.current_index = 0
        self.is_front = True

        # Dummy flashcards
        self.flashcards = [
            ("Front 1", "Back 1"),
            ("Front 2", "Back 2"),
            ("Front 3", "Back 3"),
            ("Front 4", "Back 4"),
            ("Front 5", "Back 5"),
            ("Front 6", "Back 6"),
            ("Front 7", "Back 7"),
            ("Front 8", "Back 8"),
            ("Front 9", "Back 9"),
            ("Front 10", "Back 10")
        ]
        
        # Single set of colors
        self.front_color = "#2B5EB2"
        self.back_color = "#222B36"
        
        self.setup_ui()
        
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.container = ctk.CTkFrame(master=self)
        self.container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.label = ctk.CTkLabel(master=self.container, text="", font=("Arial", 24))
        self.label.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.label.bind("<Button-1>", lambda e: self.flip_frame())
        
        self.setup_buttons()
        
    def setup_buttons(self):
        self.frame_buttons = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.frame_buttons.pack(side="top", fill="x", padx=2, pady=(0,2))
        
        self.prev_button = ctk.CTkButton(master=self.frame_buttons, text="Previous", command=self.on_previous)
        self.prev_button.pack(side='left', fill="x", expand=True, padx=(8,5), pady=5)
        
        self.next_button = ctk.CTkButton(master=self.frame_buttons, text="Next", command=self.on_next)
        self.next_button.pack(side='left', fill="x", expand=True, padx=(8,5), pady=5)
        
        self.update_flashcard()
    
    def update_flashcard(self):
        front, back = self.flashcards[self.current_index]
        self.label.configure(text=front if self.is_front else back)
        self.container.configure(fg_color=self.front_color if self.is_front else self.back_color)
    
    def flip_frame(self):
        self.is_front = not self.is_front
        self.update_flashcard()
    
    def on_next(self):
        if self.current_index < len(self.flashcards) - 1:
            self.current_index += 1
            self.is_front = True
            self.update_flashcard()
    
    def on_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.is_front = True
            self.update_flashcard()
