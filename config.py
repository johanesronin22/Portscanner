import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'super-secret-key-change-in-production'
    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Export paths
    EXPORT_DIR = os.path.join(BASE_DIR, 'exports')
    HTML_EXPORT_DIR = os.path.join(EXPORT_DIR, 'html')
    PDF_EXPORT_DIR = os.path.join(EXPORT_DIR, 'pdf')
    
    # Ensure export directories exist
    os.makedirs(HTML_EXPORT_DIR, exist_ok=True)
    os.makedirs(PDF_EXPORT_DIR, exist_ok=True)
