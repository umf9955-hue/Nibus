"""
Smart Mirror - Version without MediaPipe (for Python 3.13)
Uses OpenCV for basic hand tracking instead
"""

import sys
import json
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from modules.ui_manager import UIManager
from modules.weather_service import WeatherService
from modules.news_service import NewsService
from modules.calendar_service import CalendarService
from modules.ai_assistant import AIAssistant

# Try to import gesture controller, fallback if MediaPipe not available
try:
    from modules.gesture_controller import GestureController
    GESTURE_AVAILABLE = True
except ImportError:
    print("⚠️  MediaPipe not available - gesture control disabled")
    print("   Install Python 3.11/3.12 and MediaPipe for full functionality")
    GESTURE_AVAILABLE = False
    
    # Create a dummy gesture controller
    class DummyGestureController:
        def __init__(self, *args, **kwargs):
            pass
        def start(self):
            pass
        def stop(self):
            pass
        def get_cursor_position(self):
            return None
        def set_widget_bounds(self, *args):
            pass
    
    GestureController = DummyGestureController

class SmartMirror:
    def __init__(self):
        # Load configuration
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("Error: config.json not found!")
            sys.exit(1)
        
        # Create Qt application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Smart Mirror")
        
        # Get screen dimensions
        screen = self.app.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        # Initialize services
        print("Initializing services...")
        self.weather_service = WeatherService(self.config)
        self.news_service = NewsService(self.config)
        self.calendar_service = CalendarService(self.config)
        self.ai_assistant = AIAssistant(self.config)
        
        # Initialize Gesture Controller (if available)
        self.gesture_controller = None
        if GESTURE_AVAILABLE:
            print("Initializing gesture control...")
            try:
                self.gesture_controller = GestureController(
                    self.screen_width,
                    self.screen_height,
                    self.on_gesture_event,
                    self.config
                )
            except Exception as e:
                print(f"⚠️  Gesture controller failed: {e}")
                self.gesture_controller = None
        else:
            print("Gesture control disabled (MediaPipe not available)")
        
        # Initialize UI Manager
        print("Initializing UI...")
        self.ui_manager = UIManager(
            self.screen_width,
            self.screen_height,
            self.weather_service,
            self.news_service,
            self.calendar_service,
            self.ai_assistant,
            self.gesture_controller
        )
        
        # Connect gesture controller to UI manager
        if self.gesture_controller:
            self.ui_manager.set_gesture_controller(self.gesture_controller)
            self.gesture_controller.start()
        else:
            # Hide cursor if no gesture control
            self.ui_manager.cursor.hide_cursor()
        
        # Setup fullscreen
        if self.config.get('app', {}).get('fullscreen', True):
            self.ui_manager.show_fullscreen()
        else:
            self.ui_manager.show()
        
        print("Smart Mirror initialized successfully!")
        if not GESTURE_AVAILABLE:
            print("⚠️  Note: Gesture control is disabled. Install Python 3.11/3.12 and MediaPipe for full functionality.")
        print("Press F11 to toggle fullscreen, ESC to exit")
        print("You can still interact with widgets using mouse/touch")
    
    def on_gesture_event(self, event_type, data):
        """Handle gesture events from the gesture controller"""
        if not self.gesture_controller:
            return
            
        if event_type == 'cursor_move':
            self.ui_manager.update_cursor_position(data['x'], data['y'])
        
        elif event_type == 'pinch_start':
            self.ui_manager.cursor.set_pinching(True)
            self.ui_manager.handle_pinch_start(data['x'], data['y'])
        
        elif event_type == 'drag_start':
            self.ui_manager.handle_drag_start(
                data['x'], data['y'],
                data['start_x'], data['start_y']
            )
        
        elif event_type == 'drag_move':
            self.ui_manager.handle_drag_move(
                data['x'], data['y'],
                data['delta_x'], data['delta_y']
            )
        
        elif event_type == 'drag_end':
            self.ui_manager.cursor.set_pinching(False)
            self.ui_manager.handle_drag_end(data['x'], data['y'])
        
        elif event_type == 'click':
            self.ui_manager.handle_click(data['x'], data['y'])
    
    def run(self):
        """Start the application"""
        try:
            sys.exit(self.app.exec())
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources on exit"""
        if self.gesture_controller:
            self.gesture_controller.stop()
        print("Cleanup complete")

if __name__ == "__main__":
    try:
        print("Starting Smart Mirror...")
        app = SmartMirror()
        print("Application initialized, starting event loop...")
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

