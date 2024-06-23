import customtkinter as ctk

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback

        label = ctk.CTkLabel(self, text="Login Page")
        label.pack(pady=10, padx=10)

        # Example widgets (entry, button) for login
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack()

        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack()

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack()
        self.login_button.bind("<Return>", self.login)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def login(self, event=None):  # Added event=None to handle the event argument from bind
        # Implement login logic here
        print(f"Logging in {self.username_entry.get()}...")

        test_data = {"user_id": "1", "username": "JoshuaHM", "access_token": "123456789", "email": "joshuahm.2004@gmail.com"}
        self.callback(test_data)