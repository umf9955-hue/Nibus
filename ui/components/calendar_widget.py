import tkinter as tk
from services.calendar import CalendarService

class CalendarWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='black')
        self.service = CalendarService()
        
        self.title = tk.Label(self, text="Upcoming Events", font=("Helvetica", 18, "bold"), fg="white", bg="black")
        self.title.pack(anchor="w", pady=(0, 10))
        
        self.events_frame = tk.Frame(self, bg='black')
        self.events_frame.pack(anchor="w")
        
        self.update_events()

    def update_events(self):
        events = self.service.get_events()
        
        # Clear old events
        for widget in self.events_frame.winfo_children():
            widget.destroy()
            
        for event in events:
            e_label = tk.Label(self.events_frame, text=f"• {event['time']} - {event['title']}", font=("Helvetica", 14), fg="white", bg="black")
            e_label.pack(anchor="w")
            
        self.after(600000, self.update_events)
