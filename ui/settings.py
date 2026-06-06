import tkinter as tk

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='black')
        self.controller = controller
        
        label = tk.Label(self, text="Settings", font=("Helvetica", 30), fg="white", bg="black")
        label.pack(pady=50)

        # Placeholder for settings controls
        info = tk.Label(self, text="Gesture Sensitivity: High", font=("Helvetica", 18), fg="gray", bg="black")
        info.pack()
