import customtkinter as ctk
import tkinter as tk

from searchbar import SearchBar
from config import APP_NAME, BACKGROUND_COLOR, FLASHCARDS_ENDPOINT

class CollaborationFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.top_frame = TabOption(self)

        self.configure(fg_color="white", corner_radius=10)
        self.grid_configure(padx=10, pady=10)

class TabOption(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        self.creating_tabs()
        self.creating_widgets()
        self.layout_widgets()

        self.team_number = 1

        self.create_team_button = CreateTeamButton(self.teams_top_frame)
        for team in range(5):
            self.teams_display = TeamsDisplayButton(self.teams_bottom_frame)
            self.team_number +=1
        self.share_item_button = ShareItemButton(self.shared_top_frame)
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR)
        self.pack(fill="both", expand=True, padx=2, pady=(9,0))

    def creating_tabs(self):
        self.add("Teams")
        self.add("Shared")

    def creating_widgets(self):
        self.teams_top_frame = ctk.CTkFrame(self.tab("Teams"))
        self.teams_bottom_frame = ctk.CTkFrame(self.tab("Teams"))

        self.shared_top_frame = ctk.CTkFrame(self.tab("Shared"))
        self.shared_bottom_frame = ctk.CTkFrame(self.tab("Shared"))

    def layout_widgets(self):
        self.teams_top_frame.configure(fg_color=BACKGROUND_COLOR)
        self.teams_top_frame.pack(fill="x")
        self.teams_bottom_frame.configure(fg_color=BACKGROUND_COLOR)
        self.teams_bottom_frame.pack(fill="both", expand=True)

        self.shared_top_frame.configure(fg_color=BACKGROUND_COLOR)
        self.shared_top_frame.pack(fill="x")
        self.shared_bottom_frame.configure(fg_color=BACKGROUND_COLOR)
        self.shared_bottom_frame.pack(fill="both", expand=True)

class CreateTeamButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()

    def setup_ui(self):
        self.configure(text="Create Team", command=self.team_creation_floating_widget)
        self.pack(side="left", padx=(20,0))

    def team_creation_floating_widget(self):
        # tk.messagebox.showinfo("Team Creation", "Create Team Button was clicked")
        CreateTeamTopLevel(self)
        

class ShareItemButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()

    def setup_ui(self):
        self.configure(text="Share Item", command=self.share_item_floating_widget)
        self.pack(side="left", padx=(20,0))

    def share_item_floating_widget(self):
        tk.messagebox.showinfo("Share Item", "Share Item Button was clicked")

class CreateTeamTopLevel(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        self.create_widgets()
        self.layout_widgets()

    def setup_ui(self):
        self.geometry(f"250x300+{self.master.winfo_rootx()+ self.master.winfo_width()}+{self.master.winfo_rooty()}")
        self.title("")
        self.configure(fg_color=BACKGROUND_COLOR)
        self.attributes('-topmost', 1)
        self.resizable(False,False)

    def create_widgets(self):
        self.top_frame  = ctk.CTkFrame(master=self)
        self.team_name_entry = ctk.CTkEntry(master=self.top_frame, placeholder_text="Team Name")
        self.create_button = ctk.CTkButton(master=self.top_frame, text="Create")
        
        self.mid_frame = ctk.CTkFrame(master=self)
        self.search_bar = SearchBar(self.mid_frame, search_handler=self.search_flashcards)

        self.bot_frame = ctk.CTkFrame(master=self)
        for user in range(1,5):
            self.user_frame = ctk.CTkFrame(master=self.bot_frame)
            self.user_list = ctk.CTkLabel(master=self.user_frame, text=f"Username {user}")
            self.user_radio_button = ctk.CTkRadioButton(master=self.user_frame, text="")

            self.user_frame.configure(fg_color=BACKGROUND_COLOR)
            self.user_frame.pack()
            self.user_list.pack(side="left", padx=(0, 5))
            self.user_radio_button.pack(side="right", padx=(5,0))       

    def layout_widgets(self):
        self.top_frame.configure(fg_color=BACKGROUND_COLOR)
        self.top_frame.pack(side="top")
        self.team_name_entry.configure(width=175)
        self.team_name_entry.pack(pady=(5,0), padx=(5,3), side="left")
        self.create_button.configure(fg_color=BACKGROUND_COLOR)
        self.create_button.pack(side="right", padx=(0,5), pady=(5,0))

        self.mid_frame.configure(fg_color=BACKGROUND_COLOR)
        self.mid_frame.pack(side="top")
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(5,5), pady=5)

        self.bot_frame.configure(fg_color=BACKGROUND_COLOR)
        self.bot_frame.pack(side="top")

    def search_flashcards(self):
        tk.messagebox.showinfo("Search Box", "Search Box was clicked")

class TeamsDisplayButton(ctk.CTkButton):
    def __init__(self,master):
        super().__init__(master)
        self.setup_ui()
        # self.create_widgets()
        # self.layout_widgets()

    def setup_ui(self):
        self.configure(width=250, height=200, fg_color = "red", text=f"Team {self.master.master.master.team_number}")
        self.pack(side="left", padx=5, pady=5)

    # def create_widgets(self):
    #     self.team_name = ctk.CTkLabel(self, )

    # def layout_widgets(self):
    #     self.team_name.pack(fill="both", expand=True)