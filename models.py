from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def is_valid_password(password):
        #Валидация: только латинские буквы, цифры и знаки препинания
        pattern = r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]*$'
        return bool(re.match(pattern, password)) and len(password) >= 6
    
    @staticmethod
    def is_valid_username(username):
        #Валидация имени пользователя
        pattern = r'^[a-zA-Z0-9_]+$'
        return bool(re.match(pattern, username)) and len(username) >= 3

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(150), nullable=False)
    cover_image = db.Column(db.String(300), default='default-cover.jpg')
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Book {self.title}>'