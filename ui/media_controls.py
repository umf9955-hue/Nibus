import tkinter as tk

class MediaControlsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='black')
        self.controller = controller
        
        label = tk.Label(self, text="Media Controls", font=("Helvetica", 30), fg="white", bg="black")
        label.pack(pady=50)

        # Volume Controls
        self.vol_label = tk.Label(self, text="Volume: 50%", font=("Helvetica", 24), fg="white", bg="black")
        self.vol_label.pack(pady=20)
        
        # Placeholder for Spotify/YouTube
        self.status_label = tk.Label(self, text="No Media Playing", font=("Helvetica", 18), fg="gray", bg="black")
        self.status_label.pack(pady=20)

    def set_volume(self, level):
        self.vol_label.config(text=f"Volume: {level}%")
