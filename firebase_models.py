from datetime import datetime
from flask_login import UserMixin
from firebase_init import db, get_user_by_email
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    user_doc = db.collection('users').document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        return User(
            uid=user_id,
            username=user_data.get('username'),
            email=user_data.get('email'),
            is_admin=user_data.get('is_admin', False)
        )
    return None

class User(UserMixin):
    """User model compatible with Flask-Login and Firebase"""
    
    def __init__(self, uid=None, username=None, email=None, is_admin=False):
        self.id = uid  # For Flask-Login compatibility
        self.uid = uid
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.utcnow()
    
    def get_id(self):
        """Return the user ID for Flask-Login"""
        return self.uid
    
    def save(self):
        """Save the user to Firestore"""
        user_data = {
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at
        }
        db.collection('users').document(self.uid).set(user_data)
        return self
    
    @staticmethod
    def find_by_email(email):
        """Find a user by email"""
        users = db.collection('users').where('email', '==', email).limit(1).stream()
        for user_doc in users:
            user_data = user_doc.to_dict()
            return User(
                uid=user_doc.id,
                username=user_data.get('username'),
                email=user_data.get('email'),
                is_admin=user_data.get('is_admin', False)
            )
        return None
    
    @staticmethod
    def get_all():
        """Get all users"""
        users = []
        for user_doc in db.collection('users').stream():
            user_data = user_doc.to_dict()
            users.append(User(
                uid=user_doc.id,
                username=user_data.get('username'),
                email=user_data.get('email'),
                is_admin=user_data.get('is_admin', False)
            ))
        return users

class Team:
    """Team model for Firestore"""
    
    def __init__(self, id=None, name=None, division=None, founded_year=None, manager_id=None, logo_url=None):
        self.id = id
        self.name = name
        self.division = division
        self.founded_year = founded_year
        self.manager_id = manager_id
        self.logo_url = logo_url
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save the team to Firestore"""
        team_data = {
            'name': self.name,
            'division': self.division,
            'founded_year': self.founded_year,
            'manager_id': self.manager_id,
            'logo_url': self.logo_url,
            'created_at': self.created_at
        }
        
        if self.id:
            # Update existing team
            db.collection('teams').document(self.id).update(team_data)
        else:
            # Create new team
            ref = db.collection('teams').add(team_data)
            self.id = ref[1].id
        
        return self
    
    @staticmethod
    def find_by_id(team_id):
        """Find a team by ID"""
        team_doc = db.collection('teams').document(team_id).get()
        if team_doc.exists:
            team_data = team_doc.to_dict()
            return Team(
                id=team_id,
                name=team_data.get('name'),
                division=team_data.get('division'),
                founded_year=team_data.get('founded_year'),
                manager_id=team_data.get('manager_id'),
                logo_url=team_data.get('logo_url')
            )
        return None
    
    @staticmethod
    def get_all():
        """Get all teams"""
        teams = []
        for team_doc in db.collection('teams').stream():
            team_data = team_doc.to_dict()
            teams.append(Team(
                id=team_doc.id,
                name=team_data.get('name'),
                division=team_data.get('division'),
                founded_year=team_data.get('founded_year'),
                manager_id=team_data.get('manager_id'),
                logo_url=team_data.get('logo_url')
            ))
        return teams
    
    @staticmethod
    def get_by_manager(manager_id):
        """Get teams managed by a specific user"""
        teams = []
        for team_doc in db.collection('teams').where('manager_id', '==', manager_id).stream():
            team_data = team_doc.to_dict()
            teams.append(Team(
                id=team_doc.id,
                name=team_data.get('name'),
                division=team_data.get('division'),
                founded_year=team_data.get('founded_year'),
                manager_id=team_data.get('manager_id'),
                logo_url=team_data.get('logo_url')
            ))
        return teams

class Player:
    """Player model for Firestore"""
    
    def __init__(self, id=None, first_name=None, last_name=None, date_of_birth=None, 
                 position=None, jersey_number=None, email=None, phone=None, photo_url=None, team_id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.position = position
        self.jersey_number = jersey_number
        self.email = email
        self.phone = phone
        self.photo_url = photo_url
        self.team_id = team_id
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save the player to Firestore"""
        player_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'position': self.position,
            'jersey_number': self.jersey_number,
            'email': self.email,
            'phone': self.phone,
            'photo_url': self.photo_url,
            'team_id': self.team_id,
            'created_at': self.created_at
        }
        
        if self.id:
            # Update existing player
            db.collection('players').document(self.id).update(player_data)
        else:
            # Create new player
            ref = db.collection('players').add(player_data)
            self.id = ref[1].id
        
        return self
    
    @property
    def full_name(self):
        """Get the player's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def find_by_id(player_id):
        """Find a player by ID"""
        player_doc = db.collection('players').document(player_id).get()
        if player_doc.exists:
            player_data = player_doc.to_dict()
            return Player(
                id=player_id,
                first_name=player_data.get('first_name'),
                last_name=player_data.get('last_name'),
                date_of_birth=player_data.get('date_of_birth'),
                position=player_data.get('position'),
                jersey_number=player_data.get('jersey_number'),
                email=player_data.get('email'),
                phone=player_data.get('phone'),
                photo_url=player_data.get('photo_url'),
                team_id=player_data.get('team_id')
            )
        return None
    
    @staticmethod
    def get_all():
        """Get all players"""
        players = []
        for player_doc in db.collection('players').stream():
            player_data = player_doc.to_dict()
            players.append(Player(
                id=player_doc.id,
                first_name=player_data.get('first_name'),
                last_name=player_data.get('last_name'),
                date_of_birth=player_data.get('date_of_birth'),
                position=player_data.get('position'),
                jersey_number=player_data.get('jersey_number'),
                email=player_data.get('email'),
                phone=player_data.get('phone'),
                photo_url=player_data.get('photo_url'),
                team_id=player_data.get('team_id')
            ))
        return players
    
    @staticmethod
    def get_by_team(team_id):
        """Get players for a specific team"""
        players = []
        for player_doc in db.collection('players').where('team_id', '==', team_id).stream():
            player_data = player_doc.to_dict()
            players.append(Player(
                id=player_doc.id,
                first_name=player_data.get('first_name'),
                last_name=player_data.get('last_name'),
                date_of_birth=player_data.get('date_of_birth'),
                position=player_data.get('position'),
                jersey_number=player_data.get('jersey_number'),
                email=player_data.get('email'),
                phone=player_data.get('phone'),
                photo_url=player_data.get('photo_url'),
                team_id=player_data.get('team_id')
            ))
        return players

class Event:
    """Event model for Firestore"""
    
    def __init__(self, id=None, name=None, description=None, location=None, start_date=None,
                 end_date=None, registration_deadline=None, created_by=None):
        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.registration_deadline = registration_deadline
        self.created_by = created_by
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save the event to Firestore"""
        event_data = {
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'registration_deadline': self.registration_deadline,
            'created_by': self.created_by,
            'created_at': self.created_at
        }
        
        if self.id:
            # Update existing event
            db.collection('events').document(self.id).update(event_data)
        else:
            # Create new event
            ref = db.collection('events').add(event_data)
            self.id = ref[1].id
        
        return self
    
    @staticmethod
    def find_by_id(event_id):
        """Find an event by ID"""
        event_doc = db.collection('events').document(event_id).get()
        if event_doc.exists:
            event_data = event_doc.to_dict()
            return Event(
                id=event_id,
                name=event_data.get('name'),
                description=event_data.get('description'),
                location=event_data.get('location'),
                start_date=event_data.get('start_date'),
                end_date=event_data.get('end_date'),
                registration_deadline=event_data.get('registration_deadline'),
                created_by=event_data.get('created_by')
            )
        return None
    
    @staticmethod
    def get_all():
        """Get all events"""
        events = []
        for event_doc in db.collection('events').stream():
            event_data = event_doc.to_dict()
            events.append(Event(
                id=event_doc.id,
                name=event_data.get('name'),
                description=event_data.get('description'),
                location=event_data.get('location'),
                start_date=event_data.get('start_date'),
                end_date=event_data.get('end_date'),
                registration_deadline=event_data.get('registration_deadline'),
                created_by=event_data.get('created_by')
            ))
        return events
    
    def register_team(self, team_id):
        """Register a team for this event"""
        event_team_data = {
            'event_id': self.id,
            'team_id': team_id,
            'registered_at': datetime.utcnow()
        }
        db.collection('event_teams').add(event_team_data)
    
    def get_registered_teams(self):
        """Get teams registered for this event"""
        team_ids = []
        for reg_doc in db.collection('event_teams').where('event_id', '==', self.id).stream():
            reg_data = reg_doc.to_dict()
            team_ids.append(reg_data.get('team_id'))
        
        teams = []
        for team_id in team_ids:
            team = Team.find_by_id(team_id)
            if team:
                teams.append(team)
        
        return teams

class Notification:
    """Notification model for Firestore"""
    
    def __init__(self, id=None, title=None, content=None, created_by=None, is_global=False, target_team_id=None):
        self.id = id
        self.title = title
        self.content = content
        self.created_by = created_by
        self.is_global = is_global
        self.target_team_id = target_team_id
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save the notification to Firestore"""
        notification_data = {
            'title': self.title,
            'content': self.content,
            'created_by': self.created_by,
            'is_global': self.is_global,
            'target_team_id': self.target_team_id,
            'created_at': self.created_at
        }
        
        if self.id:
            # Update existing notification
            db.collection('notifications').document(self.id).update(notification_data)
        else:
            # Create new notification
            ref = db.collection('notifications').add(notification_data)
            self.id = ref[1].id
        
        return self
    
    @staticmethod
    def get_all():
        """Get all notifications"""
        notifications = []
        for notification_doc in db.collection('notifications').stream():
            notification_data = notification_doc.to_dict()
            notifications.append(Notification(
                id=notification_doc.id,
                title=notification_data.get('title'),
                content=notification_data.get('content'),
                created_by=notification_data.get('created_by'),
                is_global=notification_data.get('is_global'),
                target_team_id=notification_data.get('target_team_id')
            ))
        return notifications
    
    @staticmethod
    def get_for_team(team_id):
        """Get notifications for a specific team"""
        notifications = []
        # Get global notifications
        for notification_doc in db.collection('notifications').where('is_global', '==', True).stream():
            notification_data = notification_doc.to_dict()
            notifications.append(Notification(
                id=notification_doc.id,
                title=notification_data.get('title'),
                content=notification_data.get('content'),
                created_by=notification_data.get('created_by'),
                is_global=notification_data.get('is_global'),
                target_team_id=notification_data.get('target_team_id')
            ))
        
        # Get team-specific notifications
        for notification_doc in db.collection('notifications').where('target_team_id', '==', team_id).stream():
            notification_data = notification_doc.to_dict()
            notifications.append(Notification(
                id=notification_doc.id,
                title=notification_data.get('title'),
                content=notification_data.get('content'),
                created_by=notification_data.get('created_by'),
                is_global=notification_data.get('is_global'),
                target_team_id=notification_data.get('target_team_id')
            ))
        
        return notifications