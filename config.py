import os

class Config:
    SECRET_KEY = 'secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}