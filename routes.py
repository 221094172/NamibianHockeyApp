from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from models import User, Team, Player, Event, Notification
from forms import (
    RegistrationForm, LoginForm, TeamRegistrationForm, 
    PlayerRegistrationForm, EventRegistrationForm, 
    TeamEventRegistrationForm, NotificationForm
)
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import uuid

# Create upload directories if they don't exist
def create_upload_dirs():
    # Define necessary upload directories
    upload_dirs = [
        os.path.join('static', 'uploads'),
        os.path.join('static', 'uploads', 'logos'),
        os.path.join('static', 'uploads', 'players')
    ]
    
    # Create each directory if it doesn't exist
    for directory in upload_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)

# Ensure upload directories exist
create_upload_dirs()

@app.route('/')
def index():
    # Get current datetime
    now = datetime.utcnow()
    
    # Get upcoming events (limit to 5)
    upcoming_events = Event.query.filter(Event.start_date > now).order_by(Event.start_date).limit(5).all()
    
    # Get recent notifications (limit to 5)
    recent_notifications = Notification.query.filter_by(is_global=True).order_by(Notification.created_at.desc()).limit(5).all()
    
    return render_template('index.html', upcoming_events=upcoming_events, recent_notifications=recent_notifications, now=now)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Get current datetime
    now = datetime.utcnow()
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form, now=now)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Get current datetime
    now = datetime.utcnow()
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    
    return render_template('login.html', form=form, now=now)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get current datetime
    now = datetime.utcnow()
    
    # Get teams managed by current user
    user_teams = Team.query.filter_by(manager_id=current_user.id).all()
    
    # Get all players in user's teams
    players = []
    for team in user_teams:
        players.extend(team.players)
    
    # Remove duplicates
    players = list(set(players))
    
    # Get events related to user's teams
    events = []
    for team in user_teams:
        events.extend(team.events)
    
    # Remove duplicates
    events = list(set(events))
    
    # Get notifications for user's teams or global notifications
    notifications = Notification.query.filter(
        (Notification.is_global == True) | 
        (Notification.target_team_id.in_([team.id for team in user_teams]))
    ).order_by(Notification.created_at.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                          teams=user_teams, 
                          players=players, 
                          events=events,
                          notifications=notifications,
                          now=now)

@app.route('/teams/register', methods=['GET', 'POST'])
@login_required
def register_team():
    # Get current datetime
    now = datetime.utcnow()
    
    form = TeamRegistrationForm()
    if form.validate_on_submit():
        logo_url = None
        if form.logo.data:
            # Generate a unique filename using UUID
            filename = secure_filename(f"{uuid.uuid4()}_{form.logo.data.filename}")
            logo_path = os.path.join('static', 'uploads', 'logos', filename)
            form.logo.data.save(logo_path)
            logo_url = '/' + logo_path  # Save the path for database storage
        
        team = Team()
        team.name = form.name.data
        team.division = form.division.data
        team.founded_year = form.founded_year.data
        team.logo_url = logo_url
        team.manager_id = current_user.id
        db.session.add(team)
        db.session.commit()
        flash('Team has been registered successfully!', 'success')
        return redirect(url_for('team_list'))
    
    return render_template('team_registration.html', form=form, now=now)

@app.route('/teams')
@login_required
def team_list():
    # Get current datetime
    now = datetime.utcnow()
    
    teams = Team.query.filter_by(manager_id=current_user.id).all()
    return render_template('team_list.html', teams=teams, now=now)

@app.route('/teams/<int:team_id>')
@login_required
def team_details(team_id):
    # Get current datetime
    now = datetime.utcnow()
    
    team = Team.query.get_or_404(team_id)
    
    # Check if current user is the team manager or admin
    if team.manager_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to view this team.', 'danger')
        return redirect(url_for('team_list'))
    
    return render_template('team_list.html', team=team, now=now)

@app.route('/players/register', methods=['GET', 'POST'])
@login_required
def register_player():
    # Get current datetime
    now = datetime.utcnow()
    
    form = PlayerRegistrationForm()
    
    # Populate team_id dropdown with teams managed by current user
    form.team_id.choices = [(team.id, team.name) for team in Team.query.filter_by(manager_id=current_user.id).all()]
    
    if form.validate_on_submit():
        photo_url = None
        if form.photo.data:
            # Generate a unique filename using UUID
            filename = secure_filename(f"{uuid.uuid4()}_{form.photo.data.filename}")
            photo_path = os.path.join('static', 'uploads', 'players', filename)
            form.photo.data.save(photo_path)
            photo_url = '/' + photo_path  # Save the path for database storage
        
        player = Player(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            position=form.position.data,
            jersey_number=form.jersey_number.data,
            email=form.email.data,
            phone=form.phone.data,
            photo_url=photo_url
        )
        
        team = Team.query.get(form.team_id.data)
        if team and team.manager_id == current_user.id:
            player.teams.append(team)
            db.session.add(player)
            db.session.commit()
            flash('Player has been registered successfully!', 'success')
            return redirect(url_for('player_list'))
        else:
            flash('Invalid team selected.', 'danger')
    
    return render_template('player_registration.html', form=form, now=now)

@app.route('/players')
@login_required
def player_list():
    # Get current datetime
    now = datetime.utcnow()
    
    # Get all players from teams managed by current user
    managed_teams = Team.query.filter_by(manager_id=current_user.id).all()
    players = []
    
    for team in managed_teams:
        for player in team.players:
            if player not in players:
                players.append(player)
    
    return render_template('player_list.html', players=players, teams=managed_teams, now=now)

@app.route('/events/register', methods=['GET', 'POST'])
@login_required
def register_event():
    # Get current datetime
    now = datetime.utcnow()
    
    form = EventRegistrationForm()
    
    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            description=form.description.data,
            location=form.location.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            registration_deadline=form.registration_deadline.data,
            created_by=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Event has been created successfully!', 'success')
        return redirect(url_for('event_list'))
    
    return render_template('event_registration.html', form=form, now=now)

@app.route('/events')
def event_list():
    # Get current datetime
    now = datetime.utcnow()
    
    events = Event.query.order_by(Event.start_date).all()
    return render_template('event_list.html', events=events, now=now)

@app.route('/events/<int:event_id>')
def event_details(event_id):
    # Get current datetime
    now = datetime.utcnow()
    
    event = Event.query.get_or_404(event_id)
    return render_template('event_list.html', event=event, now=now)

@app.route('/events/register_team', methods=['GET', 'POST'])
@login_required
def register_team_for_event():
    # Get current datetime
    now = datetime.utcnow()
    
    form = TeamEventRegistrationForm()
    
    # Populate team_id dropdown with teams managed by current user
    form.team_id.choices = [(team.id, team.name) for team in Team.query.filter_by(manager_id=current_user.id).all()]
    
    # Populate event_id dropdown with upcoming events
    form.event_id.choices = [(event.id, event.name) for event in 
                            Event.query.filter(Event.registration_deadline > now).all()]
    
    if form.validate_on_submit():
        team = Team.query.get(form.team_id.data)
        event = Event.query.get(form.event_id.data)
        
        if team and event and team.manager_id == current_user.id:
            if event not in team.events:
                team.events.append(event)
                db.session.commit()
                flash(f'Team {team.name} has been registered for {event.name}!', 'success')
            else:
                flash('Team is already registered for this event.', 'warning')
        else:
            flash('Invalid team or event selected.', 'danger')
        
        return redirect(url_for('event_list'))
    
    return render_template('team_event_registration.html', form=form, now=now)

@app.route('/notifications', methods=['GET', 'POST'])
@login_required
def notifications():
    # Get current datetime
    now = datetime.utcnow()
    
    form = NotificationForm()
    
    # Populate target_team_id dropdown for admin users
    if current_user.is_admin:
        form.target_team_id.choices = [(0, 'All Teams')] + [(team.id, team.name) for team in Team.query.all()]
    else:
        form.target_team_id.choices = [(team.id, team.name) for team in Team.query.filter_by(manager_id=current_user.id).all()]
    
    if form.validate_on_submit():
        notification = Notification(
            title=form.title.data,
            content=form.content.data,
            created_by=current_user.id,
            is_global=form.is_global.data
        )
        
        if not form.is_global.data and form.target_team_id.data:
            team = Team.query.get(form.target_team_id.data)
            if team and (team.manager_id == current_user.id or current_user.is_admin):
                notification.target_team_id = team.id
            else:
                flash('Invalid team selected.', 'danger')
                return render_template('notifications.html', form=form, now=now)
        
        db.session.add(notification)
        db.session.commit()
        flash('Notification has been sent!', 'success')
        return redirect(url_for('notifications'))
    
    # Get notifications visible to current user
    if current_user.is_admin:
        all_notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    else:
        managed_teams = Team.query.filter_by(manager_id=current_user.id).all()
        team_ids = [team.id for team in managed_teams]
        
        all_notifications = Notification.query.filter(
            (Notification.is_global == True) | 
            (Notification.target_team_id.in_(team_ids)) |
            (Notification.created_by == current_user.id)
        ).order_by(Notification.created_at.desc()).all()
    
    return render_template('notifications.html', form=form, notifications=all_notifications, now=now)
