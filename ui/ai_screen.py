import tkinter as tk

class AIScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='black')
        self.controller = controller
        
        self.label = tk.Label(self, text="AI Assistant Listening...", font=("Helvetica", 24), fg="white", bg="black")
        self.label.pack(pady=50)

        self.response_text = tk.Text(self, height=10, width=50, font=("Helvetica", 16), fg="white", bg="black", bd=0, wrap="word")
        self.response_text.pack(pady=20, padx=50)
        self.response_text.insert("1.0", "Waiting for input...")

    def update_response(self, text):
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert("1.0", text)
