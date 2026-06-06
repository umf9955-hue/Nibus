from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen

class DraggableWidget(QWidget):
    """Base class for draggable widgets"""
    
    # Signals
    position_changed = pyqtSignal(int, int)  # x, y
    drag_started = pyqtSignal()
    drag_ended = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
        # Drag state
        self.is_dragging = False
        self.drag_offset = QPoint(0, 0)
        self.original_position = QPoint(0, 0)
        
        # Minimalist styling
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
        """)
    
    def set_position(self, x, y):
        """Set widget position"""
        self.move(x, y)
        self.original_position = QPoint(x, y)
    
    def get_position(self):
        """Get widget position"""
        return self.pos()
    
    def start_drag(self, cursor_x, cursor_y):
        """Start dragging the widget"""
        if not self.is_dragging:
            self.is_dragging = True
            widget_pos = self.pos()
            self.drag_offset = QPoint(cursor_x - widget_pos.x(), cursor_y - widget_pos.y())
            self.drag_started.emit()
    
    def update_drag(self, cursor_x, cursor_y):
        """Update drag position"""
        if self.is_dragging:
            new_x = cursor_x - self.drag_offset.x()
            new_y = cursor_y - self.drag_offset.y()
            
            # Keep within parent bounds
            parent = self.parent()
            if parent:
                max_x = parent.width() - self.width()
                max_y = parent.height() - self.height()
                new_x = max(0, min(new_x, max_x))
                new_y = max(0, min(new_y, max_y))
            
            self.move(new_x, new_y)
            self.position_changed.emit(new_x, new_y)
    
    def end_drag(self):
        """End dragging"""
        if self.is_dragging:
            self.is_dragging = False
            self.drag_ended.emit()
    
    def contains_point(self, x, y):
        """Check if point is within widget bounds"""
        widget_pos = self.pos()
        return (widget_pos.x() <= x <= widget_pos.x() + self.width() and
                widget_pos.y() <= y <= widget_pos.y() + self.height())
    
    def paintEvent(self, event):
        """Custom paint for minimalist look"""
        super().paintEvent(event)
        
        # Optional: Add subtle glow when dragging
        if self.is_dragging:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = QPen(QColor(255, 255, 255, 100), 2)
            painter.setPen(pen)
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 10, 10)


