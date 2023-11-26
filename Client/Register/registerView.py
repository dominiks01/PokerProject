from tkinter import ttk
import tkinter as tk

import customtkinter as ctk
from requests import post

from GUI.screensEnum import ScreensEnum

URL = "http://127.0.0.1:5000"


class RegisterView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create new frame for register details
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.pack(expand=True, pady=40, padx=40, fill="both")

        self.label = ctk.CTkLabel(
            self.register_frame, text="Signup", font=("Times New Roman", 20, "bold")
        )
        self.label.grid(row=0, column=1, pady=15, padx=25)

        # Username entry
        self.username_entry = ctk.CTkEntry(
            master=self.register_frame,
            font=("Courier New", 15),
            width=250,
            placeholder_text="Username",
        )
        self.username_entry.grid(
            row=1, column=1, sticky=tk.NSEW, padx=25, pady=10, ipady=5
        )

        # Email entry
        self.email_entry = ctk.CTkEntry(
            master=self.register_frame,
            font=("Courier New", 15),
            width=250,
            placeholder_text="Email",
        )
        self.email_entry.grid(
            row=2, column=1, sticky=tk.NSEW, padx=25, pady=10, ipady=5
        )

        # password entry
        self.password_entry = ctk.CTkEntry(
            master=self.register_frame,
            font=("Courier New", 15),
            width=250,
            placeholder_text="Password",
            show="*",
        )
        self.password_entry.grid(
            row=3, column=1, sticky=tk.NSEW, padx=25, pady=10, ipady=5
        )

        # password rentry
        self.password_reentry = ctk.CTkEntry(
            master=self.register_frame,
            font=("Courier New", 15),
            width=250,
            placeholder_text="Confirm Password",
            show="*",
        )
        self.password_reentry.grid(
            row=5, column=1, sticky=tk.NSEW, padx=25, pady=10, ipady=5
        )

        # register button
        self.signup_button = ctk.CTkButton(
            master=self.register_frame,
            text="Signup",
            command=self.register_button_clicked,
            height=40,
        )
        self.signup_button.grid(
            row=7, column=1, columnspan=2, sticky=tk.NSEW, padx=25, pady=10
        )

        # register button
        self.login_button = ctk.CTkLabel(
            master=self.register_frame, text="Already have an account? Login", height=40
        )
        self.login_button.grid(
            row=8, column=1, columnspan=2, sticky=tk.NSEW, padx=25, pady=0
        )
        self.login_button.bind("<Button-1>", lambda e: self.login_button_clicked())

        # message
        self.message_label = ctk.CTkLabel(self.register_frame, text="")
        self.message_label.grid(row=9, column=1, sticky=tk.W + tk.E)
        self.message_label.configure(anchor="center")

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def show_error(self, message):
        self.message_label["text"] = message
        self.message_label["foreground"] = "red"
        self.message_label.after(3000, self.hide_message)
        self.email_entry["foreground"] = "red"

    def register_button_clicked(self):
        if self.controller:
            self.controller.register(
                self.username_entry.get(),
                self.email_entry.get(),
                self.password_entry.get(),
                self.password_reentry.get(),
            )

    def login_button_clicked(self):
        if self.controller:
            self.controller.login()

    def show_success(self, message):
        self.message_label["text"] = message
        self.message_label["foreground"] = "green"
        self.message_label.after(3000, self.hide_message)

        # reset the form
        self.email_entry["foreground"] = "black"
        self.email_var.set("")

    def hide_message(self):
        self.message_label["text"] = ""

    def delete(self):
        self.pack_forget()
        self.grid_forget()
