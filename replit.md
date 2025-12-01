# WorkersConnect - Location-Based Skilled Worker Platform

## Overview
WorkersConnect is a location-based platform that connects customers with local skilled workers in India. Customers can find electricians, plumbers, carpenters, and other service providers within a 10km radius and call them directly.

## Project Structure
```
/
├── app.py              # Main Flask application with routes
├── config.py           # Configuration settings
├── models.py           # Database models (User with Customer/Worker roles)
├── static/
│   ├── css/
│   │   └── style.css   # Custom CSS with modern design
│   └── images/
│       └── workers-hero.png  # Hero section background
├── templates/
│   ├── base.html              # Base template with common elements
│   ├── index.html             # Homepage with hero section
│   ├── register.html          # User registration
│   ├── login.html             # User login
│   ├── forgot_password.html   # Password reset (demo)
│   ├── dashboard_customer.html # Customer dashboard
│   ├── dashboard_worker.html   # Worker dashboard
│   ├── profile.html           # Worker profile editing
│   └── search.html            # Search results with worker cards
└── workersconnect.db   # SQLite database (auto-created)
```

## Features
- **User Roles**: Customer (service seeker) and Worker (service provider)
- **Geolocation**: HTML5 geolocation API for finding nearby workers
- **Distance Calculation**: Haversine formula for accurate distance
- **Smart Ranking**: Workers ranked by 50% rating + 30% experience + 20% proximity
- **Direct Calling**: tel: links for instant phone dialing on mobile

## Tech Stack
- **Backend**: Python Flask
- **Database**: SQLite with Flask-SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5, Font Awesome, Custom CSS
- **Font**: Poppins (Google Fonts)

## Demo Accounts
All demo accounts use password: `123`

### Customer Account
- Email: customer@demo.com
- Password: 123

### Workers (15 pre-loaded)
Includes 4 specific contacts:
- Ramalakshmi: +919133145667
- Vijayalaxmi: +919347389841
- Girish: +919392165234
- Avinash: +919059387985

## Running the Application
```bash
python app.py
```
The app runs on port 5000.

## Recent Changes
- Initial project setup (December 2025)
- Created beautiful hero section matching provided design
- Implemented full authentication system
- Added 15 demo workers with realistic data
- Implemented geolocation-based search with Haversine formula
- Created responsive worker cards with call functionality
