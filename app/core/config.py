from functools import lru_cache
import os

from dotenv import load_dotenv
load_dotenv()

class Settings:
    """
    Basic configuration settings for the application.
    """
    
    # MySQL Database Configuration
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USERNAME: str = os.getenv("MYSQL_USERNAME", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "password")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "defaultdb")
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DATABASE_NAME}"
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # Application Domain
    domain: str = os.getenv("DOMAIN", "http://localhost:8000")
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    # Facebook OAuth Configuration
    FACEBOOK_CLIENT_ID: str = os.getenv("FACEBOOK_CLIENT_ID", "")
    FACEBOOK_CLIENT_SECRET: str = os.getenv("FACEBOOK_CLIENT_SECRET", "")
    FACEBOOK_AUTH_ENDPOINT = "https://www.facebook.com/v18.0/dialog/oauth"
    FACEBOOK_TOKEN_ENDPOINT = "https://graph.facebook.com/v18.0/oauth/access_token"
    FACEBOOK_USERINFO_ENDPOINT = "https://graph.facebook.com/me"
    
    #Stripe API key
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY", "")
    # App Settings
    port: int = int(os.getenv("PORT", 8000))
    reload: bool = os.getenv("RELOAD", "true").lower() == "true"
    REDIRECT_URI: str = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5500/index.html")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

