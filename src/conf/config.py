#from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    sqlalchemy_database_url: str = "URL"
    secret_key: str = "secret_key"
    algorithm: str = "algorithm"
    mail_username: str = "mail_username"
    mail_password: str = "pass"
    mail_from: str = "mail@mail.ua"
    mail_port: int = 554
    mail_server: str = "server"
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = "name"
    cloudinary_api_key: str = "key"
    cloudinary_api_secret: str = "secret"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
