from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from ui.draggable_widget import DraggableWidget

class NewsWidget(DraggableWidget):
    def __init__(self, news_service, parent=None):
        super().__init__(parent)
        self.news_service = news_service
        self.setFixedSize(400, 80)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        
        self.headlines = []
        self.current_index = 0
        
        # News label
        self.news_label = QLabel("Loading News...")
        self.news_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        font = QFont("Helvetica", 14)
        self.news_label.setFont(font)
        self.news_label.setStyleSheet("color: rgba(255, 255, 255, 200); background: transparent;")
        self.news_label.setWordWrap(True)
        layout.addWidget(self.news_label)
        
        self.setLayout(layout)
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.fetch_news)
        self.update_timer.start(1800000)  # 30 minutes
        
        # Scroll timer
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.scroll_news)
        self.scroll_timer.start(10000)  # 10 seconds
        
        self.fetch_news()
    
    def fetch_news(self):
        """Fetch news headlines"""
        self.headlines = self.news_service.get_headlines()
        if not self.headlines:
            self.headlines = ["No news available"]
        self.current_index = 0
        self.scroll_news()
    
    def scroll_news(self):
        """Scroll to next headline"""
        if self.headlines:
            self.news_label.setText(self.headlines[self.current_index])
            self.current_index = (self.current_index + 1) % len(self.headlines)


