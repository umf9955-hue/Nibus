try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIAssistant:
    def __init__(self, config):
        self.config = config
        self.api_key = config.get('ai', {}).get('api_key', '')
        self.model = config.get('ai', {}).get('model', 'gpt-3.5-turbo')
        self.client = None
        
        if not OPENAI_AVAILABLE:
            print("⚠️  OpenAI not available - AI Assistant disabled")
            return
        
        if self.api_key and self.api_key != 'YOUR_OPENAI_API_KEY':
            try:
                openai.api_key = self.api_key
                self.client = openai
            except Exception as e:
                print(f"AI Assistant initialization error: {e}")
    
    def process_query(self, query):
        """Process a user query"""
        if not OPENAI_AVAILABLE:
            return "AI Assistant not available. Install openai package: pip install openai"
        
        if not self.client:
            return "AI Assistant not configured. Please add your OpenAI API key to config.json"
        
        try:
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful smart mirror assistant."},
                    {"role": "user", "content": query}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

