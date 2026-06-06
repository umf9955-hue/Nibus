import math

class GestureRecognizer:
    def __init__(self):
        self.p_time = 0

    def detect_gesture(self, lm_list):
        """
        Detects gestures based on landmark list.
        Returns: gesture_name (str)
        """
        if not lm_list:
            return None

        # Finger Tips IDs
        # Thumb: 4, Index: 8, Middle: 12, Ring: 16, Pinky: 20
        fingers = []
        
        # Thumb (check if tip is to the right/left of ip joint depending on hand)
        # Simplified: Check x distance for thumb
        if lm_list[4][1] > lm_list[3][1]: # Assuming right hand for simplicity or mirror logic
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(8, 21, 4):
            if lm_list[id][2] < lm_list[id - 2][2]: # Tip is above PIP joint (y is inverted in image coords)
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)

        # Pinch (Index + Thumb close)
        length = math.hypot(lm_list[8][1] - lm_list[4][1], lm_list[8][2] - lm_list[4][2])
        if length < 30:
            return "PINCH"

        # "O" Gesture (Thumb + Index touch, others open)
        # Similar to pinch but other fingers must be UP
        if length < 30 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            return "O_GESTURE"

        # Thumbs Up (Thumb up, others down)
        if fingers[0] == 1 and total_fingers == 1:
             # Check if thumb tip is above other knuckles
             if lm_list[4][2] < lm_list[8][2]:
                 return "THUMBS_UP"
        
        # Thumbs Down (Thumb down, others down)
        if fingers[0] == 0 and total_fingers == 0:
             # Check if thumb tip is below other knuckles
             if lm_list[4][2] > lm_list[5][2]: # Compare to Index MCP
                 return "THUMBS_DOWN"

        # Open Hand / Five Fingers
        if total_fingers == 5:
            # Check for Palm Up/Down for Scroll (requires depth or orientation, simplified here)
            # We can use "Open Hand + Movement" logic in main loop for scroll
            return "OPEN_HAND"
            
        # Peace Sign
        if fingers[1] == 1 and fingers[2] == 1 and total_fingers == 2:
            return "PEACE"
            
        # Pointing (Index only)
        if fingers[1] == 1 and total_fingers == 1:
            return "POINTING"

        return None
