from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
from .models import db, User, Player, Team, Match, StaffMember, News, Partner
from .schemas import (
    user_schema, users_schema,
    player_schema, players_schema,
    team_schema, teams_schema,
    match_schema, matches_schema,
    staff_member_schema, staff_members_schema,
    news_schema, news_items_schema,
    partner_schema, partners_schema
)

# Create Blueprint
api_bp = Blueprint('api', __name__)

# Authentication routes
@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate data
    errors = user_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Username or email already exists"}), 409
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        role=data.get('role', 'user')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "message": "User registered successfully",
        "user": user_schema.dump(user),
        "access_token": access_token
    }), 201

@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Login a user"""
    data = request.get_json()
    
    # Find user by username or email
    user = User.query.filter_by(username=data.get('username')).first() or User.query.filter_by(email=data.get('email')).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data.get('password')):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "message": "Login successful",
        "user": user_schema.dump(user),
        "access_token": access_token
    }), 200

# Player routes
@api_bp.route('/players', methods=['GET'])
def get_players():
    """Get all players"""
    # Get query parameters for filtering
    category = request.args.get('category')
    team_id = request.args.get('team_id')
    
    # Base query
    query = Player.query
    
    # Apply filters if provided
    if category:
        query = query.filter_by(category=category)
    if team_id:
        query = query.filter_by(team_id=team_id)
    
    # Execute query
    players = query.all()
    
    return jsonify(players_schema.dump(players)), 200

@api_bp.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    """Get a specific player by ID"""
    player = Player.query.get_or_404(player_id)
    return jsonify(player_schema.dump(player)), 200

@api_bp.route('/players', methods=['POST'])
@jwt_required()
def create_player():
    """Create a new player"""
    data = request.get_json()
    
    # Validate data
    errors = player_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Create new player
    player = Player(**data)
    
    db.session.add(player)
    db.session.commit()
    
    return jsonify({
        "message": "Player created successfully",
        "player": player_schema.dump(player)
    }), 201

@api_bp.route('/players/<int:player_id>', methods=['PUT'])
@jwt_required()
def update_player(player_id):
    """Update a player"""
    player = Player.query.get_or_404(player_id)
    data = request.get_json()
    
    # Update player attributes
    for key, value in data.items():
        if hasattr(player, key):
            setattr(player, key, value)
    
    db.session.commit()
    
    return jsonify({
        "message": "Player updated successfully",
        "player": player_schema.dump(player)
    }), 200

@api_bp.route('/players/<int:player_id>', methods=['DELETE'])
@jwt_required()
def delete_player(player_id):
    """Delete a player"""
    player = Player.query.get_or_404(player_id)
    
    db.session.delete(player)
    db.session.commit()
    
    return jsonify({"message": "Player deleted successfully"}), 200

# Team routes
@api_bp.route('/teams', methods=['GET'])
def get_teams():
    """Get all teams"""
    teams = Team.query.all()
    return jsonify(teams_schema.dump(teams)), 200

@api_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """Get a specific team by ID"""
    team = Team.query.get_or_404(team_id)
    return jsonify(team_schema.dump(team)), 200

@api_bp.route('/teams', methods=['POST'])
@jwt_required()
def create_team():
    """Create a new team"""
    data = request.get_json()
    
    # Validate data
    errors = team_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Create new team
    team = Team(**data)
    
    db.session.add(team)
    db.session.commit()
    
    return jsonify({
        "message": "Team created successfully",
        "team": team_schema.dump(team)
    }), 201

@api_bp.route('/teams/<int:team_id>', methods=['PUT'])
@jwt_required()
def update_team(team_id):
    """Update a team"""
    team = Team.query.get_or_404(team_id)
    data = request.get_json()
    
    # Update team attributes
    for key, value in data.items():
        if hasattr(team, key):
            setattr(team, key, value)
    
    db.session.commit()
    
    return jsonify({
        "message": "Team updated successfully",
        "team": team_schema.dump(team)
    }), 200

@api_bp.route('/teams/<int:team_id>', methods=['DELETE'])
@jwt_required()
def delete_team(team_id):
    """Delete a team"""
    team = Team.query.get_or_404(team_id)
    
    db.session.delete(team)
    db.session.commit()
    
    return jsonify({"message": "Team deleted successfully"}), 200

# Match routes
@api_bp.route('/matches', methods=['GET'])
def get_matches():
    """Get all matches"""
    # Get query parameters for filtering
    status = request.args.get('status')
    season = request.args.get('season')
    team_id = request.args.get('team_id')
    
    # Base query
    query = Match.query
    
    # Apply filters if provided
    if status:
        query = query.filter_by(status=status)
    if season:
        query = query.filter_by(season=season)
    if team_id:
        query = query.filter((Match.home_team_id == team_id) | (Match.away_team_id == team_id))
    
    # Sort by date (upcoming matches first)
    query = query.order_by(Match.date)
    
    # Execute query
    matches = query.all()
    
    return jsonify(matches_schema.dump(matches)), 200

@api_bp.route('/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Get a specific match by ID"""
    match = Match.query.get_or_404(match_id)
    return jsonify(match_schema.dump(match)), 200

@api_bp.route('/matches', methods=['POST'])
@jwt_required()
def create_match():
    """Create a new match"""
    data = request.get_json()
    
    # Validate data
    errors = match_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Create new match
    match = Match(**data)
    
    db.session.add(match)
    db.session.commit()
    
    return jsonify({
        "message": "Match created successfully",
        "match": match_schema.dump(match)
    }), 201

@api_bp.route('/matches/<int:match_id>', methods=['PUT'])
@jwt_required()
def update_match(match_id):
    """Update a match"""
    match = Match.query.get_or_404(match_id)
    data = request.get_json()
    
    # Update match attributes
    for key, value in data.items():
        if hasattr(match, key):
            setattr(match, key, value)
    
    db.session.commit()
    
    return jsonify({
        "message": "Match updated successfully",
        "match": match_schema.dump(match)
    }), 200

@api_bp.route('/matches/<int:match_id>', methods=['DELETE'])
@jwt_required()
def delete_match(match_id):
    """Delete a match"""
    match = Match.query.get_or_404(match_id)
    
    db.session.delete(match)
    db.session.commit()
    
    return jsonify({"message": "Match deleted successfully"}), 200

# Staff routes
@api_bp.route('/staff', methods=['GET'])
def get_staff_members():
    """Get all staff members"""
    # Get query parameters for filtering
    role = request.args.get('role')
    
    # Base query
    query = StaffMember.query
    
    # Apply filters if provided
    if role:
        query = query.filter_by(role=role)
    
    # Execute query
    staff_members = query.all()
    
    return jsonify(staff_members_schema.dump(staff_members)), 200

@api_bp.route('/staff/<int:staff_id>', methods=['GET'])
def get_staff_member(staff_id):
    """Get a specific staff member by ID"""
    staff_member = StaffMember.query.get_or_404(staff_id)
    return jsonify(staff_member_schema.dump(staff_member)), 200

@api_bp.route('/staff', methods=['POST'])
@jwt_required()
def create_staff_member():
    """Create a new staff member"""
    data = request.get_json()
    
    # Validate data
    errors = staff_member_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Create new staff member
    staff_member = StaffMember(**data)
    
    db.session.add(staff_member)
    db.session.commit()
    
    return jsonify({
        "message": "Staff member created successfully",
        "staff_member": staff_member_schema.dump(staff_member)
    }), 201

@api_bp.route('/staff/<int:staff_id>', methods=['PUT'])
@jwt_required()
def update_staff_member(staff_id):
    """Update a staff member"""
    staff_member = StaffMember.query.get_or_404(staff_id)
    data = request.get_json()
    
    # Update staff member attributes
    for key, value in data.items():
        if hasattr(staff_member, key):
            setattr(staff_member, key, value)
    
    db.session.commit()
    
    return jsonify({
        "message": "Staff member updated successfully",
        "staff_member": staff_member_schema.dump(staff_member)
    }), 200

@api_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
@jwt_required()
def delete_staff_member(staff_id):
    """Delete a staff member"""
    staff_member = StaffMember.query.get_or_404(staff_id)
    
    db.session.delete(staff_member)
    db.session.commit()
    
    return jsonify({"message": "Staff member deleted successfully"}), 200

# News routes
@api_bp.route('/news', methods=['GET'])
def get_news_items():
    """Get all news items"""
    # Get query parameters for filtering
    category = request.args.get('category')
    
    # Base query
    query = News.query
    
    # Apply filters if provided
    if category:
        query = query.filter_by(category=category)
    
    # Sort by published date (newest first)
    query = query.order_by(News.published_date.desc())
    
    # Execute query
    news_items = query.all()
    
    return jsonify(news_items_schema.dump(news_items)), 200

@api_bp.route('/news/<int:news_id>', methods=['GET'])
def get_news_item(news_id):
    """Get a specific news item by ID"""
    news_item = News.query.get_or_404(news_id)
    return jsonify(news_schema.dump(news_item)), 200

@api_bp.route('/news', methods=['POST'])
@jwt_required()
def create_news_item():
    """Create a new news item"""
    data = request.get_json()
    
    # Validate data
    errors = news_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Set author_id to current user if not provided
    if 'author_id' not in data:
        data['author_id'] = get_jwt_identity()
    
    # Create new news item
    news_item = News(**data)
    
    db.session.add(news_item)
    db.session.commit()
    
    return jsonify({
        "message": "News item created successfully",
        "news_item": news_schema.dump(news_item)
    }), 201

@api_bp.route('/news/<int:news_id>', methods=['PUT'])
@jwt_required()
def update_news_item(news_id):
    """Update a news item"""
    news_item = News.query.get_or_404(news_id)
    data = request.get_json()
    
    # Update news item attributes
    for key, value in data.items():
        if hasattr(news_item, key):
            setattr(news_item, key, value)
    
    db.session.commit()
    
    return jsonify({
        "message": "News item updated successfully",
        "news_item": news_schema.dump(news_item)
    }), 200

@api_bp.route('/news/<int:news_id>', methods=['DELETE'])
@jwt_required()
def delete_news_item(news_id):
    """Delete a news item"""
    news_item = News.query.get_or_404(news_id)
    
    db.session.delete(news_item)
    db.session.commit()
    
    return jsonify({"message": "News item deleted successfully"}), 200

# Partner routes
@api_bp.route('/partners', methods=['GET'])
def get_partners():
    """Get all partners"""
    partners = Partner.query.all()
    return jsonify(partners_schema.dump(partners)), 200

@api_bp.route('/partners/<int:partner_id>', methods=['GET'])
def get_partner(partner_id):
    """Get a specific partner by ID"""
    partner = Partner.query.get_or_404(partner_id)
    return jsonify(partner_schema.dump(partner)), 200

@api_bp.route('/partners', methods=['POST'])
@jwt_required()
def create_partner():
    """Create a new partner"""
    data = request.get_json()
    
    # Validate data
    errors = partner_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Create new partner
    partner = Partner(**data)
    
    db.session.add(partner)
    db.session.commit()
    
    return jsonify({
        "message": "Partner created successfully",
        "partner": partner_schema.dump(partner)
    }), 201

@api_bp.route('/partners/<int:partner_id>', methods=['PUT'])
@jwt_required()
def update_partner(partner_id):
    """Update a partner"""
    partner = Partner.query.get_or_404(partner_id)
    data = request.get_json()
    
    # Update partner attributes
    for key, value in data.items():
        if hasattr(partner, key):
            setattr(partner, key, value)
    
    db.session.commit()
    
    return jsonify({
        "message": "Partner updated successfully",
        "partner": partner_schema.dump(partner)
    }), 200

@api_bp.route('/partners/<int:partner_id>', methods=['DELETE'])
@jwt_required()
def delete_partner(partner_id):
    """Delete a partner"""
    partner = Partner.query.get_or_404(partner_id)
    
    db.session.delete(partner)
    db.session.commit()
    
    return jsonify({"message": "Partner deleted successfully"}), 200