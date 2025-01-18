import sys
import os

# Add your project directory to the sys.path
path = '/home/bookinbinness/mysite/blog_flask'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the environment variable for Flask
os.environ['FLASK_APP'] = 'app.py'

# Import the app from your app.py file
from app import app as application
