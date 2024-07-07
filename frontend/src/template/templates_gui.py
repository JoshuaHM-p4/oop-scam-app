import customtkinter as ctk
from .templates_model import TemplateModel, HomeworkModel, MathModel, LetterModel, EssayModel
import sys, os
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # frontend/
from config import APP_NAME, BACKGROUND_COLOR

class TemplatesFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
               
        
    def setup_ui(self):
        # Load images
        self.homework_img = ctk.CTkImage(Image.open("assets/images/homework.png"), size=(100, 100))
        self.letter_img = ctk.CTkImage(Image.open("assets/images/letter.png"), size=(100, 100))
        self.essay_img = ctk.CTkImage(Image.open("assets/images/essay.png"), size=(100, 100))
        self.math_img = ctk.CTkImage(Image.open("assets/images/math.png"), size=(100, 100))
        
        self.top_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        
        self.homework_button = ctk.CTkButton(self.top_frame, fg_color="#1C3662", text="Homework", 
                                             corner_radius=20, image=self.homework_img, compound="top",
                                             command=lambda: self.show_frame("HomeworkFrame"))
        
        self.letter_button = ctk.CTkButton(self.top_frame, fg_color="#2B3742", text="Letter", 
                                           corner_radius=20, image=self.letter_img, compound="top",
                                           command=lambda: self.show_frame("LetterFrame"))
        
        self.bottom_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        
        self.essay_button = ctk.CTkButton(self.bottom_frame, fg_color="#2B3742", text="Essay", 
                                          corner_radius=20, image=self.essay_img, compound="top",
                                          command=lambda: self.show_frame("EssayFrame"))
        
        self.math_button = ctk.CTkButton(self.bottom_frame, fg_color="#1C3662", text="Math", 
                                         corner_radius=20, image=self.math_img, compound="top",
                                         command=lambda: self.show_frame("MathFrame"))
        
        self.horizontal_line = ctk.CTkCanvas(self, height=5, bg='#222B36', highlightthickness=0)
        
        self.vertical_line = ctk.CTkCanvas(self, width=5, bg='#222B36', highlightthickness=0)
        self.pack_and_place_widgets()
        
    def pack_and_place_widgets(self):
        # Packing top frame and its buttons
        self.top_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(20,0))
        self.homework_button.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.letter_button.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Packing bottom frame and its buttons
        self.bottom_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(0,20))
        self.essay_button.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.math_button.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Placing horizontal and vertical lines
        self.horizontal_line.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9)
        self.vertical_line.place(relx=0.5, rely=0.5, anchor='center', relheight=0.9)
        
    def pack_forget_frames(self):
        for widget in self.winfo_children():
            widget.pack_forget()
            widget.place_forget()
    
    def pack_first_page(self):
        self.pack_forget_frames()
        self.pack_and_place_widgets()
    
    def show_frame(self, frame_name):
        self.back_button = ctk.CTkButton(self, text="Back", fg_color=BACKGROUND_COLOR, corner_radius=20, command=self.pack_first_page)
        self.pack_forget_frames()
        self.back_button.pack(side="top", anchor="w", padx=2, pady=2)
        if frame_name == "HomeworkFrame":
            self.homework_frame = HomeworkFrame(self)
            self.homework_frame.pack(side="top", fill="both", expand=True, pady=2, padx=2)
        elif frame_name == "LetterFrame":
            self.letter_frame = LetterFrame(self)
            self.letter_frame.pack(side="top", fill="both", expand=True, pady=2, padx=2)
        elif frame_name == "EssayFrame":
            self.essay_frame = EssayFrame(self)
            self.essay_frame.pack(side="top", fill="both", expand=True, pady=2, padx=2)
        elif frame_name == "MathFrame":
            self.math_frame = MathFrame(self)
            self.math_frame.pack(side="top", fill="both", expand=True, pady=2, padx=2)
            
class HomeworkFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.questions = []  # List to store questions
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        
    #     # Entry for question input
    #     self.question_entry = ctk.CTkEntry(self, placeholder_text="Type your question here")
    #     self.question_entry.pack(pady=10)
        
    #     # Button to add question
    #     self.add_question_btn = ctk.CTkButton(self, text="Add Question", command=self.add_question)
    #     self.add_question_btn.pack(pady=10)
        
    #     # Listbox to display questions
    #     self.questions_textbox = ctk.CTkTextbox(self)
    #     self.questions_textbox.pack(fill="both", expand=True, pady=10)
    
    # def add_question(self):
    #     question = self.question_entry.get()
    #     if question:  # Check if the question is not empty
    #         self.questions.append(question)  # Add question to the list
    #         self.questions_textbox.insert(ctk.END, question)  # Display question in the listbox
    #         self.question_entry.delete(0, ctk.END)  # Clear the entry widget

        
class LetterFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        # self.letter = LetterModel()
        
        # self.letter_title = ctk.CTkLabel(self, text="Letter", fg_color="black", font=("Arial", 20, "bold"))
        # self.letter_title.pack(side="top", fill="x", padx=2, pady=2)
        
        # self.letter_entry = ctk.CTkEntry(self, placeholder_text="Enter Letter", fg_color="black")
        # self.letter_entry.pack(side="top", fill="x", padx=2, pady=2)
        
        # self.letter_button = ctk.CTkButton(self, text="Save Letter", fg_color="black", corner_radius=20)
        # self.letter_button.pack(side="top", fill="x", padx=2, pady=2)
        
class EssayFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        # self.essay = EssayModel()
        
        # self.essay_title = ctk.CTkLabel(self, text="Essay", fg_color="black", font=("Arial", 20, "bold"))
        # self.essay_title.pack(side="top", fill="x", expand=True, padx=2, pady=2)
        
        # self.essay_entry = ctk.CTkEntry(self, placeholder_text="Enter Essay", fg_color="black")
        # self.essay_entry.pack(side="top", fill="x", expand=True, padx=2, pady=2)
        
        # self.essay_button = ctk.CTkButton(self, text="Save Essay", fg_color="black", corner_radius=20)
        # self.essay_button.pack(side="top", fill="x", expand=True, padx=2, pady=2)
        
class MathFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        # # self.math = MathModel()
        
        # self.math_title = ctk.CTkLabel(self, text="Math", fg_color="black", font=("Arial", 20, "bold"))
        # self.math_title.pack(side="top", fill="x", expand=True, padx=2, pady=2)
        
        # self.math_entry = ctk.CTkEntry(self, placeholder_text="Enter Math", fg_color="black")
        # self.math_entry.pack(side="top", fill="x", expand=True, padx=2, pady=2)
        
        # self.math_button = ctk.CTkButton(self, text="Save Math", fg_color="black", corner_radius=20)
        # self.math_button.pack(side="top", fill="x", expand=True, padx=2, pady=2)
        


