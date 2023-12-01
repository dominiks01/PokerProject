from tkinter import ttk
import tkinter as tk
import re

import customtkinter as ctk
import numpy as np


class LobbyView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None
        self.clicked = None

        self.lobby_frame = ctk.CTkFrame(self, width=500, height=500)
        self.lobby_frame.pack(expand=True, pady=40, padx=40, fill="both")

        """
            Configure styles for Treeview
        """
        style = ttk.Style()
        style.configure(
            style="Treeview",
            background="#333333",
            foreground="White",
            fieldbackground="#2b2b2b",
            borderwidth=0.1,
        )

        style.configure(
            style="Treeview.Heading",
            background="#333333",
            foreground="White",
            fieldbackground="#2b2b2b",
            borderwidth=0.1,
            font=(12),
        )

        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        style.theme_use("default")
        style.map(
            "Treeview", background=[("selected", "#333333"), ("active", "#333333")]
        )

        """
            Navbar buttons 
        """
        self.create_lobby_button = ctk.CTkButton(
            self.lobby_frame,
            width=200,
            text="create new lobby",
            command=self.create_lobby,
            height=40,
        )
        self.create_lobby_button.grid(column=0, row=0, pady=(10, 10))

        self.log_out = ctk.CTkButton(
            self.lobby_frame, text="log out", width=200, height=40, command=self.log_out
        )
        self.log_out.grid(column=1, row=0, pady=(10, 10))

        self.show_profile = ctk.CTkButton(
            self.lobby_frame,
            text="go to profile",
            width=200,
            height=40,
            command=self.profile,
        )
        self.show_profile.grid(column=2, row=0, pady=(10, 10))

        self.leaderboard = ctk.CTkButton(
            self.lobby_frame,
            text="show leaderboard",
            width=200,
            height=40,
            command=self.leaderboard,
        )
        self.leaderboard.grid(column=3, row=0, pady=(10, 10))

        """
            Main feature - Treeview representing lobby 
        """
        self.lobby_treeview = ttk.Treeview(
            self.lobby_frame,
            columns=("Author", "Description", "Starting Money", "Players"),
            padding=25,
        )

        self.lobby_treeview.heading(
            column="Author",
            text="Author",
            anchor="center",
            command=lambda _=0: self.sort_by("owner"),
        )

        self.lobby_treeview.heading(
            column="Description",
            text="Description",
            anchor="center",
            command=lambda _=0: self.sort_by("lobby_name"),
        )

        self.lobby_treeview.heading(
            column="Starting Money",
            text="Starting Money",
            anchor="center",
            command=lambda _=0: self.sort_by("starting_money"),
        )

        self.lobby_treeview.heading(
            column="Players",
            text="Players",
            anchor="center",
            command=lambda _=0: self.sort_by("max_players"),
        )

        """
            Treeview columns configuration
        """
        self.lobby_treeview.column(column="#0", width=0, anchor="center")
        self.lobby_treeview.column(column="Author", width=200, anchor="center")
        self.lobby_treeview.column(column="Description", width=250, anchor="center")
        self.lobby_treeview.column(column="Starting Money", width=180, anchor="center")
        self.lobby_treeview.column(column="Players", width=100, anchor="center")
        self.lobby_treeview.bind("<Double-1>", self.join_lobby_)
        self.lobby_treeview.grid(column=0, row=1, columnspan=4)

    def set_controller(self, controller):
        self.controller = controller

    def draw_lobby(self, lst):
        print("LST", lst)
        for item in lst:
            values = (
                item["owner"],
                item["lobby_name"],
                item["starting_money"],
                item["max_players"],
            )

            self.lobby_treeview.insert("", "end", values=values, tags=(item["_id"]))

    def show_error(self, message):
        return

    def sort_by(self, value):
        self.controller.sort_by(value)

    def join_lobby_(self, event):
        item = self.lobby_treeview.identify("region", event.x, event.y)

        if item != "cell":
            return

        item = self.lobby_treeview.selection()[0]
        lobby_index = self.lobby_treeview.item(item, "tags")[0]

        self.controller.join_lobby(lobby_index)

    def create_lobby(self):
        self.controller.create_lobby()

    def log_out(self):
        self.controller.log_out()

    def profile(self):
        self.controller.profile()

    def leaderboard(self):
        self.controller.leaderboard()

    def remove_lobby(self):
        for row in self.lobby_treeview.get_children():
            self.lobby_treeview.delete(row)

    def delete(self):
        self.pack_forget()
        self.grid_forget()
        self.lobby_frame = None
