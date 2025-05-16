# Namibia Hockey Union App - PythonAnywhere Deployment Guide

This guide will walk you through deploying your Namibia Hockey Union Flask application to PythonAnywhere.

## Step 1: Create a PythonAnywhere Account

1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com/) and sign up for a free account
2. Verify your email and log in to your dashboard

## Step 2: Set Up Your MySQL Database

1. Click on the **Databases** tab in the top menu
2. Create a MySQL password when prompted and note it down
3. Under "Create a new database," enter a name (e.g., `namibia_hockey`) and click "Create"
4. Your database will be created with the name `yourusername$namibia_hockey`

## Step 3: Upload Your Project Files

### Option A: Upload ZIP File
1. On your local machine, compress your entire project directory into a ZIP file
2. In PythonAnywhere, go to the **Files** tab
3. Click "Upload a file" and select your ZIP file
4. After uploading, go to **Consoles** → **Bash**
5. Run: `unzip your-zipfile.zip -d namibia_hockey_app`

### Option B: Use Git
If your project is on GitHub:
1. In PythonAnywhere, go to **Consoles** → **Bash**
2. Run: `git clone https://github.com/yourusername/your-repo.git namibia_hockey_app`

## Step 4: Create a Virtual Environment and Install Dependencies

In the Bash console:
```bash
# Navigate to your project directory
cd namibia_hockey_app

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install flask flask-login flask-sqlalchemy flask-wtf pillow email-validator mysqlclient gunicorn
```

## Step 5: Create a MySQL-Compatible Database Configuration

1. Create a database configuration file by running:

```bash
# Make sure you're in your project directory
cd ~/namibia_hockey_app

# Create a MySQL-specific configuration
cat > mysql_config.py << EOL
import os

# Database configuration
SQLALCHEMY_DATABASE_URI = 'mysql://yourusername:your_password@yourusername.mysql.pythonanywhere-services.com/yourusername$namibia_hockey'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_recycle": 280,
    "pool_pre_ping": True
}
EOL
```

Replace `yourusername` with your actual PythonAnywhere username and `your_password` with your MySQL password.

## Step 6: Configure Your Web App

1. Click on the **Web** tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose your domain (usually yourusername.pythonanywhere.com)
4. Select "Manual configuration" (not "Flask")
5. Choose Python 3.10 (or closest available version)

## Step 7: Configure Application Settings

In the web app configuration page:

1. **Source code:**
   - Set to: `/home/yourusername/namibia_hockey_app`
   - Working directory: `/home/yourusername/namibia_hockey_app`

2. **Virtualenv:**
   - Set to: `/home/yourusername/namibia_hockey_app/venv`

3. **Static files:**
   - URL: `/static/` → Directory: `/home/yourusername/namibia_hockey_app/static`

4. **WSGI file:**
   - Click on the WSGI configuration file link

5. Edit the WSGI file:
```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/namibia_hockey_app'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['SECRET_KEY'] = 'your_secret_key'
os.environ['DATABASE_URL'] = 'mysql://yourusername:your_password@yourusername.mysql.pythonanywhere-services.com/yourusername$namibia_hockey'
os.environ['ADMIN_EMAIL'] = 'aadmin@gmail.com'
os.environ['ADMIN_PASSWORD'] = 'admin'
os.environ['ADMIN_SECRET_CODE'] = 'admin'
os.environ['FLASK_DEBUG'] = 'False'

# Import your Flask application
from main import app as application
```

Replace `yourusername` with your actual PythonAnywhere username and `your_password` with your MySQL password.

## Step 8: Initialize Your Database

In the Bash console:
```bash
cd ~/namibia_hockey_app
source venv/bin/activate
python

# In the Python console:
from app import app, db
with app.app_context():
    db.create_all()
    exit()
```

## Step 9: Create Uploads Directory

In the Bash console:
```bash
cd ~/namibia_hockey_app
mkdir -p static/uploads/team_logos
mkdir -p static/uploads/player_photos
```

## Step 10: Reload Your Web App

1. Go back to the **Web** tab
2. Click the big green "Reload" button for your web app

## Step 11: Test Your Application

1. Visit your app at yourusername.pythonanywhere.com
2. Test the functionality:
   - Try to register and login
   - Create a team and add players
   - Upload images and verify they display correctly

## Troubleshooting

If you encounter issues:

1. Check the **Web** tab → **Log files** section:
   - Error log
   - Server log
   - Access log

2. Database issues:
   - Go to **Databases** tab → **phpMyAdmin** to directly inspect your database

3. File permissions:
   - Run: `chmod -R 755 ~/namibia_hockey_app/static/uploads`

## Next Steps

1. **Custom Domain**: If you want to use a custom domain, you'll need to upgrade to a paid plan
2. **Scheduled Tasks**: Use the "Tasks" tab to set up regular backups
3. **Database Scaling**: The free tier includes 512MB of database storage, which should be sufficient for your app

## Security Recommendations

1. Change the default admin password
2. Generate a proper random secret key
3. Consider enabling HTTPS through PythonAnywhere's settings