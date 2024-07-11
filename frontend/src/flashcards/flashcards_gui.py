import customtkinter as ctk
from .flashcards_model import FlashcardModel, FlashcardSetModel
import tkinter as tk
import sys
import os
from PIL import Image
import requests
import threading
import queue

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

        # Main Flashcards List Session
        self.flashcard_sets: list[FlashcardSetModel] = []
        self.flashcard_set_frame = None

        # Main Flashcard Set Session
        self.current_flashcard_set: FlashcardSetModel = None

        # Threading
        self.request_lock = threading.Lock()

        self.starred_flashcard_sets = []
        self.reference = {}
        self.starred_frame = None
        self.top_menu.active_set = None

        self.changes_in_starred = False

        self.container = Container(self)
        self.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.grid_configure(padx=10, pady=10)

        # Back button for the flashcard set frame
        self.back_image = ctk.CTkImage(Image.open("assets/images/back_arrow.png"), size=(30, 30))

        self.back_button = ctk.CTkButton(self, text="",
                                         command=self.show_first_page,
                                         image=self.back_image,
                                         corner_radius=20,
                                         fg_color=BACKGROUND_COLOR,
                                         hover_color="#2B5EB2",
                                         width=30)
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate")

    def update_flashcard_sets(self):
        self.container.display_flashcard_sets(self.flashcard_sets)

    def filter_flashcard_sets(self, query: str):
        filtered_set = [flashcard_set for flashcard_set in self.flashcard_sets if query.lower() in flashcard_set.name.lower()]
        self.container.display_flashcard_sets(filtered_set)

    def fetch_flashcard_sets(self, query: str = None):
        self.flashcard_sets = []
        query = query

        def get_request():
            if not self.request_lock.acquire(blocking=False):
                print("Request for Fetching Flashcards Already in Progress. Skipping this request.")
                return
            lock_acquired = True
            try:
                token = self.controller.access_token
                header = {"Authorization": f"Bearer {token}"}

                endpoint = f"{FLASHCARDS_ENDPOINT}/flashcard_sets" + (f"?query={query}" if query else "")
                response = requests.get(endpoint, headers=header)

                response_data = response.json()

                for data in response_data:
                    flashcard_set = FlashcardSetModel(id = data["id"], name = data["name"])
                    flashcard_set.flashcards = self.fetch_flashcards(data["id"])
                    self.flashcard_sets.append(flashcard_set)
                self.after(0, self.update_flashcard_sets)
            except ConnectionError:
                tk.messagebox.showerror("Connection Error", "Could not connect to server")
            finally:
                if lock_acquired:
                    self.request_lock.release()

        threading.Thread(target=get_request).start()

    def fetch_flashcards(self, set_id:int) -> list[FlashcardModel]:
        flashcards = []
        token = self.controller.access_token
        header = {"Authorization": f"Bearer {token}"}

        response = requests.get(f"{FLASHCARDS_ENDPOINT}/flashcard_sets/{set_id}/flashcards", headers=header)

        response_data = response.json()

        for data in response_data:
            flashcard = FlashcardModel(id = data["id"], set_id = set_id, word = data["word"], definition = data["definition"])
            flashcards.append(flashcard)
        return flashcards

    def tkraise(self, aboveThis=None):
        self.fetch_flashcard_sets()
        super().tkraise(aboveThis)

    # Method to show the first page with the top menu and container
    def show_first_page(self):
        if self.flashcard_set_frame:
            # Hide the flashcard set frame
            self.flashcard_set_frame.pack_forget()
        if self.starred_frame:
            # Hide the starred frame
            self.starred_frame.pack_forget()
        if self.top_menu.active_set:
            # Hide the active set(Add, Edit, Share) frame
            self.top_menu.active_set.pack_forget()

        # Show the top menu and container
        self.top_menu.pack(fill="x", padx=2, pady=(9, 0))
        if self.changes_in_starred:
            self.container.display_flashcard_sets(self.flashcard_sets)
            self.changes_in_starred = False
        if self.top_menu.top_menu_star_button_state:
            self.starred_frame.pack(fill="both", expand=True, padx=2, pady=2)
        else:
            self.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))

        # Hide the back button and progress bar
        self.back_button.pack_forget()
        self.progressbar.pack_forget()

    # Method to display a specific flashcard set
    def show_flashcard_set(self, set_id):

        flashcard_set = next((set for set in self.flashcard_sets if set.id == set_id), None)

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

        self.container.pack_forget()


        self.starred_frame = StarredFlashcardsFrame(self)

        self.starred_frame.pack(fill="both", expand=True, padx=2, pady=2)



# TopMenu: Top menu bar containing search bar and menu buttons
class TopMenu(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.hamburger_is_open : bool= False
        self.hamburger_option_is_active : bool= False
        self.top_menu_star_button_state = False
        self.hamburger_menu_active = "normal"

        self.active_set = None
        self.last_active_set = None
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
            self.last_active_set = self.active_set

            self.master.show_starred_flashcards()

        elif self.top_menu_star_button_state == True:
            self.star_button.configure(image=self.star_before)
            self.top_menu_star_button_state = False

            if self.last_active_set:
                self.master.starred_frame.pack_forget()
                self.last_active_set.pack(fill="both", expand=True, padx=2, pady=(0,3))
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
            self.hamburger_menu_options.configure(state=self.hamburger_menu_active)
            self.hamburger_menu_options.pack(side="left", padx=(0, 13))
            self.hamburger_is_open = True
        else:
            self.hamburger_menu_options.pack_forget()
            self.hamburger_is_open = False


    # Selected is the return of the segmented button, automatically returns the value with the command attribute
    def hamburger_menu_options_click(self, selected):
        # Call designated functions for options clicked
        def show_add_set_frame():

            if self.active_set:
                self.active_set.pack_forget()
            self.master.container.pack_forget()
            self.active_set = AddSetFrame(self.master)



        def show_edit_set_frame():
            if self.active_set:
                self.active_set.pack_forget()
            self.master.container.pack_forget()
            self.active_set = EditSetFrame(self.master)


        def show_share_set_frame():
            if self.active_set:
                self.active_set.pack_forget()
            self.master.container.pack_forget()
            self.active_set = ShareSetFrame(self.master)

        # To reset the selected value of segmented button
        self.hamburger_menu_var.set("")

        def activate_frame():
            self.star_button.configure(image=self.star_before)
            self.top_menu_star_button_state = False
            if self.master.starred_frame:
                self.master.starred_frame.pack_forget()

            # Mapping of selections to their respective functions
            action_map = {
                "Add Set": show_add_set_frame,
                "Edit Set": show_edit_set_frame,
                "Share Set": show_share_set_frame
            }

            # Execute the function based on the selected action
            if selected in action_map:
                return action_map[selected]()

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
        if query.strip() != '':
            self.master.filter_flashcard_sets(query.strip())
        else:
            self.master.update_flashcard_sets()

# Container: Scrollable frame to load and display flashcard sets
class Container(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=(0,3))

    # Method to display flashcard sets from the Flashcard Sets API
    def display_flashcard_sets(self, flashcard_sets):
        colors = ["red", "green", "blue", "gray14", "purple", "orange", "pink", "light blue", "grey"]
        for widget in self.winfo_children():
            widget.destroy()

        # Load star images
        star_image = ctk.CTkImage(Image.open("assets/images/star_white.png"), size=(23, 23))
        star_image_active = ctk.CTkImage(Image.open("assets/images/star_after.png"), size=(23, 23))

        # Database connection to fetch flashcard sets
        for flashcard_set in flashcard_sets:

            print(f"Loading Flashcard Set {flashcard_set.id}: {flashcard_set.name}")
            frame_color = colors[flashcard_set.id % len(colors)]
            frame = ctk.CTkFrame(self, fg_color=frame_color, height=300, corner_radius=10, border_color=frame_color, border_width=20)
            frame.pack(padx=(0, 5), pady=5, fill="both")

            # Check if the flashcard set is starred
            if flashcard_set.starred:
                star_image_btn = ctk.CTkButton(frame, text="",
                                            image=star_image_active,
                                           corner_radius=10,
                                           fg_color=frame_color,
                                           width=40, height=40)
                star_image_btn.is_active = True
            else:
                star_image_btn = ctk.CTkButton(frame, text="",
                                            image=star_image,
                                           corner_radius=10,
                                           fg_color=frame_color,
                                           width=40, height=40)
                star_image_btn.is_active = False

            label = ctk.CTkLabel(frame, text=flashcard_set.name, text_color="black", font=("Arial", 20))

            star_image_btn.configure(command=lambda
                                     btn=star_image_btn,
                                     star_active=star_image_active,
                                     star_inactive=star_image,
                                     i=flashcard_set.id,
                                     name = flashcard_set.name,
                                     fs=flashcard_set: self.toggle_star_image(btn, star_active, star_inactive, fs.id, name))

            star_image_btn.pack(side='top', padx=2, pady=3, ipadx=0, ipady=0, anchor='ne')

            label.pack(fill='both', expand=True, padx=5, pady=5)

            frame.pack_propagate(False)

            label.bind("<Button-1>", lambda event, i=flashcard_set.id, name=flashcard_set.name, fs=flashcard_set: self.master.show_flashcard_set(fs.id))

    # Method to toggle the star image on flashcard sets
    def toggle_star_image(self, btn, star_active, star_inactive, i, name):
        if btn.is_active:
            btn.configure(image=star_inactive)
            btn.is_active = False

            print(f"Removed Set {i}:{name} from starred sets")
            # self.flashcard_sets[name] = 0
            # < starred backend >

        else:
            btn.configure(image=star_active)
            btn.is_active = True

            print(f"Added Set {i}:{name} to starred sets")
            # self.flashcard_sets[name] = 1
            # < starred backend >

class StarredFlashcardsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.display_starred_flashcards()

    def display_starred_flashcards(self):
        if any(i == 1 for i in self.flashcard_sets.values()):
            # Destroy existing widgets before creating new ones
            for widget in self.winfo_children():
                widget.destroy()

            self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=10)
            self.scrollable_frame.pack(fill="both", expand=True)

            # Load images once, outside the loop
            star_image = ctk.CTkImage(Image.open("assets/images/star_white.png"), size=(23, 23))
            star_image_active = ctk.CTkImage(Image.open("assets/images/star_after.png"), size=(23, 23))

            colors = ["red", "green", "blue", "gray14", "purple", "orange", "pink", "light blue", "grey"]
            if self.flashcard_sets:
                for index, name in enumerate(self.flashcard_sets, start=1):
                    if self.flashcard_sets[name] == 1:
                        frame_color = colors[index % len(colors)]
                        frame = ctk.CTkFrame(self.scrollable_frame, fg_color=frame_color, height=300, corner_radius=10, border_color=frame_color, border_width=20)
                        frame.pack(padx=(0, 5), pady=5, fill="both")

                        star_image_btn = ctk.CTkButton(frame, text="",
                                                       image=star_image_active,
                                                       corner_radius=10,
                                                       fg_color=frame_color,
                                                       width=40, height=40)
                        star_image_btn.is_active = True

                        # Use default arguments in lambda to capture current loop variables
                        star_image_btn.configure(command=lambda btn=star_image_btn, star_active=star_image_active, star_inactive=star_image, i=index, name=name: self.toggle_star_image(flashcards, btn, star_active, star_inactive, i, name))

                        star_image_btn.pack(side='top', padx=2, pady=3, ipadx=0, ipady=0, anchor='ne')

                        label = ctk.CTkLabel(frame, text=name, text_color="black", font=("Arial", 20))
                        label.pack(fill='both', expand=True, padx=5, pady=5)

                        frame.pack_propagate(False)

                        label.bind("<Button-1>", lambda event, i=index, name=name: self.master.container.on_flashcard_set_click(i, name))
        else:
            # Ensure previous widgets are cleared before displaying the message
            for widget in self.winfo_children():
                widget.destroy()

            label = ctk.CTkLabel(self, text="No Starred Flashcards", font=("Arial", 24))
            label.pack(fill="both", expand=True, padx=5, pady=5)

    def toggle_star_image(self, flashcards, btn, star_active, star_inactive, i, name):
        if btn.is_active:
            btn.configure(image=star_inactive)
            btn.is_active = False
            self.master.flashcard_sets[name] = 0
            tk.messagebox.showinfo("Starred Flashcards", f"Removed Set {i}:{name} from starred sets")
            self.master.changes_in_starred = True

        # Reload the starred flashcards to update the display
        self.display_starred_flashcards()



# FlashcardSetFrame: Frame to display flashcards in a set
class FlashcardSetFrame(ctk.CTkFrame):
    def __init__(self, master, flashcard_set: FlashcardSetModel, progressbar=None):
        super().__init__(master)
        self.master = master
        self.current_index = 0
        self.is_front = True
        self.progressbar = progressbar

        self.flashcards = flashcard_set.flashcards

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
        # FlashcardModel(id = data["id"], set_id = set_id, word = data["word"], definition = data["definition"])
        current_flashcard = self.flashcards[self.current_index] # TO FIX: handle empty flashcards

        self.label.configure(text=current_flashcard.word if self.is_front else current_flashcard.definition)
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

        self.request_lock = threading.Lock()
        self.condition = threading.Condition()

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

        ## Flashcard Set ##
        header = {
            "Authorization": f"Bearer {token}",
        }

        if not set_name or not word or not definition:
            # < handle word and definition entry missing >
            return None

        # Search Set in self.master.flashcard_sets by set_name
        flashcard_set = next((set for set in self.master.flashcard_sets if set.name == set_name), None)

        # Create a new set if set_name is not found
        if not flashcard_set:
            def post_flashcard_set():
                if not self.request_lock.acquire(blocking=False):
                    print("Request for Sending Flashcard Set Already in Progress. Skipping this request.")
                    return

                lock_acquired = True
                try:
                    set_data = {
                        "name": set_name,
                    }
                    response = requests.post(f"{FLASHCARDS_ENDPOINT}/flashcard_sets", json=set_data, headers=header)
                    data = response.json()['data']

                    flashcard_set = FlashcardSetModel(id=data["id"], name=data["name"])
                    self.master.flashcard_sets.append(flashcard_set)

                    with self.condition:
                        self.condition.notify_all()  # Notify that the set has been created

                    self.after(0, self.master.update_flashcard_sets)
                except ConnectionError:
                    tk.messagebox.showerror("Connection Error", "Could not connect to server")
                finally:
                    if lock_acquired:
                        self.request_lock.release()

            threading.Thread(target=post_flashcard_set).start()

        ## Flashcard ##
        def post_flashcard():
            if not self.request_lock.acquire(blocking=False):
                print("Request for Sending Flashcard Already in Progress. Skipping this request.")
                return

            lock_acquired = True
            try:
                with self.condition:
                    if not flashcard_set:
                        self.condition.wait()  # Wait until the set is created

                flashcard_data = {
                    "word": word,
                    "definition": definition
                }

                flashcard_response = requests.post(f"{FLASHCARDS_ENDPOINT}/flashcard_sets/{flashcard_set.id}/flashcards", json=flashcard_data, headers=header)

                if flashcard_response.status_code == 400:
                    print(flashcard_response["error"])

                flashcard_data_api = flashcard_response.json()
                flashcard_set.flashcards.append(FlashcardModel(id=flashcard_data_api["id"], set_id=flashcard_set.id, word=flashcard_data_api["word"], definition=flashcard_data_api["definition"]))

            except ConnectionError:
                tk.messagebox.showerror("Connection Error", "Could not connect to server")
            finally:
                if lock_acquired:
                    self.request_lock.release()

        threading.Thread(target=post_flashcard).start()

        self.word_var.set("")
        self.definition_var.set("")

    def save_set(self):
        tk.messagebox.showinfo("Save Set Button Response", "Save Set button was clicked")
        token = self.master.controller.access_token
        set_name = self.set_name_var.get()

        if not set_name:
            return None

        flashcard_set = next((set for set in self.master.flashcard_sets if set.name == set_name), None)

        if not flashcard_set:
            return None


        def post_request():
            if not self.request_lock.acquire(blocking=False):
                print("Request for Already in Progress. Skipping this request.")
                return

            lock_acquired = True
            try:

                set_data = {
                    "name": set_name,
                }

                header = {
                    "Authorization": f"Bearer {token}",
                }

                response = requests.post(f"{FLASHCARDS_ENDPOINT}/flashcard_sets", json=set_data, headers=header)
                data = response.json()
                flashcard_set = FlashcardSetModel(id = data["id"], name = data["name"])

                self.master.flashcard_sets.append(flashcard_set)

                if response.status_code == 200:
                    # <handle dito ng succesful request>
                    data = response.json()
                    print(data['msg'])
                else:
                    # <handle dito yung bad request>
                    pass
            except ConnectionError:
                tk.messagebox.showerror("Connection Error", "Could not connect to server")
            finally:
                if lock_acquired:
                    self.request_lock.release()

        threading.Thread(target=post_request).start()

        self.set_name_var.set("")
        self.word_var.set("")
        self.definition_var.set("")

    # Destroys the active frame and layouts the main frame of flashcards
    def back_command(self):
        self.pack_forget()
        self.master.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))
        # To set the value of hamburger_option_is_active to false, accessing through the parent frame
        self.master.top_menu.hamburger_option_is_active = False
        self.back_to_container = True
        self.master.top_menu.active_set = None


class EditSetFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.delete_lock = threading.Lock()

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

        sets = [flashcard.name for flashcard in self.master.flashcard_sets]
        self.set_selection = ctk.CTkComboBox(self.upper_frame, values=sets)

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
        tk.messagebox.showinfo("Edit Set Details Button Response", "Edit Set Details button was clicked")
        self.master.top_menu.hamburger_menu_options.configure(state='disabled')
        self.master.top_menu.hamburger_menu_active = 'disabled'
        self.pack_forget()
        EditSetDetailsFrame(self.master)

    def delete_set(self):
        tk.messagebox.showinfo("Delete Set Button Response", "Delete Set button was clicked")

        token = self.master.controller.access_token
        set_name = self.set_selection.get()

        if not set_name:
            return None

        flashcard_set = next((set for set in self.master.flashcard_sets if set.name == set_name), None)

        if not flashcard_set:
            return None

        def delete_request():
            if not self.delete_lock.acquire(blocking=False):
                print("Request for Deleting Set Already in Progress. Skipping this request.")
                return

            lock_acquired = True
            try:
                header = {
                    "Authorization": f"Bearer {token}",
                }

                response = requests.delete(f"{FLASHCARDS_ENDPOINT}/flashcard_sets/{flashcard_set.id}", headers=header)
                data = response.json()

                # Delete Flashcard Set from
                flashcard_sets = [set for set in self.master.flashcard_sets if set.name != set_name]
                self.master.flashcard_sets = flashcard_sets
                self.set_selection.set("")
                self.set_selection.configure(values=[flashcard.name for flashcard in self.master.flashcard_sets])

                if response.status_code == 200:
                    # <handle dito ng succesful request>
                    data = response.json()
                    print(data['msg'])
                else:
                    # <handle dito yung bad request>
                    pass
            except ConnectionError:
                tk.messagebox.showerror("Connection Error", "Could not connect to server")
            finally:
                if lock_acquired:
                    self.delete_lock.release()

        threading.Thread(target=delete_request).start()

        self.set_selection.set("")

        return None

    # Destroys the active frame and layouts the main frame of flashcards
    def back_command(self):
        self.pack_forget()
        self.master.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))
        # To set the value of hamburger_option_is_active to false, accessing through the parent frame
        self.master.top_menu.hamburger_option_is_active = False
        self.master.top_menu.active_set = None


class ShareSetFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
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

        self.set_selection = ctk.CTkComboBox(self.upper_frame, values=self.master.flashcard_sets)

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

        token = self.master.controller.access_token
        set_name = self.set_selection.get()

    # Destroys the active frame and layouts the main frame of flashcards
    def back_command(self):
        self.pack_forget()
        self.master.container.pack(fill="both", expand=True, padx=2, pady=(0, 3))
        # To set the value of hamburger_option_is_active to false, accessing through the parent frame
        self.master.top_menu.hamburger_option_is_active = False
        self.master.top_menu.active_set = None

class EditSetDetailsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.edited_set_name_var = ctk.StringVar()
        self.edited_word_var = ctk.StringVar()
        self.edited_definition_var = ctk.StringVar()

        self.current_flashcard_set: FlashcardSetModel = None
        self.current_flashcard: FlashcardModel = None

        self.flashcard_set_lock = threading.Lock()
        self.flashcard_lock = threading.Lock()
        self.condition = threading.Condition()

        self.setup_ui()
        self.create_widgets()
        self.layout_widgets()

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        self.pack(fill="both", expand=True, padx=2, pady=(0,3))

    def create_widgets(self):
        self.left_frame = ctk.CTkFrame(self)
        self.middle_frame = ctk.CTkFrame(self)
        self.right_frame = ctk.CTkFrame(self)

        self.upper_frame = ctk.CTkFrame(self.middle_frame)

        # Get Sets for Set Selection Combobox
        sets = [flashcard_set.name for flashcard_set in self.master.flashcard_sets]
        self.set_selection = ctk.CTkComboBox(self.upper_frame, values=sets, command=self.on_set_selection_change)

        self.get_current_set()

        # Get Flashcards for Word Selection Combobox
        flashcard_words = [flashcard.word for flashcard in self.current_flashcard_set.flashcards]
        self.word_selection = ctk.CTkComboBox(self.upper_frame, values=flashcard_words, command=self.on_word_selection_change)

        self.get_current_flashcard()
        self.show_unedited_set_details()

        # Edited Set Details
        self.set_name_label = ctk.CTkLabel(self.upper_frame, text="Set Name:")
        self.set_name_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Edit Set Name", textvariable=self.edited_set_name_var)
        self.word_label = ctk.CTkLabel(self.upper_frame, text="Word:")
        self.word_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Edit Word", textvariable=self.edited_word_var)
        self.definition_label = ctk.CTkLabel(self.upper_frame, text="Definition:")
        self.definition_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Edit the definition of the word (Backside)",textvariable=self.edited_definition_var)

        self.lower_frame = ctk.CTkFrame(self.middle_frame)

        self.edit_flashcard_button = ctk.CTkButton(self.lower_frame, text="Apply Edits", command=self.edit_flashcard)
        self.back_button = ctk.CTkButton(self.lower_frame, text="Back", command=self.back_command)

    def get_current_set(self):
        # Get Selected Combobox Flashcard Set
        self.current_flashcard_set = next((set for set in self.master.flashcard_sets if set.name == self.set_selection.get()), None)
        return self.current_flashcard_set

    def get_current_flashcard(self):
        self.current_flashcard = next((flashcard for flashcard in self.current_flashcard_set.flashcards if flashcard.word == self.word_selection.get()), None)
        return self.current_flashcard

    def show_unedited_set_details(self): # Original Set Details before editing
        self.edited_set_name_var.set(self.current_flashcard_set.name)
        self.edited_word_var.set(self.current_flashcard.word)
        self.edited_definition_var.set(self.current_flashcard.definition)

    def get_edited_set_details(self):
        set, word, definition = self.edited_set_name_var.get(), self.edited_word_var.get(), self.edited_definition_var.get()
        return set, word, definition

    def on_set_selection_change(self, event):
        # Get Flashcards for Word Selection Combobox
        self.get_current_set()

        # Update Word Selection Combobox
        flashcard_words = [flashcard.word for flashcard in self.current_flashcard_set.flashcards]
        self.word_selection.configure(values=flashcard_words)
        self.word_selection.set(flashcard_words[0]) # Set the first word as default for update

        # Get Current Flashcard by Word and Show Unedited Set Details into Entry Fields
        self.get_current_flashcard()
        self.show_unedited_set_details()

    def on_word_selection_change(self, event):
        self.get_current_flashcard()
        self.show_unedited_set_details()

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
        self.word_selection.configure(width=400, height=31)
        self.word_selection.pack(pady=(15,0))

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
        self.lower_frame.pack(side='top', fill="x", padx=2, pady=(200,3))

        self.edit_flashcard_button.configure(height=35)
        self.edit_flashcard_button.pack(side='left')
        self.back_button.configure(height=35)
        self.back_button.pack(side='right')

    def edit_flashcard(self):
        # tk.messagebox.showinfo("Edit Flashcard Button Response", "Edit Flashcard button was clicked")

        self.get_current_set()
        self.get_current_flashcard()
        edited_set_name, edited_word, edited_definition = self.get_edited_set_details()

        # print(f"Current: {self.current_flashcard_set.name} - Edited: {edited_set_name}")
        # print(f"Current: {self.current_flashcard.word} - Edited: {edited_word}")
        # print(f"Current: {self.current_flashcard.definition} - Edited: {edited_definition}")

        token = self.master.controller.access_token
        header = {
            "Authorization": f"Bearer {token}",
        }

        # UPDATE FLASHCARD SET
        if edited_set_name != self.current_flashcard_set.name:
            def patch_flashcard_set():
                if not self.flashcard_set_lock.acquire(blocking=False):
                    print("Request for Flashcard Set Already in Progress. Skipping this request.")
                    return

                lock_acquired = True

                try:

                    edited_data = {
                        "name": edited_set_name,
                    }
                    response = requests.patch(f"{FLASHCARDS_ENDPOINT}/flashcard_sets/{self.current_flashcard_set.id}", json=edited_data, headers=header)
                    data = response.json()["data"]
                    message = response.json()["msg"]

                    for flashcard_set in self.master.flashcard_sets:
                        if flashcard_set.name == self.current_flashcard_set.name:
                            flashcard_set.name = edited_set_name

                    sets = [flashcard_set.name for flashcard_set in self.master.flashcard_sets]
                    self.set_selection.configure(values=sets)
                    self.set_selection.set(edited_set_name)
                    self.get_current_set() # self.current_flashcard_set = edited FlashcardSetModel
                    self.master.update_flashcard_sets()

                    with self.condition:
                        self.condition.notify_all()  # Notify that the set has been created

                except ConnectionError:
                    tk.messagebox.showerror("Connection Error", "Could not connect to server")
                finally:
                    if lock_acquired:
                        self.flashcard_set_lock.release()

            threading.Thread(target=patch_flashcard_set).start()

        # UPDATE WORD OR DEFINITION
        if edited_word != self.current_flashcard.word or edited_definition != self.current_flashcard.definition:
            def patch_flashcard():
                if not self.flashcard_lock.acquire(blocking=False):
                    print("Request for Flashcard Already in Progress. Skipping this request.")
                    return

                lock_acquired = True

                try:
                    edited_data = {}

                    if edited_word != self.current_flashcard.word:
                        edited_data["word"] = edited_word
                    if edited_definition != self.current_flashcard.definition:
                        edited_data["definition"] = edited_definition

                    response = requests.patch(f"{FLASHCARDS_ENDPOINT}/flashcard_sets/{self.current_flashcard_set.id}/flashcards/{self.current_flashcard.id}", json=edited_data, headers=header)
                    data = response.json()["data"]
                    message = response.json()["msg"]

                    for flashcard in self.current_flashcard_set.flashcards:
                        if flashcard.word == self.current_flashcard.word:
                            flashcard.word = edited_word
                            flashcard.definition = edited_definition

                    flashcard_words = [flashcard.word for flashcard in self.current_flashcard_set.flashcards]
                    self.word_selection.configure(values=flashcard_words)
                    self.word_selection.set(edited_word)
                    self.get_current_flashcard()
                    self.show_unedited_set_details()
                except ConnectionError:
                    tk.messagebox.showerror("Connection Error", "Could not connect to server")
                finally:
                    if lock_acquired:
                        self.flashcard_lock.release()

            threading.Thread(target=patch_flashcard).start()

        return None


    # Destroys the active frame and edit set flashcards frame
    def back_command(self):
        self.pack_forget()
        self.master.top_menu.active_set = EditSetFrame(self.master)
        self.master.top_menu.hamburger_menu_options.configure(state='normal')
        self.master.top_menu.hamburger_menu_active = 'normal'


