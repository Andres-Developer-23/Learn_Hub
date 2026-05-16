"""
Script simple para obtener token de Gmail.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILE = BASE_DIR / 'token.json'

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_project.settings')

import django
django.setup()

from django.conf import settings

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

flow = InstalledAppFlow.from_client_secrets_file(
    str(settings.GMAIL_API_CREDENTIALS_FILE),
    SCOPES
)

credentials = flow.run_local_server(port=8080, open_browser=True)

with open(TOKEN_FILE, 'w') as f:
    f.write(credentials.to_json())

print(f"✓ Token guardado en: {TOKEN_FILE}")