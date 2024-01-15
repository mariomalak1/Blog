import os

class Config:
    SECRET_KEY = "1e6fcc6160a5d633efd78b334c5416fd"
    SQLALCHEMY_DATABASE_URI = "sqlite:///postapp.db"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("EMAIL_USER")
    MAIL_PASSWORD = os.getenv("APP_PASSWORD_GMAIL")
