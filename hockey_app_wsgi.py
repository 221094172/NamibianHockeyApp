import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/myproject'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables - replace with your actual values
os.environ['SECRET_KEY'] = 'namibia_hockey_secret_key'
os.environ['DATABASE_URL'] = 'mysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere-services.com/yourusername$dbname'
os.environ['ADMIN_EMAIL'] = 'aadmin@gmail.com'
os.environ['ADMIN_PASSWORD'] = 'admin'
os.environ['ADMIN_SECRET_CODE'] = 'admin'
os.environ['FLASK_DEBUG'] = 'False'

# Import the Flask application object
from main import app as application  # noqa