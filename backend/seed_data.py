import os
import sys
import random
from datetime import datetime, timedelta
from faker import Faker
from werkzeug.security import generate_password_hash

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the app and models
from app import create_app
from app.models import db, User, Player, Team, Match, StaffMember, News, Partner

# Initialize Faker
fake = Faker()

def create_admin_user():
    """Create an admin user"""
    admin = User(
        username='admin',
        email='admin@esc.com',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    print("Admin user created")

def create_teams(count=15):
    """Create sample teams"""
    teams = []
    
    # Create Espoir Sportif de Chorbane as the main team
    esc_team = Team(
        name='Espoir Sportif de Chorbane',
        logo_url='https://example.com/esc_logo.png',
        founded_year=1980,
        home_stadium='Stade Municipal de Chorbane',
        description='Espoir Sportif de Chorbane est un club de football tunisien fondé en 1980.'
    )
    db.session.add(esc_team)
    teams.append(esc_team)
    
    # Create other teams
    for i in range(count - 1):
        team = Team(
            name=fake.company() + ' FC',
            logo_url=f'https://example.com/logo_{i}.png',
            founded_year=fake.year(),
            home_stadium=fake.city() + ' Stadium',
            description=fake.paragraph()
        )
        db.session.add(team)
        teams.append(team)
    
    db.session.commit()
    print(f"{count} teams created")
    return teams

def create_players(count=30, teams=None):
    """Create sample players"""
    if not teams:
        teams = Team.query.all()
    
    positions = ['goalkeeper', 'defender', 'midfielder', 'forward']
    categories = ['Seniors', 'U19', 'U17', 'U15']
    
    for i in range(count):
        # Assign most players to ESC team
        team = teams[0] if i < count * 0.7 else random.choice(teams[1:])
        
        player = Player(
            first_name=fake.first_name_male(),
            last_name=fake.last_name(),
            jersey_number=random.randint(1, 99),
            position=random.choice(positions),
            birth_date=fake.date_of_birth(minimum_age=16, maximum_age=40),
            nationality=fake.country(),
            photo_url=f'https://example.com/player_{i}.png',
            bio=fake.paragraph(),
            height=random.uniform(165, 195),
            weight=random.uniform(60, 90),
            team_id=team.id,
            category=random.choice(categories)
        )
        db.session.add(player)
    
    db.session.commit()
    print(f"{count} players created")

def create_matches(count=20, teams=None):
    """Create sample matches"""
    if not teams:
        teams = Team.query.all()
    
    main_team = teams[0]  # ESC team
    other_teams = teams[1:]
    
    match_types = ['championship', 'cup', 'friendly']
    statuses = ['upcoming', 'played', 'cancelled']
    
    # Current season
    season = "2023-2024"
    
    # Start date for matches (3 months ago)
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(count):
        # Alternate between home and away matches for the main team
        is_home = i % 2 == 0
        
        # Select opponent
        opponent = random.choice(other_teams)
        
        # Match date (past or future)
        days_offset = random.randint(-90, 90)
        match_date = start_date + timedelta(days=days_offset)
        
        # Determine status based on date
        if match_date > datetime.now():
            status = 'upcoming'
            home_score = None
            away_score = None
        else:
            status = 'played'
            home_score = random.randint(0, 5)
            away_score = random.randint(0, 5)
        
        # Create match
        if is_home:
            match = Match(
                date=match_date,
                home_team_id=main_team.id,
                away_team_id=opponent.id,
                home_score=home_score,
                away_score=away_score,
                venue=main_team.home_stadium,
                match_type=random.choice(match_types),
                season=season,
                status=status,
                summary=fake.paragraph() if status == 'played' else None
            )
        else:
            match = Match(
                date=match_date,
                home_team_id=opponent.id,
                away_team_id=main_team.id,
                home_score=home_score,
                away_score=away_score,
                venue=opponent.home_stadium,
                match_type=random.choice(match_types),
                season=season,
                status=status,
                summary=fake.paragraph() if status == 'played' else None
            )
        
        db.session.add(match)
    
    db.session.commit()
    print(f"{count} matches created")

def create_staff_members(count=10):
    """Create sample staff members"""
    roles = [
        'Head Coach', 'Assistant Coach', 'Goalkeeper Coach', 
        'Fitness Coach', 'Physiotherapist', 'Team Doctor',
        'Technical Director', 'Scout', 'Analyst', 'Team Manager'
    ]
    
    for i in range(count):
        staff = StaffMember(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=roles[i] if i < len(roles) else random.choice(roles),
            photo_url=f'https://example.com/staff_{i}.png',
            bio=fake.paragraph(),
            start_date=fake.date_between(start_date='-5y', end_date='today')
        )
        db.session.add(staff)
    
    db.session.commit()
    print(f"{count} staff members created")

def create_news(count=15):
    """Create sample news items"""
    categories = ['match report', 'club news', 'announcement', 'interview', 'press release']
    
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    
    for i in range(count):
        news = News(
            title=fake.sentence(),
            content='\n\n'.join(fake.paragraphs(nb=5)),
            image_url=f'https://example.com/news_{i}.png',
            published_date=fake.date_time_between(start_date='-60d', end_date='now'),
            category=random.choice(categories),
            author_id=admin.id if admin else None
        )
        db.session.add(news)
    
    db.session.commit()
    print(f"{count} news items created")

def create_partners(count=8):
    """Create sample partners"""
    partnership_levels = ['platinum', 'gold', 'silver', 'bronze']
    
    for i in range(count):
        partner = Partner(
            name=fake.company(),
            logo_url=f'https://example.com/partner_{i}.png',
            website_url=fake.url(),
            description=fake.paragraph(),
            partnership_level=random.choice(partnership_levels)
        )
        db.session.add(partner)
    
    db.session.commit()
    print(f"{count} partners created")

def seed_data():
    """Seed the database with sample data"""
    print("Starting data seeding...")
    
    # Create admin user
    create_admin_user()
    
    # Create teams
    teams = create_teams(15)
    
    # Create players
    create_players(30, teams)
    
    # Create matches
    create_matches(20, teams)
    
    # Create staff members
    create_staff_members(10)
    
    # Create news
    create_news(15)
    
    # Create partners
    create_partners(8)
    
    print("Data seeding completed successfully!")

if __name__ == '__main__':
    # Create app context
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Seed data
        seed_data()