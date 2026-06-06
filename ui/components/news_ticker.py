import tkinter as tk
from services.news import NewsService

class NewsTicker(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='black')
        self.service = NewsService()
        self.headlines = []
        self.current_index = 0
        
        self.label = tk.Label(self, text="Loading News...", font=("Helvetica", 18), fg="white", bg="black")
        self.label.pack(fill="x", pady=10)
        
        self.fetch_news()
        self.scroll_news()

    def fetch_news(self):
        self.headlines = self.service.get_headlines()
        if not self.headlines:
            self.headlines = ["No news available"]
        self.after(1800000, self.fetch_news) # Update every 30 mins

    def scroll_news(self):
        if self.headlines:
            self.label.config(text=self.headlines[self.current_index])
            self.current_index = (self.current_index + 1) % len(self.headlines)
        
        self.after(10000, self.scroll_news) # Change headline every 10s

    def next_headline(self):
        self.current_index = (self.current_index + 1) % len(self.headlines)
        self.label.config(text=self.headlines[self.current_index])

    def prev_headline(self):
        self.current_index = (self.current_index - 1) % len(self.headlines)
        self.label.config(text=self.headlines[self.current_index])
