from tkinter import ttk
import tkinter as tk
import re

import customtkinter as ctk
import numpy as np


class RoomView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.room_frame = ctk.CTkFrame(self, fg_color="black")
        self.room_frame.pack(expand=True, pady=40, padx=40, fill='both')
        self.controller = None
        self.clicked = None

        style = ttk.Style()
        style.configure("Treeview",
                        background="#333333",
                        foreground="White",
                        fieldbackground="#2b2b2b")

        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground="White",
                        fieldbackground="#2b2b2b")

        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.room_treeview = ttk.Treeview(self.room_frame, columns=("","Player", "Ready"))
        self.room_treeview.heading("#1", text="Index", anchor="center")
        self.room_treeview.heading("Player", text="Player", anchor="center", command= lambda i =0: self.sort_by(i))
        self.room_treeview.heading("Ready", text="Ready", anchor="center", command= lambda i =1: self.sort_by(i))
        self.room_treeview.column("#0", width=0, anchor="center")
        self.room_treeview.column("#1", width=100, anchor="center")
        self.room_treeview.column("Player", width=200, anchor="center")
        self.room_treeview.column("Ready", width=250, anchor="center")

    def set_controller(self, controller):
        self.controller = controller

    def sort_by(self, value):
        self.controller.sort_by(value)

    def draw_room(self):
        for player_index, item in  enumerate(self.controller.get_room()):
            self.room_treeview.insert("", "end", values=(player_index+1, )+item)

        self.room_treeview.pack(expand=True, fill="both")

    def show_error(self, message):
       return
    
    def delete(self):
        self.pack_forget()
        self.grid_forget()
        self.room_frame = None

    