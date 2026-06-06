from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.draggable_widget import DraggableWidget

class WeatherWidget(DraggableWidget):
    def __init__(self, weather_service, parent=None):
        super().__init__(parent)
        self.weather_service = weather_service
        self.setFixedSize(250, 120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)
        
        # Temperature label
        self.temp_label = QLabel("--°C")
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        font = QFont("Helvetica", 42, QFont.Weight.Bold)
        self.temp_label.setFont(font)
        self.temp_label.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.temp_label)
        
        # Description label
        self.desc_label = QLabel("Loading...")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        font = QFont("Helvetica", 14)
        self.desc_label.setFont(font)
        self.desc_label.setStyleSheet("color: rgba(255, 255, 255, 200); background: transparent;")
        layout.addWidget(self.desc_label)
        
        self.setLayout(layout)
        
        self.update_weather()
    
    def update_weather(self):
        """Update weather display"""
        data = self.weather_service.get_current_weather()
        if data:
            self.temp_label.setText(f"{data['temp']}°C")
            self.desc_label.setText(f"{data['city']} - {data['condition']}")


