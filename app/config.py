from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 🌍 App configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # 🗄️ MySQL Configuration
    mysql_user: str
    mysql_password: str
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_db: str

    # 🔗 SQLAlchemy connection string (optional, can be built dynamically)
    database_url: str = ""

    # 🔐 JWT / Security
    secret_key: str
    algorithm: str = "HS256"  # <-- add this for JWT
    access_token_expire_minutes: int = 1440

    # 📧 SMTP (optional)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    from_email: str = ""

    # ✅ Pydantic v2 settings
    model_config = {
        "env_file": ".env",
        "extra": "allow"   # allow extra fields from environment
    }

settings = Settings()
