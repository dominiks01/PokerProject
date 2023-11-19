from tkinter import ttk
import tkinter as tk
import re

import customtkinter as ctk
import numpy as np


class RoomView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.room_frame = ctk.CTkFrame(self, fg_color="#dbdbdb")
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
        
        self.lobby_button = ctk.CTkButton(self.room_frame, text='Go to lobby', command=self.lobby_button_clicked ,height=40)
        self.lobby_button.grid(column=0, row=0, pady=(0,10))
        
        self.change_state = ctk.CTkButton(self.room_frame, text='Change State' ,height=40)
        self.change_state.grid(column=1, row=0, pady=(0,10))

        self.room_treeview = ttk.Treeview(self.room_frame, columns=("","Player", "Ready"))
        self.room_treeview.heading("#1", text="Index", anchor="center")
        self.room_treeview.heading("Player", text="Player", anchor="center", command= lambda i =0: self.sort_by("username"))
        self.room_treeview.heading("Ready", text="Ready", anchor="center", command= lambda i =1: self.sort_by("ready"))
        self.room_treeview.column("#0", width=0, anchor="center")
        self.room_treeview.column("#1", width=100, anchor="center")
        self.room_treeview.column("Player", width=200, anchor="center")
        self.room_treeview.column("Ready", width=250, anchor="center")
        self.room_treeview.grid(column=0, row=1, columnspan=2)


    def set_controller(self, controller):
        self.controller = controller

    def sort_by(self, value):
        self.controller.sort_by(value)
    
    def lobby_button_clicked(self):
        self.controller.join_lobby()

    def draw_room(self, lst):
        for player_index, item in  enumerate(lst):
            values = (item['username'], item['ready'])
            self.room_treeview.insert("", "end", values=(player_index+1, )+values)

    def show_error(self, message):
       return
    
    def delete(self):
        self.pack_forget()
        self.grid_forget()
        self.room_frame = None

    