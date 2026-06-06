from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from ui.draggable_widget import DraggableWidget

class ClockWidget(DraggableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Time label
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        font = QFont("Helvetica", 48, QFont.Weight.Bold)
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.time_label)
        
        # Date label
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        font = QFont("Helvetica", 18)
        self.date_label.setFont(font)
        self.date_label.setStyleSheet("color: rgba(255, 255, 255, 200); background: transparent;")
        layout.addWidget(self.date_label)
        
        self.setLayout(layout)
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # Update every second
        
        self.update_clock()
    
    def update_clock(self):
        """Update clock display"""
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%A, %B %d, %Y")
        
        self.time_label.setText(time_str)
        self.date_label.setText(date_str)


