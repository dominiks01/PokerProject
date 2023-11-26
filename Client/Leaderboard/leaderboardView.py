from tkinter import ttk
import tkinter as tk
import re

import customtkinter as ctk
import numpy as np


class LeaderboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None
       
        self.leaderboard_frame = ctk.CTkFrame(self, width=500, height=500)
        self.leaderboard_frame.pack(expand=True, pady=40, padx=40, fill='both')

    def set_controller(self, controller):
        self.controller = controller

    def draw_view(self, lst):
       pass

    def show_error(self, message):
       pass
    
    def clear_view(self):
        for row in self.lobby_treeview.get_children():
            self.lobby_treeview.delete(row)
    
    def delete(self):
        self.pack_forget()
        self.grid_forget()
        self.lobby_frame = None

    