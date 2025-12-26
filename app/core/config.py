import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    """
    Basic configuration settings for the application.
    """
    
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USERNAME: str = os.getenv("MYSQL_USERNAME", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "password")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "defaultdb")
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DATABASE_NAME}"

settings = Settings()
