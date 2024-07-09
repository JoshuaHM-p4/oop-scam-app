import customtkinter as ctk
from .templates_model import TemplateModel, HomeworkModel, MathModel, LetterModel, EssayModel
import sys, os
from PIL import Image
from CTkListbox import *
import datetime
# import tkinter as tk
from tkinter.filedialog import asksaveasfile



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
        self.back_img = ctk.CTkImage(Image.open("assets/images/back_arrow.png"), size=(30, 30))
        
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
        self.back_button = ctk.CTkButton(self, text="", fg_color=BACKGROUND_COLOR, corner_radius=20, command=self.pack_first_page,
                                         image=self.back_img, width=30)
        self.pack_forget_frames()
        self.back_button.pack(side="top", anchor="w", padx=2, pady=2)
        if frame_name == "HomeworkFrame":
            self.homework_frame = HomeworkFrame(self)
            self.homework_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10)
        elif frame_name == "LetterFrame":
            self.letter_frame = LetterFrame(self)
            self.letter_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10)
        elif frame_name == "EssayFrame":
            self.essay_frame = EssayFrame(self)
            self.essay_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10)
        elif frame_name == "MathFrame":
            self.math_frame = MathFrame(self)
            self.math_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10)
            
class HomeworkFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        
        self.questions = []  # List to store questions
        self.counter = 0
        self.setup_header_questions()
        self.setup_ui()
        
    def header_questions(self):
        self.name_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Enter your name", width=150)
        self.title_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Enter homework title", width=150)
        self.subject_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Enter subject", width=150)
        self.professor_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Enter professor's name", width=150)
        self.instructions_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Enter instructions(Optional)", width=150)
        self.section_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Enter section(Optional)", width=150)
        self.school_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Enter school(Optional)", width=150)
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        
        self.date_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Enter date", width=150)
        
        self.date_entry.insert(0, current_date)
        
    
    def setup_header_questions(self):
        self.home_work_title = ctk.CTkLabel(self, text="Homework", fg_color=BACKGROUND_COLOR, font=("Arial", 20, "bold"))
        self.home_work_title.pack(pady=5, fill="x", padx=10)
        
        self.check_var = ctk.StringVar(value="off")
        
        
        self.header_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=20, border_width=1)
        self.header_frame.pack(fill="x", padx=10, pady=10)
        self.header_questions()
        
        
        self.checkbox = ctk.CTkCheckBox(self.header_frame, text="Apply header?", variable=self.check_var, onvalue="on", offvalue="off",
                                           command=self.pack_header_questions)
        
        self.checkbox.pack(padx=5, pady=10)
        
    def pack_header_questions(self):
        if self.check_var.get() == "on":
            self.name_entry.pack(side="top", padx=10, pady=(3, 0))
            self.title_entry.pack(side="top", padx=10)
            self.subject_entry.pack(side="top", padx=10)
            self.professor_entry.pack(side="top", padx=10,)
            self.instructions_entry.pack(side="top", padx=10)
            self.section_entry.pack(side="top", padx=10)
            self.school_entry.pack(side="top", padx=10)
            self.date_entry.pack(side="top", padx=10, pady=(0,10))
        else:
            self.name_entry.pack_forget()
            self.title_entry.pack_forget()
            self.subject_entry.pack_forget()
            self.professor_entry.pack_forget()
            self.instructions_entry.pack_forget()
            self.section_entry.pack_forget()
            self.school_entry.pack_forget()
            self.date_entry.pack_forget()

    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        
        # Entry for question input
        self.question_entry = ctk.CTkEntry(self, placeholder_text="Type your question here", corner_radius=10, border_width=1)
        self.question_entry.pack(pady=5, fill="x", padx=10)
        
        # Button to add question
        self.add_question_btn = ctk.CTkButton(self, text="Add Question", command=self.add_question)
        self.add_question_btn.pack(pady=5)
        
        self.remove_icon = ctk.CTkImage(Image.open("assets/images/trash.png"), size=(20, 20))
        
        # Listbox to display questions
        self.questions_listbox = CTkListbox(self, corner_radius=10, border_width=1, command=self.enable_remove_button, multiple_selection=True)
        self.questions_listbox.pack(fill="both", expand=True, pady=5, padx=10)
        
        
        
        self.lower_frame_buttons = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.lower_frame_buttons.pack(fill="both", pady=5, padx=10)
        
        self.save_homework_btn = ctk.CTkButton(self.lower_frame_buttons, text="Save Homework", command= self.save_homework, 
                                               corner_radius=10)
        self.save_homework_btn.pack(side="left", pady=5, padx=5,expand=True, anchor='e')
        
        self.remove_question_btn = ctk.CTkButton(self.lower_frame_buttons, text="Remove Question", command=self.remove_question,
                                                 image=self.remove_icon, compound="left",corner_radius=10, state="disabled")
        self.remove_question_btn.pack(side="right", pady=5, anchor='w', expand=True, padx=5)
        
    def enable_remove_button(self,event=None):
        self.remove_question_btn.configure(state="normal")
        
    def remove_question(self):
        selected_indices = self.questions_listbox.curselection()
        selected_indices = list(selected_indices)
        print(selected_indices)
        for i in reversed(selected_indices):  # Iterate in reverse order
            print(i)
            self.questions_listbox.delete(i)
        self.remove_question_btn.configure(state="disabled")
        # for index in selected_indices:
        #     self.questions_listbox.delete(index)
        # if selected_indices:  # Check if there is at least one selected item
        #     selected_index = selected_indices[0]  # Get the first selected item
        #     self.questions_listbox.delete(selected_index)  # Delete the selected item
        # elif selected_indices > 1:
        #     for index in selected_indices:
        #         self.questions_listbox.delete(index)
        

        
        
    # def save(self):
    #     files = [('All Files', '*.*'),  
    #             ('Python Files', '*.py'), 
    #             ('Text Document', '*.txt'),
    #             ('Word Documents', '*.docx')]
    #     self.file = asksaveasfile(filetypes = files, defaultextension = files)


    def add_question(self):
        question = self.question_entry.get()
        if question:  # Check if the question is not empty
            self.questions.append(question)  # Add question to the list
            self.questions_listbox.insert(ctk.END, question)  # Display question in the listbox
            self.question_entry.delete(0, ctk.END)  # Clear the entry widget
            
    def save_homework(self):
        name: str = self.name_entry.get()
        title: str = self.title_entry.get()
        subject: str = self.subject_entry.get()
        professor: str = self.professor_entry.get() 
        instructions: str = self.instructions_entry.get() # optional
        section: str = self.section_entry.get() # optional 
        school: str = self.school_entry.get() # optional 
        date: str = self.date_entry.get() # auto 

        questions: list[str] = self.questions
        
        homework_template = HomeworkModel(
            name = name, 
            title = title,
            date = date,
            subject = subject,
            professor = professor,  
            questions = questions,
            section = section, 
            school = school, 
        )
        homework_template.add_instructions(instructions)
        
        if questions:
            file_path = asksaveasfile(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")]).name
            if file_path:
                homework_template.create_file(file_path)

                # Write header if checkbox is checked
                if self.check_var.get() == "on": 
                    homework_template.write_header(file_path)

                homework_template.write_questions(file_path)

        # homework = HomeworkModel("John Doe", "Example Homework", "July 06, 2024", "Mathematics", ["Question 1", "Question 2", "Question 3"], "Prof. Bill Joe", "Section 1")
        # homework.create_file("homework.docx")
        # homework.write_header("homework.docx")
        # homework.add_instructions("Answer the following questions:")
        # homework.write_questions("homework.docx")


            
            
            
        
class LetterFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):
        # self.letter = LetterModel()

        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)
        
        self.letter_title = ctk.CTkLabel(self, text="Letter", fg_color=BACKGROUND_COLOR, font=("Arial", 20, "bold"))
        self.letter_title.pack(pady=5, fill="x", padx=10)
        
        self.recipient_entry = ctk.CTkEntry(self, placeholder_text="Recipient's Name", width=50)
        self.recipient_entry.pack(pady=5, padx=10)
        
        self.address_entry = ctk.CTkEntry(self, placeholder_text="Address",width=50)
        self.address_entry.pack(pady=5)
        
        self.save_button = ctk.CTkButton(self, text="Save Letter", fg_color="black", corner_radius=20)
        self.save_button.pack(pady=5)
        
class EssayFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)

        self.essay_title = ctk.CTkLabel(self, text="Essay", fg_color=BACKGROUND_COLOR, font=("Arial", 20, "bold"))
        self.essay_title.pack(pady=5, fill="x", padx=10)
        
        self.essay_entry = ctk.CTkEntry(self, placeholder_text="Enter Essay Title")
        self.essay_entry.pack(pady=5, fill="x", padx=10)
        
class MathFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(fg_color=BACKGROUND_COLOR, corner_radius=10)

        self.math_title = ctk.CTkLabel(self, text="Math", fg_color=BACKGROUND_COLOR, font=("Arial", 20, "bold"))
        self.math_title.pack(pady=5, fill="x", padx=10)
        
        self.math_entry = ctk.CTkEntry(self, placeholder_text="Enter Math Problem")
        self.math_entry.pack(pady=5, fill="x", padx=10)
        
        self.add_math_btn = ctk.CTkButton(self, text="Add Math Problem", fg_color="black", corner_radius=20, command=lambda: self.add_math())
        self.add_math_btn.pack(pady=5)
        
        self.math_listbox = CTkListbox(self)
        self.math_listbox.pack(fill="both", expand=True, pady=5, padx=10)
        
        self.save_homework_btn = ctk.CTkButton(self, text="Save Homework", command=lambda: self.save_math())
        self.save_homework_btn.pack(pady=5)
        
    def add_math(self):
        math_problem = self.math_entry.get()
        if math_problem:
            self.math_listbox.insert(ctk.END, math_problem)
            self.math_entry.delete(0, ctk.END)
            
    def save_math(self):
        pass
        
        


