import cv2
import mediapipe as mp
import threading
import time
import math
from gestures.camera import CameraSystem
from gestures.gesture_recognizer import GestureRecognizer

class GestureController:
    def __init__(self, screen_width, screen_height, callback, config):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.callback = callback
        self.config = config
        
        # Camera setup
        camera_config = config.get('camera', {})
        self.camera = CameraSystem(
            use_oakd=camera_config.get('use_oakd', False),
            width=camera_config.get('width', 640),
            height=camera_config.get('height', 480)
        )
        
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Gesture recognizer
        self.gesture_recognizer = GestureRecognizer()
        
        # State management
        self.running = False
        self.thread = None
        
        # Cursor state
        self.cursor_x = screen_width // 2
        self.cursor_y = screen_height // 2
        self.prev_index_x = 0
        self.prev_index_y = 0
        
        # Pinch state machine
        self.pinch_state = 'idle'  # idle, pinching, dragging
        self.pinch_threshold = 50  # pixels distance for pinch detection (increased for easier detection)
        self.dragged_widget = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Smoothing
        self.smoothing_factor = config.get('gestures', {}).get('smoothing', 0.5)
        
        # Window bounds (will be set by UI manager)
        self.widget_bounds = {
            'x': 0,
            'y': 0,
            'width': screen_width,
            'height': screen_height
        }
    
    def set_widget_bounds(self, x, y, width, height):
        """Set the bounds of the widget area"""
        self.widget_bounds = {'x': x, 'y': y, 'width': width, 'height': height}
    
    def _is_point_in_bounds(self, x, y):
        """Check if point is within widget bounds"""
        return (self.widget_bounds['x'] <= x <= self.widget_bounds['x'] + self.widget_bounds['width'] and
                self.widget_bounds['y'] <= y <= self.widget_bounds['y'] + self.widget_bounds['height'])
    
    def _calculate_cursor_position(self, index_x, index_y, frame_width, frame_height):
        """Calculate cursor position from hand landmark"""
        # Normalize to 0-1 range
        normalized_x = index_x / frame_width
        normalized_y = index_y / frame_height
        
        # Map to screen coordinates within widget bounds
        screen_x = self.widget_bounds['x'] + (normalized_x * self.widget_bounds['width'])
        screen_y = self.widget_bounds['y'] + (normalized_y * self.widget_bounds['height'])
        
        # Apply smoothing
        self.cursor_x = self.cursor_x * (1 - self.smoothing_factor) + screen_x * self.smoothing_factor
        self.cursor_y = self.cursor_y * (1 - self.smoothing_factor) + screen_y * self.smoothing_factor
        
        # Clamp to bounds - ensure cursor stays within window
        self.cursor_x = max(self.widget_bounds['x'], 
                           min(self.widget_bounds['x'] + self.widget_bounds['width'] - 1, self.cursor_x))
        self.cursor_y = max(self.widget_bounds['y'], 
                           min(self.widget_bounds['y'] + self.widget_bounds['height'] - 1, self.cursor_y))
        
        return self.cursor_x, self.cursor_y
    
    def _detect_pinch(self, landmarks):
        """Detect pinch gesture between thumb and index finger"""
        if len(landmarks) < 21:
            return False, 0
        
        # Get thumb tip (4) and index tip (8)
        thumb = landmarks[4]
        index = landmarks[8]
        
        # Calculate distance
        distance = math.sqrt(
            (thumb.x - index.x) ** 2 + (thumb.y - index.y) ** 2
        )
        
        # Convert to pixel distance (approximate)
        # Assuming frame is ~640x480, distance is normalized 0-1
        pixel_distance = distance * 640  # Approximate
        
        is_pinching = pixel_distance < self.pinch_threshold
        return is_pinching, pixel_distance
    
    def start(self):
        """Start gesture tracking in a separate thread"""
        self.running = True
        self.thread = threading.Thread(target=self._track_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop gesture tracking"""
        self.running = False
        if self.camera:
            self.camera.release()
        if self.thread:
            self.thread.join(timeout=2)
    
    def get_cursor_position(self):
        """Get current cursor position"""
        return {'x': int(self.cursor_x), 'y': int(self.cursor_y)}
    
    def _track_loop(self):
        """Main tracking loop"""
        while self.running:
            frame = self.camera.get_frame()
            if frame is None:
                time.sleep(0.01)
                continue
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Get landmarks as list
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.append([lm.x, lm.y, lm.z])
                    
                    # Get index finger tip (landmark 8)
                    index_tip = hand_landmarks.landmark[8]
                    frame_height, frame_width = frame.shape[:2]
                    
                    # Calculate cursor position
                    cursor_x, cursor_y = self._calculate_cursor_position(
                        index_tip.x * frame_width,
                        index_tip.y * frame_height,
                        frame_width,
                        frame_height
                    )
                    
                    # Check if cursor is in bounds
                    if self._is_point_in_bounds(cursor_x, cursor_y):
                        # Update cursor position
                        self.callback('cursor_move', {'x': int(cursor_x), 'y': int(cursor_y)})
                        
                        # Detect pinch gesture
                        is_pinching, pinch_distance = self._detect_pinch(landmarks)
                        
                        # State machine for pinch
                        if is_pinching and self.pinch_state == 'idle':
                            # Start pinching - more sensitive threshold
                            self.pinch_state = 'pinching'
                            self.drag_start_x = cursor_x
                            self.drag_start_y = cursor_y
                            self.callback('pinch_start', {'x': int(cursor_x), 'y': int(cursor_y)})
                            print(f"✋ Pinch detected at ({int(cursor_x)}, {int(cursor_y)})")  # Debug feedback
                        
                        elif is_pinching and self.pinch_state in ['pinching', 'dragging']:
                            # Continue pinching/dragging
                            if self.pinch_state == 'pinching':
                                # Check if moved enough to start dragging
                                move_distance = math.sqrt(
                                    (cursor_x - self.drag_start_x) ** 2 + 
                                    (cursor_y - self.drag_start_y) ** 2
                                )
                                if move_distance > 10:  # 10 pixel threshold
                                    self.pinch_state = 'dragging'
                                    self.callback('drag_start', {
                                        'x': int(cursor_x),
                                        'y': int(cursor_y),
                                        'start_x': int(self.drag_start_x),
                                        'start_y': int(self.drag_start_y)
                                    })
                            
                            if self.pinch_state == 'dragging':
                                # Update drag position
                                self.callback('drag_move', {
                                    'x': int(cursor_x),
                                    'y': int(cursor_y),
                                    'delta_x': int(cursor_x - self.drag_start_x),
                                    'delta_y': int(cursor_y - self.drag_start_y)
                                })
                        
                        elif not is_pinching and self.pinch_state in ['pinching', 'dragging']:
                            # Release pinch
                            was_dragging = (self.pinch_state == 'dragging')
                            self.pinch_state = 'idle'
                            self.dragged_widget = None
                            
                            if was_dragging:
                                self.callback('drag_end', {'x': int(cursor_x), 'y': int(cursor_y)})
                                print(f"👆 Pinch released after drag")  # Debug feedback
                            else:
                                self.callback('click', {'x': int(cursor_x), 'y': int(cursor_y)})
                                print(f"👆 Pinch released (click)")  # Debug feedback
                    else:
                        # Cursor outside bounds - reset pinch state and don't process gestures
                        if self.pinch_state != 'idle':
                            self.pinch_state = 'idle'
                            self.dragged_widget = None
                            self.callback('drag_end', {'x': int(cursor_x), 'y': int(cursor_y)})  # Release any active drag
                        # Don't update cursor position when outside bounds
            
            time.sleep(0.01)  # ~100 FPS

