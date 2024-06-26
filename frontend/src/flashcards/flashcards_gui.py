import customtkinter as ctk
from .flashcards_model import FlashcardModel, FlashcardSetModel
import tkinter as tk
import sys
import os
from PIL import Image

# Add the common directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'searchbar'))) # src/common/searchbar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

from searchbar import SearchBar
from config import APP_NAME, BACKGROUND_COLOR

class FlashcardsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.top_menu = TopMenu(self)
        self.container = Container(self)
        self.configure(fg_color=BACKGROUND_COLOR,
                       corner_radius=10)
        self.grid_configure(padx=10, pady=10)

        

   

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
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
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
            
    
    