import tkinter as tk
import time

class ClockWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='black')
        
        self.time_label = tk.Label(self, font=("Helvetica", 64, "bold"), fg="white", bg="black")
        self.time_label.pack(anchor="w")
        
        self.date_label = tk.Label(self, font=("Helvetica", 24), fg="white", bg="black")
        self.date_label.pack(anchor="w")
        
        self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M")
        date_str = time.strftime("%A, %B %d, %Y")
        
        self.time_label.config(text=now)
        self.date_label.config(text=date_str)
        
        self.after(1000, self.update_clock)
