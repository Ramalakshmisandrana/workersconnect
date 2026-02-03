from flask import Flask, render_template, redirect, url_for, request, flash, url_for as flask_url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User
import random
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = 'static/profile_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Make sure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_demo_data():
    """Create demo workers with pre-loaded data"""
    
    skills_list = [
        'Electrician', 'Plumber', 'Carpenter', 'Painter', 'AC Technician',
        'Welder', 'Mason', 'Mobile Repair', 'CCTV Installation', 'RO Service',
        'Pest Control', 'Maid', 'Driver', 'Beautician', 'Tailor', 'Cook', 'Gardener'
    ]
    
    # Required workers with specific phone numbers
    required_workers = [
        {'name': 'Ramalakshmi', 'phone': '+919133145667'},
        {'name': 'Vijayalaxmi', 'phone': '+919347389841'},
        {'name': 'Girish', 'phone': '+919392165234'},
        {'name': 'Avinash', 'phone': '+919059387985'},
    ]
    
    # Additional workers with Indian names
    additional_workers = [
        {'name': 'Suresh Kumar', 'phone': '+919876543201'},
        {'name': 'Ramesh Yadav', 'phone': '+919876543202'},
        {'name': 'Priya Sharma', 'phone': '+919876543203'},
        {'name': 'Venkat Reddy', 'phone': '+919876543204'},
        {'name': 'Lakshmi Devi', 'phone': '+919876543205'},
        {'name': 'Raju Naidu', 'phone': '+919876543206'},
        {'name': 'Srinivas Rao', 'phone': '+919876543207'},
        {'name': 'Anjali Patel', 'phone': '+919876543208'},
        {'name': 'Mohan Das', 'phone': '+919876543209'},
        {'name': 'Kavitha Reddy', 'phone': '+919876543210'},
        {'name': 'Satish Gupta', 'phone': '+919876543211'},
    ]
    
    all_workers = required_workers + additional_workers
    
    # Hyderabad coordinates (17.38, 78.48) with slight variations
    hyderabad_lat, hyderabad_lon = 17.385, 78.486
    # Delhi coordinates (28.61, 77.20) with slight variations
    delhi_lat, delhi_lon = 28.613, 77.209
    
    for i, worker_data in enumerate(all_workers):
        # Check if worker already exists
        existing = User.query.filter_by(phone=worker_data['phone']).first()
        if existing:
            continue
            
        # Alternate between Hyderabad and Delhi locations
        if i % 2 == 0:
            base_lat, base_lon = hyderabad_lat, hyderabad_lon
        else:
            base_lat, base_lon = delhi_lat, delhi_lon
        
        # Add random offset (within ~5km)
        lat = base_lat + random.uniform(-0.04, 0.04)
        lon = base_lon + random.uniform(-0.04, 0.04)
        
        # Random skills (2 skills per worker)
        worker_skills = random.sample(skills_list, 2)
        
        # Create worker
        worker = User(
            full_name=worker_data['name'],
            email=f"{worker_data['name'].lower().replace(' ', '.')}@workersconnect.com",
            phone=worker_data['phone'],
            role='worker',
            skills=', '.join(worker_skills),
            experience=random.randint(1, 15),
            rating=round(random.uniform(3.5, 5.0), 1),
            is_available=True,
            latitude=lat,
            longitude=lon
        )
        worker.set_password('123')
        db.session.add(worker)
    
    # Create a demo customer
    existing_customer = User.query.filter_by(email='customer@demo.com').first()
    if not existing_customer:
        customer = User(
            full_name='Demo Customer',
            email='customer@demo.com',
            phone='+919876500000',
            role='customer'
        )
        customer.set_password('123')
        db.session.add(customer)
    
    db.session.commit()
    print("Demo data created successfully!")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = '+91' + request.form.get('phone')
        password = request.form.get('password')
        role = request.form.get('role')
        skills = request.form.get('skills', '')

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('register'))

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            role=role,
            skills=skills if role == 'worker' else None
        )
        user.set_password(password)

        # Handle profile picture
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"profile_{user.id}_{filename}"  # will be renamed after commit
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_pic = filename

        db.session.add(user)
        db.session.commit()

        # Fix filename after user has ID
        if user.profile_pic and 'profile_' not in user.profile_pic:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_pic)
            new_filename = f"profile_{user.id}_{secure_filename(file.filename)}"
            new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
            user.profile_pic = new_filename
            db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Password reset link has been sent to your email.', 'success')
        else:
            flash('Password reset link has been sent to your email.', 'success')
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'customer':
        return render_template('dashboard_customer.html')
    else:
        return render_template('dashboard_worker.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'worker':
        flash('Only workers can access this page.', 'warning')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        current_user.skills = request.form.get('skills')
        current_user.experience = int(request.form.get('experience', 0))
        current_user.is_available = 'is_available' in request.form
    
        lat = request.form.get('latitude')
        lon = request.form.get('longitude')
        if lat and lon:
            try:
                current_user.latitude = float(lat)
                current_user.longitude = float(lon)
            except ValueError:
                flash('Invalid coordinates.', 'warning')

        # Handle profile picture update
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"profile_{current_user.id}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user.profile_pic = filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('profile.html')

@app.route('/search')
def search():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    skill_filter = request.args.get('skill', '').strip()
    
    # Default to Hyderabad
    if lat is None or lon is None:
        lat, lon = 17.385, 78.486
    
    # Get available workers
    workers = User.query.filter_by(role='worker', is_available=True).all()
    
    # Filter by skill
    if skill_filter:
        workers = [w for w in workers if w.skills and skill_filter.lower() in [s.strip().lower() for s in w.skills.split(',')]]
    
    # Calculate distance and filter out workers without location
    workers_with_distance = []
    for worker in workers:
        if worker.latitude and worker.longitude:
            distance = worker.distance_from(lat, lon)
            workers_with_distance.append((worker, distance))
    
    # Sort by distance: nearest first
    workers_with_distance.sort(key=lambda x: x[1] if x[1] is not None else float('inf'))
    
    return render_template('search.html', 
                         workers=workers_with_distance, 
                         skill_filter=skill_filter,
                         lat=lat,
                         lon=lon)

@app.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    if current_user.role != 'worker':
        flash('Only workers can delete their account.', 'danger')
        return redirect(url_for('dashboard'))
    
    user_id = current_user.id
    logout_user()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    
    flash('Your account has been permanently deleted.', 'info')
    return redirect(url_for('index'))

# Initialize database and create demo data
with app.app_context():
    db.create_all()
    create_demo_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
