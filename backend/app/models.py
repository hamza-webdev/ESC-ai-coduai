from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Association tables for many-to-many relationships
player_match = db.Table('player_match',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True),
    db.Column('goals', db.Integer, default=0),
    db.Column('assists', db.Integer, default=0),
    db.Column('yellow_cards', db.Integer, default=0),
    db.Column('red_cards', db.Integer, default=0),
    db.Column('minutes_played', db.Integer, default=0)
)

class User(db.Model):
    """User model for authentication and authorization"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # admin, coach, player, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Player(db.Model):
    """Player model representing a football player"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    jersey_number = db.Column(db.Integer)
    position = db.Column(db.String(30))  # goalkeeper, defender, midfielder, forward
    birth_date = db.Column(db.Date)
    nationality = db.Column(db.String(50))
    photo_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    height = db.Column(db.Float)  # in cm
    weight = db.Column(db.Float)  # in kg
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    category = db.Column(db.String(20))  # Seniors, U19, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team = db.relationship('Team', back_populates='players')
    matches = db.relationship('Match', secondary=player_match, back_populates='players')
    
    def __repr__(self):
        return f'<Player {self.first_name} {self.last_name}>'

class Team(db.Model):
    """Team model representing a football team"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(255))
    founded_year = db.Column(db.Integer)
    home_stadium = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    players = db.relationship('Player', back_populates='team')
    home_matches = db.relationship('Match', foreign_keys='Match.home_team_id', back_populates='home_team')
    away_matches = db.relationship('Match', foreign_keys='Match.away_team_id', back_populates='away_team')
    
    def __repr__(self):
        return f'<Team {self.name}>'

class Match(db.Model):
    """Match model representing a football match"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    venue = db.Column(db.String(100))
    match_type = db.Column(db.String(50))  # championship, cup, friendly
    season = db.Column(db.String(20))  # e.g., "2023-2024"
    status = db.Column(db.String(20), default='upcoming')  # upcoming, played, cancelled
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    home_team = db.relationship('Team', foreign_keys=[home_team_id], back_populates='home_matches')
    away_team = db.relationship('Team', foreign_keys=[away_team_id], back_populates='away_matches')
    players = db.relationship('Player', secondary=player_match, back_populates='matches')
    
    def __repr__(self):
        return f'<Match {self.home_team.name} vs {self.away_team.name} on {self.date}>'

class StaffMember(db.Model):
    """StaffMember model representing a staff member (coach, medical, etc.)"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # head coach, assistant coach, physio, etc.
    photo_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    start_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<StaffMember {self.first_name} {self.last_name} - {self.role}>'

class News(db.Model):
    """News model representing club news and announcements"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    published_date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))  # match report, club news, announcement, etc.
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User')
    
    def __repr__(self):
        return f'<News {self.title}>'

class Partner(db.Model):
    """Partner model representing club sponsors and partners"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(255))
    website_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    partnership_level = db.Column(db.String(50))  # platinum, gold, silver, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Partner {self.name}>'