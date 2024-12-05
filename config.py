import os
from dotenv import load_dotenv

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file
load_dotenv(os.path.join(current_dir, '.env'))

# Environment
ENV = os.getenv('ENV', 'qa').lower()

# Host configuration
HOST = os.getenv('HOST', 'https://api-qa.com')

TIMEOUT = int(os.getenv('TIMEOUT', 20))  # seconds

# Schema directory
SCHEMA_DIR = os.path.join(current_dir, 'schemas')


# Secret management (placeholder for actual secret management integration)
def get_secret(secret_name):
    return os.getenv(secret_name)


# Example of how to use the secret management function
API_KEY = get_secret('API_KEY')
ACCESS_TOKEN = get_secret('ACCESS_TOKEN')
