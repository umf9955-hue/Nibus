import threading
import time
try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False
import speech_recognition as sr
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

class VoiceController:
    def __init__(self, callback, config):
        self.callback = callback
        self.config = config
        self.wake_word = "hey mirror"
        
        # Initialize Porcupine for wake word detection
        self.porcupine = None
        if PORCUPINE_AVAILABLE:
            try:
                # Try to initialize Porcupine (requires access key)
                # For free usage, you can use a custom wake word model
                access_key = config.get('voice', {}).get('porcupine_key', '')
                if access_key and access_key != '':
                    self.porcupine = pvporcupine.create(
                        keywords=['hey mirror'],
                        access_key=access_key
                    )
            except Exception as e:
                print(f"Porcupine initialization failed: {e}")
                print("Voice commands will use continuous listening mode")
        else:
            print("Porcupine not available, using continuous listening mode")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = None
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Microphone initialization failed: {e}")
        
        # Initialize TTS
        self.tts_engine = None
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
            except Exception as e:
                print(f"TTS initialization failed: {e}")
        
        # State
        self.running = False
        self.thread = None
        self.listening = False
    
    def start(self):
        """Start voice command listening"""
        if not self.microphone:
            print("No microphone available, voice commands disabled")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop voice command listening"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.porcupine:
            self.porcupine.delete()
    
    def speak(self, text):
        """Speak text using TTS"""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
    
    def _listen_loop(self):
        """Main listening loop"""
        if self.porcupine:
            self._listen_with_wake_word()
        else:
            self._listen_continuous()
    
    def _listen_with_wake_word(self):
        """Listen with wake word detection using Porcupine"""
        # This requires audio input handling with Porcupine
        # Simplified version - would need proper audio stream handling
        print("Wake word detection active (Porcupine)")
        while self.running:
            time.sleep(0.1)
            # In a real implementation, this would process audio frames
            # and detect the wake word
    
    def _listen_continuous(self):
        """Continuous listening mode (fallback)"""
        print("Voice commands active (continuous mode)")
        print(f"Say '{self.wake_word}' followed by your command")
        
        while self.running:
            try:
                with self.microphone as source:
                    # Listen for audio
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                try:
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"Heard: {text}")
                    
                    # Check for wake word
                    if self.wake_word in text:
                        # Extract command
                        command = text.replace(self.wake_word, "").strip()
                        self._process_command(command)
                    
                except sr.UnknownValueError:
                    # Could not understand audio
                    pass
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                # No speech detected, continue
                pass
            except Exception as e:
                print(f"Voice listening error: {e}")
                time.sleep(1)
    
    def _process_command(self, command):
        """Process voice command"""
        command = command.lower()
        
        # Simple command matching
        if "weather" in command:
            self.callback('voice_command', {'action': 'show_weather'})
        elif "time" in command or "clock" in command:
            self.callback('voice_command', {'action': 'show_clock'})
        elif "calendar" in command or "events" in command:
            self.callback('voice_command', {'action': 'show_calendar'})
        elif "news" in command:
            self.callback('voice_command', {'action': 'show_news'})
        elif "notes" in command:
            self.callback('voice_command', {'action': 'show_notes'})
        elif "help" in command:
            self.speak("Available commands: weather, time, calendar, news, notes")
        else:
            self.callback('voice_command', {'action': 'unknown', 'text': command})

