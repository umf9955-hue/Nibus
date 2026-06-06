import tkinter as tk
from services.weather import WeatherService

class WeatherWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='black')
        self.service = WeatherService()
        
        self.temp_label = tk.Label(self, text="--°C", font=("Helvetica", 48), fg="white", bg="black")
        self.temp_label.pack(anchor="e")
        
        self.desc_label = tk.Label(self, text="Loading...", font=("Helvetica", 18), fg="white", bg="black")
        self.desc_label.pack(anchor="e")
        
        self.update_weather()

    def update_weather(self):
        data = self.service.get_current_weather()
        if data:
            self.temp_label.config(text=f"{data['temp']}°C")
            self.desc_label.config(text=f"{data['city']} - {data['condition']}")
        
        # Update every 10 minutes
        self.after(600000, self.update_weather)
