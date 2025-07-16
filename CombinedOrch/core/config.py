"""
Core configuration for the Educational Tool Chatbot API
"""

import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings:
    """Application settings"""
    
    # API Configuration
    TITLE = "Educational Tool Chatbot"
    DESCRIPTION = "AI-powered chatbot that recommends educational tools based on user queries"
    VERSION = "1.0.0"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # CORS Settings
    CORS_ORIGINS = ["*"]
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    @classmethod
    def validate_settings(cls):
        """Validate required settings"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        logger.info("Configuration validated successfully")

# Create settings instance
settings = Settings() 