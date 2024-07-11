import customtkinter as ctk
import tkinter as tk
import random

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
        self.master = master
        self.setup_ui()
        self.creating_tabs()
        self.creating_widgets()
        self.layout_widgets()

        self.team_number = 1

        self.create_team_button = CreateTeamButton(self.teams_top_frame)
        for team in range(100):
            self.teams_display = TeamsDisplayButton(self.teams_bottom_frame, team, self.team_number, self.master)
            self.team_number +=1

        self.share_item_button = ShareItemButton(self.shared_top_frame)
        self.share_display_label = ShareDisplayLabel(self.shared_mid_frame)
        for item in range(100):
            self.share_display_frame = ShareDisplayFrame(self.shared_bottom_frame, item)
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR)
        self.pack(fill="both", expand=True, padx=2, pady=(9,0))

    def creating_tabs(self):
        self.teams = self.add("Teams")
        self.shared = self.add("Shared")

    def creating_widgets(self):
        self.teams_top_frame = ctk.CTkFrame(master=self.teams)
        self.teams_bottom_frame = ctk.CTkScrollableFrame(master=self.teams)

        self.shared_top_frame = ctk.CTkFrame(master=self.shared)
        self.shared_mid_frame = ctk.CTkFrame(master=self.shared)
        self.shared_bottom_frame = ctk.CTkScrollableFrame(master=self.shared)

    def layout_widgets(self):
        self.teams_top_frame.configure(fg_color=BACKGROUND_COLOR)
        self.teams_top_frame.pack(fill="x", pady=(10,10))
        self.teams_bottom_frame.configure(fg_color=BACKGROUND_COLOR)
        self.teams_bottom_frame.pack(fill="both", expand=True, padx=(32,1))

        self.shared_top_frame.configure(fg_color=BACKGROUND_COLOR)
        self.shared_top_frame.pack(fill="x", pady=(10,10))
        self.shared_mid_frame.configure(fg_color=BACKGROUND_COLOR)
        self.shared_mid_frame.pack(fill="x", pady=(10,0))
        self.shared_bottom_frame.configure(fg_color=BACKGROUND_COLOR)
        self.shared_bottom_frame.pack(fill="both", expand=True, padx=(32,1))

class CreateTeamButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()

    def setup_ui(self):
        self.configure(text="Create Team", command=self.team_creation_floating_widget, corner_radius=10)
        self.pack(side="left", padx=(42,0))

    def team_creation_floating_widget(self):
        # tk.messagebox.showinfo("Team Creation", "Create Team Button was clicked")
        CreateTeamTopLevel(self)

class ShareItemButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()

    def setup_ui(self):
        self.configure(text="Share Item", command=self.share_item_floating_widget, corner_radius=10)
        self.pack(side="left", padx=(43,0))

    def share_item_floating_widget(self):
        # tk.messagebox.showinfo("Share Item", "Share Item Button was clicked")
        ShareItemTopLevel(self)

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

        self.bot_frame = ctk.CTkScrollableFrame(master=self)
        for user in range(1,100):
            self.user_frame = ctk.CTkFrame(master=self.bot_frame)
            self.user_list = ctk.CTkLabel(master=self.user_frame, text=f"Username {user}")
            self.user_check_button = ctk.CTkCheckBox(master=self.user_frame, text="", corner_radius=20, checkbox_height=15, checkbox_width=15)

            self.user_frame.configure(fg_color=BACKGROUND_COLOR)
            self.user_frame.pack()
            self.user_list.pack(side="left", padx=(0, 10))
            self.user_check_button.pack(side="right", padx=(5,0))       

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
    def __init__(self,master, button_num, team_num, frame_master):
        super().__init__(master)
        self.button_num = button_num
        self.team_num = team_num
        self.row_num = button_num//3
        self.col_num = button_num%3
        self.frame_master = frame_master
        self.colors = ["#f0f8ff", "#faebd7", "#7fffd4", "#007fff", "#f5f5dc", 
                       "#ffe4c4", "#ffebcd", "#deb887", "#5f9ea0", "#7fff00", 
                       "#ff7f50", "#fff8dc", "#6495ed", "#cd5c5c", "#dcdcdc", 
                       "#fffff0", "#c3b091"] 
        self.setup_ui()
        # self.create_widgets() "orange", "yellow", "green", "blue", "violet"
        # self.layout_widgets()

    def setup_ui(self):
        #self.master.master.master.team_number
        self.configure(width=250, height=200, fg_color = random.choice(self.colors), 
                       text=f"Team {self.team_num}", 
                       text_color="black", 
                       font=("Arial", 20), 
                       corner_radius=10, 
                       command=self.on_click)
        self.grid(row=self.row_num, column=self.col_num, padx=(5,20), pady=10, sticky=ctk.NSEW)
    
    # def create_widgets(self):
    #     self.team_name = ctk.CTkLabel(self, )
                       
    # def layout_widgets(self):
    #     self.team_name.pack(fill="both", expand=True)

    def on_click(self):
        collaborationframe = self.frame_master.master
        self.master.master.master.master.master.pack_forget()
        TeamDisplay(self.frame_master, collaborationframe)

class ShareItemTopLevel(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        self.create_widgets()
        self.layout_widgets()

    def setup_ui(self):
        self.geometry(f"250x50+{self.master.winfo_rootx()+ self.master.winfo_width()}+{self.master.winfo_rooty()}")
        self.title("")
        self.configure(fg_color=BACKGROUND_COLOR)
        self.attributes('-topmost', 1)
        self.resizable(False,False)

    def create_widgets(self):
        #, search_handler=self.search_flashcards
        self.search_bar = SearchBar(self)

    def layout_widgets(self):
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(5,5), pady=5)

class ShareDisplayLabel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        self.create_widgets()
        self.layout_widgets()

    def setup_ui(self):
        self.configure(fg_color="#222B36", height=15, corner_radius=10)
        self.pack(fill='x', expand=True, pady=(10,0), padx=(43,17))

    def create_widgets(self):
        self.items_label = ctk.CTkLabel(self, text="▼ Items", font=("Arial", 20))
        self.owner_label = ctk.CTkLabel(self, text="Owner", font=("Arial", 20))
        self.type_label = ctk.CTkLabel(self, text="Type", font=("Arial", 20))

    def layout_widgets(self):
        self.items_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
        self.owner_label.pack(side='left', fill='x', expand=True, pady=5, padx=5)
        self.type_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)

class ShareDisplayFrame(ctk.CTkFrame):
    def __init__(self, master, item_num):
        super().__init__(master)
        self.item_num = item_num + 1
        # items, owner, type
        # self.items = items
        # self.owner = owner
        # self.type  = type
        self.setup_ui()
        self.create_widgets()
        self.layout_widgets()

    def setup_ui(self):
        self.configure(fg_color="#222B36", height=15, corner_radius=10)
        self.pack(fill='x', pady=5, padx=(5,0))

    def create_widgets(self):
        self.items_label = ctk.CTkLabel(self, text=f"Item {self.item_num}", font=("Arial", 20))
        self.owner_label = ctk.CTkLabel(self, text=f"Owner {self.item_num}", font=("Arial", 20))
        self.type_label = ctk.CTkLabel(self, text=f"Type {self.item_num}", font=("Arial", 20))

    def layout_widgets(self):
        self.items_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)
        self.owner_label.pack(side='left', fill='x', expand=True, pady=5, padx=5)
        self.type_label.pack(side="left", fill='x', expand=True, pady=5, padx=5)

class TeamDisplay(ctk.CTkScrollableFrame):
    def __init__(self, master, collab_frame):
        super().__init__(master)
        self.collab_frame = collab_frame
        self.setup_ui()
        self.frame_setup()
        for num in range(1,5):
            self.create_widgets(num)
            self.layout_widgets()

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR)
        self.pack(fill='both', expand=True)

    def frame_setup(self):
        self.back_frame = ctk.CTkFrame(self)
        self.back_button = ctk.CTkButton(self.back_frame, text="❮❮ Back", command=self.back_button)

        self.upper_frame = ctk.CTkFrame(self)
        self.lower_frame = ctk.CTkFrame(self)

        self.back_frame.configure(fg_color = BACKGROUND_COLOR)
        self.back_button.configure(fg_color=BACKGROUND_COLOR, border_color="#222B36", border_width=2, corner_radius=10)

        self.upper_frame.configure(fg_color = BACKGROUND_COLOR, border_color ="#222B36", border_width= 2, corner_radius = 10)
        self.lower_frame.configure(fg_color = BACKGROUND_COLOR, border_color ="#222B36", border_width= 2, corner_radius = 10)

        self.back_frame.pack(fill='both', expand=True, side='top')
        self.back_button.pack(side='left', padx=10, pady=5)

        self.upper_frame.pack(fill='both', expand=True, pady=5, padx=(10,15), side='top')
        self.lower_frame.pack(fill='both', expand=True, padx=(10,15), side='top')

    def create_widgets(self, num):
        self.members_label = ctk.CTkLabel(self.upper_frame, text=f"User {num}")
        self.shared_item = ctk.CTkLabel(self.lower_frame, text=f"Item {num}")

    def layout_widgets(self):
        self.members_label.pack(padx=10, pady=10)
        self.shared_item.pack(padx=10, pady=10)

    def back_button(self):
        self.pack_forget()
        self.collab_frame.module_frames[7].top_frame.pack(fill='both', expand=True)
        
        
        