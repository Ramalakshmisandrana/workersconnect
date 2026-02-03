from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from math import radians, cos, sin, asin, sqrt
from flask import url_for

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'customer' or 'worker'
    profile_pic = db.Column(db.String(200), nullable=True)  # stores filename like "profile_123.jpg"
    
    # Worker-specific fields
    skills = db.Column(db.String(500), nullable=True)
    experience = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=4.0)
    is_available = db.Column(db.Boolean, default=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_skills_list(self):
        if self.skills:
            return [s.strip() for s in self.skills.split(',')]
        return []
    
    def get_profile_pic_url(self):
        if self.profile_pic:
            return url_for('static', filename=f'profile_pics/{self.profile_pic}')
        return None

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """Calculate the great circle distance in kilometers between two points"""
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    def distance_from(self, lat, lon):
        """Calculate distance from given coordinates"""
        if self.latitude and self.longitude:
            return self.haversine(lat, lon, self.latitude, self.longitude)
        return float('inf')
    
    def ranking_score(self, distance):
        """Calculate ranking score: 50% rating + 30% experience + 20% proximity"""
        max_distance = 10  # km
        proximity_score = max(0, (max_distance - distance) / max_distance * 100)
        rating_score = (self.rating / 5) * 100
        experience_score = min(self.experience / 10, 1) * 100
        
        return (rating_score * 0.5) + (experience_score * 0.3) + (proximity_score * 0.2)
