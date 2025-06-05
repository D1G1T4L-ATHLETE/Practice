from flask import Flask, render_template_string, redirect, url_for, request, flash
from data_sources.weather import get_weather, get_forecast
from quotes import get_random_quote, get_programming_quote
from utils import get_fun_fact, get_current_time, get_daily_joke
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
import os

load_dotenv()  # This loads your .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-please-change')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Add this after app creation
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Error handling for rate limit
@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template_string("""
        <h1>⚠️ Too Many Requests</h1>
        <p>Please slow down! Try again in a few minutes.</p>
        <p><a href="/">Go back home</a></p>
    """), 429

# General error handler
@app.errorhandler(500)
def internal_error(e):
    return render_template_string("""
        <h1>🔧 Oops! Something went wrong</h1>
        <p>We're having some technical difficulties. Please try again later.</p>
        <p><a href="/">Go back home</a></p>
    """), 500

# Page not found error
@app.errorhandler(404)
def page_not_found(e):
    return render_template_string("""
        <h1>🔍 Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <p><a href="/">Go back home</a></p>
    """), 404

# HTML template with some basic styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Daily Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .dashboard-item {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            padding: 20px;
            background: #007bff;
            color: white;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .refresh-btn {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .refresh-btn:hover {
            background: #218838;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌟 YOUR DAILY DASHBOARD 🌟</h1>
        <p>{{ time_info['date'] }} | {{ time_info['time'] }}</p>
    </div>

    <div class="dashboard-item">
        {{ weather }}
    </div>

    <div class="dashboard-item">
        {{ quote }}
    </div>

    <div class="dashboard-item">
        {{ programming_quote }}
    </div>

    <div class="dashboard-item">
        {{ fun_fact }}
    </div>

    <div class="dashboard-item">
        {{ joke }}
    </div>

    <div class="dashboard-item">
        <h3>📊 5-Hour Forecast:</h3>
        {% for forecast in forecasts[:3] %}
            <p>{{ forecast }}</p>
        {% endfor %}
    </div>

    <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Dashboard</button>
</body>
</html>
"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login form template
LOGIN_TEMPLATE = """
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 2em auto; padding: 1em; }
        .form-group { margin-bottom: 1em; }
        input { width: 100%; padding: 8px; margin-top: 5px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h2>Login</h2>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <div class="error">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    <form method="POST">
        <div class="form-group">
            <label>Username</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Password</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Login</button>
    </form>
    <p>New user? <a href="{{ url_for('register') }}">Register here</a></p>
</body>
</html>
"""

# Registration template
REGISTER_TEMPLATE = """
<html>
<head>
    <title>Register</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 2em auto; padding: 1em; }
        .form-group { margin-bottom: 1em; }
        input { width: 100%; padding: 8px; margin-top: 5px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .error { color: red; }
    </style>
</head>
<body>
    <h2>Register</h2>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <div class="error">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    <form method="POST">
        <div class="form-group">
            <label>Username</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Email</label>
            <input type="email" name="email" required>
        </div>
        <div class="form-group">
            <label>Password</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
</body>
</html>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template_string(REGISTER_TEMPLATE)
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template_string(REGISTER_TEMPLATE)
            
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
        
    return render_template_string(REGISTER_TEMPLATE)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    """Render the dashboard as a webpage"""
    try:
        time_info = get_current_time()
        weather_info = get_weather()
        quote = get_random_quote()
        prog_quote = get_programming_quote()
        fun_fact = get_fun_fact()
        joke = get_daily_joke()
        forecasts = get_forecast()
        
        return render_template_string(HTML_TEMPLATE,
            time_info=time_info,
            weather=weather_info,
            quote=quote,
            programming_quote=prog_quote,
            fun_fact=fun_fact,
            joke=joke,
            forecasts=forecasts
        )
    except Exception as e:
        # Log the error (but never log sensitive data!)
        print(f"Dashboard error: {str(e)}")
        return internal_error(e)

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Run the server in debug mode
    app.run(debug=False) 