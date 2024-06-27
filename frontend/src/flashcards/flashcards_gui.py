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
        self.back_image = ctk.CTkImage(Image.open("assets/images/back_arrow.png"), size=(30, 30))
        self.back_button = ctk.CTkButton(self, text="", 
                                         command=self.show_first_page,
                                         image=self.back_image,
                                         corner_radius=20,
                                         fg_color=BACKGROUND_COLOR,
                                         hover_color="#2B5EB2",
                                         width=30)
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate")
        
    def show_first_page(self):
        if self.flashcard_set_frame:
            self.flashcard_set_frame.pack_forget()  # Hide the FlashcardSetFrame
        self.top_menu.pack(fill="x", padx=2, pady=(9, 0))  # Reapply padding
        self.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))  # Reapply padding
        self.back_button.pack_forget()
        self.progressbar.pack_forget()  
        
    def show_flashcard_set(self, flashcard_set):
        if self.flashcard_set_frame:
            self.flashcard_set_frame.pack_forget()  # Hide the previous FlashcardSetFrame
        self.back_button.pack(side="top", anchor="nw", padx=5, pady=(10,3))
        self.flashcard_set_frame = FlashcardSetFrame(self, flashcard_set, self.progressbar)  # Create a new FlashcardSetFrame
        self.flashcard_set_frame.pack(fill="both", expand=True, padx=2, pady=2)
        self.top_menu.pack_forget()
        self.container.pack_forget()


class TopMenu(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.hamburger_is_open : bool= False
        self.hamburger_option_is_active : bool= False
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
        # Show menu when hamburger button is clicked
        if self.hamburger_is_open == False:

            # To access the selected value, not the return value
            self.hamburger_menu_var = ctk.StringVar()
            self.hamburger_menu_options = ctk.CTkSegmentedButton(self, 
                                                                 values=["Add Set", "Edit Set","Share Set"], 
                                                                 command=self.hamburger_menu_options_click,
                                                                 variable=self.hamburger_menu_var)
            self.hamburger_menu_options.pack(side="left", padx=(0, 13))
            self.hamburger_is_open = True
        elif self.hamburger_is_open == True:
            self.hamburger_menu_options.pack_forget()
            self.hamburger_is_open = False

    # Selected is the return of the segmented button, automatically returns the value with the command attribute
    def hamburger_menu_options_click(self, selected):
        # Call designated functions for options clicked
        def show_add_set_frame():
            self.master.container.pack_forget()
            self.active_set = AddSetFrame(self.master)

        def show_edit_set_frame():
            self.master.container.pack_forget()
            self.active_set = EditSetFrame(self.master)
        
        def show_share_set_frame():
            self.master.container.pack_forget()
            self.active_set = ShareSetFrame(self.master)

        # To reset the selected value of segmented button
        self.hamburger_menu_var.set("")

        def activate_frame():
            if selected == "Add Set":
                return show_add_set_frame()
            elif selected == "Edit Set":
                return show_edit_set_frame()
            elif selected == "Share Set":
                return show_share_set_frame()

        # If no active frames
        if self.hamburger_option_is_active == False:
            self.hamburger_option_is_active = True
            activate_frame()
            
        # If there is no active frames
        elif self.hamburger_option_is_active == True:
            self.active_set.pack_forget()
            activate_frame()

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
    def __init__(self, master, flashcard_set=None, progressbar=None):
        super().__init__(master)
        self.flashcard_set = flashcard_set
        self.current_index = 0
        self.is_front = True
        self.progressbar = progressbar

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
        
        # Load disabled images
        self.prev_image_disabled = ctk.CTkImage(Image.open("assets/images/left_arrow_disabled.png"), size=(30, 30))
        self.next_image_disabled = ctk.CTkImage(Image.open("assets/images/right_arrow_disabled.png"), size=(30, 30))
        
        self.prev_image = ctk.CTkImage(Image.open("assets/images/left_arrow.png"), size=(30, 30))
        self.prev_button = ctk.CTkButton(self, text="", 
                                            image=self.prev_image, 
                                            command=self.on_previous,
                                            corner_radius=20,
                                            fg_color=BACKGROUND_COLOR,
                                            hover_color="#2B5EB2")
        
        self.prev_button.pack(side='left', padx=(8,5), pady=5)
    
        self.container = ctk.CTkFrame(master=self, corner_radius=10)
        self.container.pack(side='left', fill="both", expand=True, padx=10, pady=5)
        
        self.label = ctk.CTkLabel(master=self.container, text="", font=("Arial", 24))
        self.label.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.next_image = ctk.CTkImage(Image.open("assets/images/right_arrow.png"), size=(30, 30))
        
        self.next_button = ctk.CTkButton(master=self, text="", 
                                         image=self.next_image, 
                                         command=self.on_next,
                                         corner_radius=20,
                                         fg_color=BACKGROUND_COLOR,
                                         hover_color="#2B5EB2")
        
        self.next_button.pack(side='left', padx=(8,5), pady=5)
        
        self.label.bind("<Button-1>", lambda e: self.flip_frame())
        
        self.progressbar.pack(side='bottom', pady=10, fill='x', padx=10)
        
        self.update_flashcard()
        self.update_progressbar()  
    
    def update_flashcard(self):
        front, back = self.flashcards[self.current_index]
        self.label.configure(text=front if self.is_front else back)
        self.container.configure(fg_color=self.front_color if self.is_front else self.back_color)
        
        # Update buttons state
        if self.current_index == 0:
            self.prev_button.configure(state='disabled', image=self.prev_image_disabled)
        else:
            self.prev_button.configure(state='normal', image=self.prev_image)

        # Correctly configure the state and image of next_button
        if self.current_index == len(self.flashcards) - 1:
            self.next_button.configure(state='disabled', image=self.next_image_disabled)
        else:
            self.next_button.configure(state='normal', image=self.next_image)
        
    
    def flip_frame(self):
        self.is_front = not self.is_front
        self.update_flashcard()
    
    def on_next(self):
        if self.current_index < len(self.flashcards) - 1:
            self.current_index += 1
            self.is_front = True
            self.update_flashcard()
            self.update_progressbar()
    
    def on_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.is_front = True
            self.update_flashcard()
            self.update_progressbar()
            
    def update_progressbar(self):
        progress = (self.current_index + 1) / len(self.flashcards)
        self.progressbar.set(progress)


class AddSetFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        self.create_widgets()
        self.layout_widgets()

        # Create new frame
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=(0,3))

        # Create widgets
    def create_widgets(self):
        self.left_frame = ctk.CTkFrame(self)
        self.middle_frame = ctk.CTkFrame(self)
        self.right_frame = ctk.CTkFrame(self)

        self.upper_frame = ctk.CTkFrame(self.middle_frame)

        self.set_name_label = ctk.CTkLabel(self.upper_frame, text="Set Name:")
        self.set_name_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Enter Set Name")
        self.word_label = ctk.CTkLabel(self.upper_frame, text="Word:")
        self.word_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Enter Word")
        self.definition_label = ctk.CTkLabel(self.upper_frame, text="Definition:")
        self.definition_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Enter the definition of the word (Backside)")

        self.lower_frame = ctk.CTkFrame(self.middle_frame)

        self.add_word_button = ctk.CTkButton(self.lower_frame, text="Add Word", command=self.add_word)
        self.save_set_button = ctk.CTkButton(self.lower_frame, text="Save Set", command=self.save_set)
        self.back_button = ctk.CTkButton(self.lower_frame, text="Back", command=self.back_command)

    def layout_widgets(self):
        self.left_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.left_frame.pack(side='left', fill="both", expand=True, padx=2, pady=(0,3))
        self.middle_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.middle_frame.pack(side='left', fill="both", expand=True, padx=2, pady=(0,3))
        self.right_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.right_frame.pack(side='left', fill="both", expand=True, padx=2, pady=(0,3))

        self.upper_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.upper_frame.pack(side='top', fill="x", padx=2, pady=(100,50))

        self.set_name_label.pack()
        self.set_name_entry.configure(width=200, height=35)
        self.set_name_entry.pack()
        self.word_label.pack()
        self.word_entry.configure(width=200, height=35)
        self.word_entry.pack()
        self.definition_label.pack()
        self.definition_entry.configure(width=400, height=40)
        self.definition_entry.pack()

        self.lower_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.lower_frame.pack(side='top', fill="x", padx=2, pady=(0,3))

        self.add_word_button.configure(height=35)
        self.add_word_button.pack(side='left')
        self.back_button.configure(height=35)
        self.back_button.pack(side='right')
        self.save_set_button.configure(height=35)
        self.save_set_button.pack()

    def add_word(self):
        tk.messagebox.showinfo("Add Word Button Response", "Add Word button was clicked")

    def save_set(self):
        tk.messagebox.showinfo("Save Set Button Response", "Save Set button was clicked")

    # Destroys the active frame and layouts the main frame of flashcards
    def back_command(self):
        self.pack_forget()
        self.master.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))
        # To set the value of hamburger_option_is_active to false, accessing through the parent frame
        self.master.top_menu.hamburger_option_is_active = False

class EditSetFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        self.create_widgets()
        self.layout_widgets()

    # Create new frame
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=(0,3))

    # Create combobox and button for selecting and user actions
    def create_widgets(self):
        self.left_frame = ctk.CTkFrame(self)
        self.middle_frame = ctk.CTkFrame(self)
        self.right_frame = ctk.CTkFrame(self)

        self.upper_frame = ctk.CTkFrame(self.middle_frame)

        self.set_selection = ctk.CTkComboBox(self.upper_frame, values=["set 1", "set 2", "set 3"])

        self.lower_frame = ctk.CTkFrame(self.middle_frame)

        self.edit_set_button = ctk.CTkButton(self.lower_frame, text="Edit Set", command=self.edit_set)
        self.delete_set_button = ctk.CTkButton(self.lower_frame, text="Delete Set", command=self.delete_set)
        self.back_button = ctk.CTkButton(self.lower_frame, text="Back", command=self.back_command)

    # placing the widgets
    def layout_widgets(self):
        self.left_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.left_frame.pack(side='left', fill="both", expand=True, padx=2, pady=(0,3))
        self.middle_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.middle_frame.pack(side='left', fill="both", expand=True, padx=2, pady=(0,3))
        self.right_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.right_frame.pack(side='left', fill="both", expand=True, padx=2, pady=(0,3))

        self.upper_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.upper_frame.pack(side='top', fill="x", padx=2, pady=(125,50))

        self.set_selection.configure(width=400, height=31)
        self.set_selection.pack()

        self.lower_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.lower_frame.pack(side='top', fill="x", padx=2, pady=(200,3))

        self.edit_set_button.configure(height=35)
        self.edit_set_button.pack(side='left')
        self.back_button.configure(height=35)
        self.back_button.pack(side='right')
        self.delete_set_button.configure(height=35)
        self.delete_set_button.pack()

    def edit_set(self):
        tk.messagebox.showinfo("Edit Set Button Response", "Edit Set button was clicked")

    def delete_set(self):
        tk.messagebox.showinfo("Delete Set Button Response", "Delete Set button was clicked")

    # Destroys the active frame and layouts the main frame of flashcards
    def back_command(self):
        self.pack_forget()
        self.master.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))
        # To set the value of hamburger_option_is_active to false, accessing through the parent frame
        self.master.top_menu.hamburger_option_is_active = False

class ShareSetFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        self.create_widgets()
        self.layout_widgets()

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=(0,3))

    # Create combobox and button for selecting, sharing, and back actions
    def create_widgets(self):
        self.left_frame = ctk.CTkFrame(self)
        self.middle_frame = ctk.CTkFrame(self)
        self.right_frame = ctk.CTkFrame(self)

        self.upper_frame = ctk.CTkFrame(self.middle_frame)

        self.set_selection = ctk.CTkComboBox(self.upper_frame, values=["set 1", "set 2", "set 3"])

        self.lower_frame = ctk.CTkFrame(self.middle_frame)

        self.share_set_button = ctk.CTkButton(self.lower_frame, text="Share Set", command=self.share_set)
        self.back_button = ctk.CTkButton(self.lower_frame, text="Back", command=self.back_command)

    # Making widgets visible
    def layout_widgets(self):
        self.left_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.left_frame.pack(side='left', fill="both", expand=True, padx=2, pady=(0,3))
        self.middle_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.middle_frame.pack(side='left', fill="both", expand=True, padx=2, pady=(0,3))
        self.right_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.right_frame.pack(side='left', fill="both", expand=True, padx=2, pady=(0,3))

        self.upper_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.upper_frame.pack(side='top', fill="x", padx=2, pady=(125,50))

        self.set_selection.configure(width=400, height=31)
        self.set_selection.pack()

        self.lower_frame.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.lower_frame.pack(side='top', fill="x", padx=2, pady=(200,3))

        self.share_set_button.configure(height=35)
        self.share_set_button.pack(side='left')
        self.back_button.configure(height=35)
        self.back_button.pack(side='right')

    def share_set(self):
        tk.messagebox.showinfo("Share Set Button Response", "Share Set button was clicked")
    
    # Destroys the active frame and layouts the main frame of flashcards
    def back_command(self):
        self.pack_forget()
        self.master.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))
        # To set the value of hamburger_option_is_active to false, accessing through the parent frame
        self.master.top_menu.hamburger_option_is_active = False
