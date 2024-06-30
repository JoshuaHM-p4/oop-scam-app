import customtkinter as ctk
from .flashcards_model import FlashcardModel, FlashcardSetModel
import tkinter as tk
import sys
import os
from PIL import Image
import requests


# Add the common directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common', 'searchbar')))  # src/common/searchbar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/

from searchbar import SearchBar
from config import APP_NAME, BACKGROUND_COLOR, FLASHCARDS_ENDPOINT

# FlashcardsFrame: Main frame for the flashcards application
class FlashcardsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.top_menu = TopMenu(self)
        self.container = Container(self, self)
        self.flashcard_set_frame = None
        self.starred_flashcard_sets = []
        self.starred_frame = None
        self.flashcard_sets = []
        
        self.top_menu.active_set = None
    
        self.configure(fg_color="white", corner_radius=10)
        self.grid_configure(padx=10, pady=10)

        # Back button with an image
        self.back_image = ctk.CTkImage(Image.open("assets/images/back_arrow.png"), size=(30, 30))
        
        self.back_button = ctk.CTkButton(self, text="", 
                                         command=self.show_first_page,
                                         image=self.back_image,
                                         corner_radius=20,
                                         fg_color=BACKGROUND_COLOR,
                                         hover_color="#2B5EB2",
                                         width=30)
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate")

    # Method to show the first page with the top menu and container
    def show_first_page(self):
        if self.flashcard_set_frame:
            self.flashcard_set_frame.pack_forget()
        if self.starred_frame:
            self.starred_frame.pack_forget()
        if self.top_menu.active_set:
            self.top_menu.active_set.pack_forget()
        self.top_menu.pack(fill="x", padx=2, pady=(9, 0))
        self.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))
        self.back_button.pack_forget()
        self.progressbar.pack_forget()

    # Method to display a specific flashcard set
    def show_flashcard_set(self, flashcard_set):
        if self.flashcard_set_frame:
            self.flashcard_set_frame.pack_forget()
        if self.starred_frame:
            self.starred_frame.pack_forget()
        self.back_button.pack(side="top", anchor="nw", padx=5, pady=(10, 3))
        self.flashcard_set_frame = FlashcardSetFrame(self, flashcard_set, self.progressbar)
        self.flashcard_set_frame.pack(fill="both", expand=True, padx=2, pady=2)
        self.top_menu.pack_forget()
        self.container.pack_forget()

    # Method to display starred flashcards
    def show_starred_flashcards(self):
        print("Starred Flashcards clicked!")
        if self.flashcard_set_frame:
            self.flashcard_set_frame.pack_forget()
        if self.starred_frame:
            self.starred_frame.pack_forget()
        if self.top_menu.active_set:
            self.top_menu.active_set.pack_forget()
        
        self.starred_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.starred_frame.pack(fill="both", expand=True, padx=2, pady=2)
        self.container.pack_forget()
    
    

# TopMenu: Top menu bar containing search bar and menu buttons
class TopMenu(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.hamburger_is_open : bool= False
        self.hamburger_option_is_active : bool= False
        self.top_menu_star_button_state = False
        self.setup_ui()
    
    # Method to set up UI elements of the top menu
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR)
        self.pack(fill="x", padx=2, pady=(9,0))
        
        # Add the SearchBar to the TopMenu
        self.search_bar = SearchBar(self, search_handler=self.search_flashcards)
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(11,0), pady=5)
    
        self.star_before = ctk.CTkImage(Image.open("assets/images/star_before.png"), size=(23, 23))
        self.star_after = ctk.CTkImage(Image.open("assets/images/star_after.png"), size=(23, 23))
        
        self.star_button = ctk.CTkButton(self, text="", 
                                         image=self.star_before, 
                                         command=self.on_star_click,
                                         width=10, 
                                         height=30, 
                                         corner_radius=10, 
                                         fg_color=BACKGROUND_COLOR, 
                                         bg_color=BACKGROUND_COLOR,
                                         hover=True)
        self.star_button.pack(side="left", padx=5)
        
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

    # Method to handle star button click
    def on_star_click(self):
        if self.top_menu_star_button_state == False:
            self.star_button.configure(image=self.star_after)
            self.top_menu_star_button_state = True
            self.master.show_starred_flashcards()
        elif self.top_menu_star_button_state == True:
            self.star_button.configure(image=self.star_before)
            self.top_menu_star_button_state = False
            if self.active_set:
                self.master.starred_frame.pack_forget()
                self.active_set.pack(fill="both", expand=True, padx=2, pady=(0,3))
            else:
                self.master.show_first_page()
    
    # Method to handle hamburger menu button click
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
        else:
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
            self.star_button.configure(image=self.star_before)
            self.top_menu_star_button_state = False
            if selected == "Add Set":
                if self.master.starred_frame:
                    self.master.starred_frame.pack_forget()
                    
                return show_add_set_frame()
            elif selected == "Edit Set":
                if self.master.starred_frame:
                    self.master.starred_frame.pack_forget()
                    
                return show_edit_set_frame()
            elif selected == "Share Set":
                if self.master.starred_frame:
                    self.master.starred_frame.pack_forget()
                    
                return show_share_set_frame()

        # If no active frames
        if self.hamburger_option_is_active == False:
            activate_frame()
            self.hamburger_option_is_active = True
            
        # If there is no active frames
        elif self.hamburger_option_is_active == True:
            self.active_set.pack_forget()
            activate_frame()

    def on_menu_hover_enter(self, event):
        self.hamburger_menu_button.configure(image=self.hamburger_menu_image_hovered)
        
    # Method to handle hamburger menu button hover leave
    def on_menu_hover_leave(self, event):
        self.hamburger_menu_button.configure(image=self.hamburger_menu_image)
    
    # Method to handle search bar queries
    def search_flashcards(self, query):
        print(f"Searching for: {query}")
        # self.master.controller.search_flashcards(query)

# Container: Scrollable frame to load and display flashcard sets
class Container(ctk.CTkScrollableFrame):
    def __init__(self, master, flashcards_frame, **kwargs):
        super().__init__(master, **kwargs)
        self.flashcards_frame = flashcards_frame  
        self.setup_ui()
    
    # Method to set up UI elements of the container
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=(0,3))
        self.load_flashcard_sets()
        
    # Method to load flashcard sets from the database
    def load_flashcard_sets(self):
        colors = ["red", "green", "blue", "gray14", "purple", "orange", "pink", "light blue", "grey"]
        
        # Create a frame for each flashcard set
        for i in range(1, 5):
            frame_color = colors[i % len(colors)]
            frame = ctk.CTkFrame(self, fg_color=frame_color, height=300, corner_radius=10, border_color=frame_color, border_width=20)
            frame.pack(padx=(0, 5), pady=5, fill="both")
            
            star_image = ctk.CTkImage(Image.open("assets/images/star_white.png"), size=(23, 23))
            star_image_active = ctk.CTkImage(Image.open("assets/images/star_after.png"), size=(23, 23))
            
            star_image_btn = ctk.CTkButton(frame, text="",
                                           image=star_image,
                                           corner_radius=10,
                                           fg_color=frame_color,
                                           width=40, height=40)
            
            star_image_btn.is_active = False
            
            star_image_btn.configure(command=lambda 
                                     btn=star_image_btn, 
                                     star_active=star_image_active, 
                                     star_inactive=star_image, i=i: 
                                     self.toggle_star_image(btn, star_active, star_inactive, i))

            star_image_btn.pack(side='top', padx=2, pady=3, ipadx=0, ipady=0, anchor='ne')
            
            label = ctk.CTkLabel(frame, text=f"Set {i}", text_color="black", font=("Arial", 20))
            label.pack(fill='both', expand=True, padx=5, pady=5)
            
            frame.pack_propagate(False)
            
            label.bind("<Button-1>", lambda event, i=i: self.on_flashcard_set_click(i))

    # Method to handle flashcard set click
    def on_flashcard_set_click(self, set_id):
        print("Flashcard Set", f"Flashcard Set {set_id} clicked!")
        self.flashcards_frame.show_flashcard_set(f"Flashcard Set {set_id}")
        
    # Method to toggle the star image on flashcard sets
    def toggle_star_image(self, btn, star_active, star_inactive, i):
        if btn.is_active:
            btn.configure(image=star_inactive)
            btn.is_active = False
            self.flashcards_frame.starred_flashcard_sets.remove(i)
        else:
            btn.configure(image=star_active)
            btn.is_active = True
            self.flashcards_frame.starred_flashcard_sets.append(i)
        print(f"Star button {i} clicked!")

# class StarredFlashcardsFrame(ctk.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
#         self.pack(fill="both", expand=True, padx=2, pady=2)
#         self.load_starred_flashcards()
        
#     def load_starred_flashcards(self):
#         # Load the starred flashcards from the database
#         pass
        
# FlashcardSetFrame: Frame to display flashcards in a set
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
        
        # Colors for flashcards
        self.front_color = "#2B5EB2"
        self.back_color = "#222B36"
        
        self.setup_ui()
        
    # Method to set up UI elements of the flashcard set frame
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
    
    # Method to update the displayed flashcard
    def update_flashcard(self):
        front, back = self.flashcards[self.current_index]
        self.label.configure(text=front if self.is_front else back)
        self.container.configure(fg_color=self.front_color if self.is_front else self.back_color)
        
        # Update buttons state
        if self.current_index == 0:
            self.prev_button.configure(state='disabled', image=self.prev_image_disabled)
        else:
            self.prev_button.configure(state='normal', image=self.prev_image)

        if self.current_index == len(self.flashcards) - 1:
            self.next_button.configure(state='disabled', image=self.next_image_disabled)
        else:
            self.next_button.configure(state='normal', image=self.next_image)
        
    # Method to flip the flashcard
    def flip_frame(self):
        self.is_front = not self.is_front
        self.update_flashcard()
    
    # Method to go to the next flashcard
    def on_next(self):
        if self.current_index < len(self.flashcards) - 1:
            self.current_index += 1
            self.is_front = True
            self.update_flashcard()
            self.update_progressbar()
    
    # Method to go to the previous flashcard
    def on_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.is_front = True
            self.update_flashcard()
            self.update_progressbar()
            
    # Method to update the progress bar
    def update_progressbar(self):
        progress = (self.current_index + 1) / len(self.flashcards)
        self.progressbar.set(progress)


class AddSetFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.set_name_var = ctk.StringVar()
        self.word_var = ctk.StringVar()
        self.definition_var = ctk.StringVar()
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
        self.set_name_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Enter Set Name", textvariable=self.set_name_var)
        self.word_label = ctk.CTkLabel(self.upper_frame, text="Word:")
        self.word_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Enter Word", textvariable=self.word_var)
        self.definition_label = ctk.CTkLabel(self.upper_frame, text="Definition:")
        self.definition_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Enter the definition of the word (Backside)",textvariable=self.definition_var)

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
        token = self.master.controller.access_token

        set_name = self.set_name_var.get()
        word = self.word_var.get()
        definition = self.definition_var.get()

        if set_name:
            data = {
                "name": set_name,
            }
        else:
            return None
        
        flashcard_data = {
                "word": word,
                "definition": definition
            }

        header = {
            "Authorization": f"Bearer {token}",
        }

        if word and definition:
            if data not in self.master.flashcard_sets:
                response = requests.post(f"{FLASHCARDS_ENDPOINT}/flashcard_sets", json=data, headers=header)
                flashcard_set = FlashcardSetModel.from_json(response.json()["data"])

                self.master.flashcard_sets.append(data)
            
            adding = requests.post(f"{FLASHCARDS_ENDPOINT}/flashcard_sets/{flashcard_set.id}/flashcards", json=flashcard_data, headers=header)

            if response.status_code == 200:
                # <handle dito ng succesful request>
                data = adding.json()
                print(data['msg'])
            else:
                # <handle dito yung bad request>
                pass

        

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