import json
import os

class ConfigLoader:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = {}
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        else:
            print(f"Config file not found at {self.config_path}")

    def get(self, section, key=None, default=None):
        if key:
            return self.config.get(section, {}).get(key, default)
        return self.config.get(section, default)

# Global instance
_loader = None

def get_config():
    global _loader
    if _loader is None:
        # Assuming config.json is in the root of the smart_mirror package or one level up
        # Adjust path as needed based on execution context
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_path, "config.json")
        _loader = ConfigLoader(config_path)
    return _loader
