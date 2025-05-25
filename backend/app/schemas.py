from marshmallow import Schema, fields, validate, post_load
from .models import User, Player, Team, Match, StaffMember, News, Partner

class UserSchema(Schema):
    """Schema for serializing and deserializing User objects"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))
    role = fields.Str(validate=validate.OneOf(['admin', 'coach', 'player', 'user']), default='user')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class PlayerSchema(Schema):
    """Schema for serializing and deserializing Player objects"""
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    jersey_number = fields.Int()
    position = fields.Str(validate=validate.OneOf(['goalkeeper', 'defender', 'midfielder', 'forward']))
    birth_date = fields.Date()
    nationality = fields.Str()
    photo_url = fields.Str()
    bio = fields.Str()
    height = fields.Float()
    weight = fields.Float()
    team_id = fields.Int()
    category = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested relationships
    team = fields.Nested('TeamSchema', exclude=('players',), dump_only=True)

class TeamSchema(Schema):
    """Schema for serializing and deserializing Team objects"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    logo_url = fields.Str()
    founded_year = fields.Int()
    home_stadium = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested relationships
    players = fields.List(fields.Nested('PlayerSchema', exclude=('team',)), dump_only=True)

class PlayerMatchStatsSchema(Schema):
    """Schema for player statistics in a match"""
    player_id = fields.Int(required=True)
    match_id = fields.Int(required=True)
    goals = fields.Int(default=0)
    assists = fields.Int(default=0)
    yellow_cards = fields.Int(default=0)
    red_cards = fields.Int(default=0)
    minutes_played = fields.Int(default=0)

class MatchSchema(Schema):
    """Schema for serializing and deserializing Match objects"""
    id = fields.Int(dump_only=True)
    date = fields.DateTime(required=True)
    home_team_id = fields.Int(required=True)
    away_team_id = fields.Int(required=True)
    home_score = fields.Int()
    away_score = fields.Int()
    venue = fields.Str()
    match_type = fields.Str(validate=validate.OneOf(['championship', 'cup', 'friendly']))
    season = fields.Str()
    status = fields.Str(validate=validate.OneOf(['upcoming', 'played', 'cancelled']), default='upcoming')
    summary = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested relationships
    home_team = fields.Nested('TeamSchema', exclude=('players',), dump_only=True)
    away_team = fields.Nested('TeamSchema', exclude=('players',), dump_only=True)
    player_stats = fields.List(fields.Nested(PlayerMatchStatsSchema), dump_only=True)

class StaffMemberSchema(Schema):
    """Schema for serializing and deserializing StaffMember objects"""
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    role = fields.Str(required=True)
    photo_url = fields.Str()
    bio = fields.Str()
    start_date = fields.Date()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class NewsSchema(Schema):
    """Schema for serializing and deserializing News objects"""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    image_url = fields.Str()
    published_date = fields.DateTime()
    category = fields.Str()
    author_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested relationships
    author = fields.Nested(UserSchema, only=('id', 'username'), dump_only=True)

class PartnerSchema(Schema):
    """Schema for serializing and deserializing Partner objects"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    logo_url = fields.Str()
    website_url = fields.Str()
    description = fields.Str()
    partnership_level = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

match_schema = MatchSchema()
matches_schema = MatchSchema(many=True)

staff_member_schema = StaffMemberSchema()
staff_members_schema = StaffMemberSchema(many=True)

news_schema = NewsSchema()
news_items_schema = NewsSchema(many=True)

partner_schema = PartnerSchema()
partners_schema = PartnerSchema(many=True)