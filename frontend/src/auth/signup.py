import customtkinter as ctk

class SignupFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Signup Page")
        label.pack(pady=10, padx=10)

        # Example widgets (entry, button) for signup
        username_entry = ctk.CTkEntry(self)
        username_entry.pack()

        password_entry = ctk.CTkEntry(self, show="*")
        password_entry.pack()

        signup_button = ctk.CTkButton(self, text="Signup", command=self.signup)
        signup_button.pack()

    def signup(self):
        # Implement signup logic here
        print("Signing up...")
        # Example: validate credentials and switch frame
        self.controller.show_frame("NotesFrame")