import customtkinter as ctk
import tkinter as tk

from searchbar import SearchBar
from config import APP_NAME, BACKGROUND_COLOR, FLASHCARDS_ENDPOINT, USERS_ENDPOINT
from user_model import UserModel

import requests
import threading

class FlashcardsUserWindow(ctk.CTkToplevel):
    def __init__(self, master, flashcard_set_title:str = "", callback=None, set_selection = None):
        super().__init__(master)
        self.callback = callback

        self.flashcard_set_title = flashcard_set_title
        self.users: list[UserModel] = []
        self.selected_users: list[int] = [] # List of User IDs
        self.user_vars = []

        self.set_selection = set_selection

        self.get_user_lock = threading.Lock()

        self.fetch_users()
        self.setup_ui()
        self.create_widgets()
        self.layout_widgets()

    def setup_ui(self):

        # .geometry("Width x Height + x-coordinate ng uppermost point ni widget + y-coordinate naman")
        self.geometry(f'250x350+{self.set_selection.winfo_rootx()}+{self.set_selection.winfo_rooty()+self.set_selection.winfo_height()}')
        self.title(self.flashcard_set_title)
        self.configure(fg_color=BACKGROUND_COLOR)
        self.attributes('-topmost', 1)
        self.resizable(False,False)

    def create_widgets(self):
        self.top_frame = ctk.CTkFrame(master=self)
        self.search_bar = SearchBar(self.top_frame, search_handler=self.search_user)

        self.users_frame = ctk.CTkScrollableFrame(master=self)

        self.bot_frame = ctk.CTkFrame(master=self)
        self.send_button = ctk.CTkButton(self.bot_frame, text="Send", command=self.send_button_on_click)

    def layout_widgets(self):
        self.top_frame.configure(fg_color=BACKGROUND_COLOR)
        self.top_frame.pack(side="top")

        self.search_bar.pack(side="left", padx=(10,0), pady=(10,10), fill='x', expand=True)

        self.users_frame.configure(fg_color=BACKGROUND_COLOR)
        self.users_frame.pack(side="top")

        self.send_button.configure(fg_color=BACKGROUND_COLOR, height=35, corner_radius=5)
        self.send_button.pack(side="top", expand=True, fill='x', pady=(10,5), padx=(5,5))

        self.bot_frame.configure(fg_color=BACKGROUND_COLOR)
        self.bot_frame.pack(side="top")
        self.layout_users()

    def fetch_users(self):
        def get_users():
            if not self.get_user_lock.acquire(blocking=False):
                print("Request for Users already in progress. Skipping this request.")
                return

            lock_acquired = True

            try:
                # Fetch Users from API
                response = requests.get(USERS_ENDPOINT + "/all", headers={"Authorization": f"Bearer {self.master.master.controller.access_token}"})
                users = response.json()

                # Convert JSON to UserModel
                self.users = [UserModel.from_json(user) for user in users]
                self.after(0, self.layout_users)
            except ConnectionError as e:
                print(e)
            finally:
                if lock_acquired:
                    self.get_user_lock.release()

        threading.Thread(target=get_users).start()

    def send_button_on_click(self):
        self.selected_users_id: list[int] = []

        # Get Selected Users
        for user_id, checked in self.user_vars.items():
            if checked.get() == 1:
                self.selected_users_id.append(user_id)

        shared_users: list[UserModel] = [user for user in self.users if user.user_id in self.selected_users_id]

        self.callback(shared_users)
        self.destroy()

    def layout_users(self, users: list[UserModel] | None = None):
        self.user_vars = {}

        if not users:
            users = self.users

        # Layout Users
        for user in users:
            user_frame = ctk.CTkFrame(master=self.users_frame)
            user_frame.configure(fg_color=BACKGROUND_COLOR)
            user_frame.pack()

            # Create a unique IntVar for each userd
            user_var = tk.IntVar()
            user_var.set(value=0)  # Initially unchecked

            # GUI ELEMENTS WITH USER_FRAME AS PARENT
            user_check_button = ctk.CTkCheckBox(master=user_frame, text=str(user), variable=user_var, corner_radius=20, checkbox_height=15, checkbox_width=15)
            user_check_button.pack(side="right", padx=(5,0))

            # Store each user_var in the dictionary with the user number as the key
            self.user_vars[user.user_id] = user_var

    def search_user(self, query):
        tk.messagebox.showinfo("Search Box", "Search Box was clicked")

        if self.users == []:
            return

        if not query:
            self.layout_users()
            return

        # <Filter User by Query>
        filtered_users = [user for user in self.users if user.username.lower().find(query.lower()) != -1]

        # Clear User List
        for widget in self.users_frame.winfo_children():
            widget.destroy()

        # Update User List
        self.layout_users(filtered_users)
