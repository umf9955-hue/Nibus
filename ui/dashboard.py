import tkinter as tk
from ui.components.clock import ClockWidget
from ui.components.weather_widget import WeatherWidget
from ui.components.news_ticker import NewsTicker
from ui.components.calendar_widget import CalendarWidget

class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='black')
        self.controller = controller

        # Grid layout configuration
        self.grid_columnconfigure(0, weight=1) # Left (Clock, Calendar)
        self.grid_columnconfigure(1, weight=2) # Center (Empty/Mirror)
        self.grid_columnconfigure(2, weight=1) # Right (Weather, News)
        self.grid_rowconfigure(0, weight=1)    # Top
        self.grid_rowconfigure(1, weight=1)    # Bottom

        # --- Top Left: Clock ---
        self.clock = ClockWidget(self)
        self.clock.grid(row=0, column=0, sticky="nw", padx=30, pady=30)

        # --- Top Right: Weather ---
        self.weather = WeatherWidget(self)
        self.weather.grid(row=0, column=2, sticky="ne", padx=30, pady=30)

        # --- Bottom Left: Calendar ---
        self.calendar = CalendarWidget(self)
        self.calendar.grid(row=1, column=0, sticky="sw", padx=30, pady=30)

        # --- Bottom: News Ticker ---
        self.news = NewsTicker(self)
        self.news.grid(row=2, column=0, columnspan=3, sticky="ew", padx=0, pady=0)
