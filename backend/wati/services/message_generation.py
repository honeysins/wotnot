import google.generativeai as genai
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MessageGenerationService:
    def __init__(self):
        self.model = None
        self.api_key = os.getenv('GEMINI_API_KEY')
    
    def initialize_model(self):
        """Initialize the Gemini model with the API key from environment"""
        try:
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            return True
        except Exception as e:
            print(f"Error initializing Gemini model: {str(e)}")
            return False
    
    async def generate_message(self, prompt: str) -> dict:
        """
        Generate a message based on the user's prompt using Gemini API
        
        Args:
            prompt: User's input prompt for message generation
            
        Returns:
            dict: Contains generated_message, success status, and error if any
        """
        try:
            # Initialize model with API key from environment
            if not self.initialize_model():
                return {
                    "generated_message": "",
                    "success": False,
                    "error": "Failed to initialize Gemini model. Please check GEMINI_API_KEY in environment variables."
                }
            
            # Create a more specific prompt for message generation
            system_prompt = f"""
            You are a helpful assistant that generates professional messages for business communications. 
            Based on the user's request, generate a well-structured message that can be used for customer communication.
            
            User's request: {prompt}
            
            Please generate a professional message that:
            1. Is appropriate for the context
            2. Uses placeholders like {{name}} for personalization
            3. Is concise but warm and professional
            4. Can be easily customized by the user
            
            Return only the generated message without any additional explanations.
            """
            
            # Generate the message
            response = self.model.generate_content(system_prompt)
            generated_message = response.text.strip()
            
            return {
                "generated_message": generated_message,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            return {
                "generated_message": "",
                "success": False,
                "error": f"Error generating message: {str(e)}"
            }

# Create a singleton instance
message_generation_service = MessageGenerationService()
