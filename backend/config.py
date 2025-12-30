"""Configuration management for the procurement agent application."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the backend directory
backend_dir = Path(__file__).parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration."""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    
    # Microsoft Foundry Configuration
    FOUNDRY_PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
    FOUNDRY_MODEL_DEPLOYMENT_NAME = os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME", "gpt-4o")
    
    # Authentication
    USE_AZURE_CREDENTIAL = os.getenv("USE_AZURE_CREDENTIAL", "false").lower() == "true"
    
    # Application Configuration
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if cls.USE_AZURE_CREDENTIAL:
            if not cls.FOUNDRY_PROJECT_ENDPOINT:
                raise ValueError("FOUNDRY_PROJECT_ENDPOINT is required when using Azure credentials")
        else:
            if not cls.AZURE_OPENAI_ENDPOINT or not cls.AZURE_OPENAI_API_KEY:
                raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are required")

config = Config()
