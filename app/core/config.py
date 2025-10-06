from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Settings:
    # MongoDB Configuration
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/fastapi_db")
    
    # FastAPI Configuration
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # App Configuration
    APP_NAME: str = "FastAPI MongoDB Demo"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = ENVIRONMENT == "development"

# Create settings instance
settings = Settings()