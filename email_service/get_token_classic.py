"""
Script para obtener token de Gmail API usando OAuth2 clásico (sin PKCE).
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILE = BASE_DIR / 'token.json'

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_project.settings')

import django
django.setup()

from django.conf import settings
import requests

CREDENTIALS_FILE = settings.GMAIL_API_CREDENTIALS_FILE
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

if len(sys.argv) < 2:
    print("Uso: python email_service/get_token_classic.py <código_autorización>")
    sys.exit(1)

code = sys.argv[1].strip()

with open(CREDENTIALS_FILE, 'r') as f:
    client_config = json.load(f)['web']

client_id = client_config['client_id']
client_secret = client_config['client_secret']
token_uri = client_config['token_uri']

data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'grant_type': 'authorization_code',
    'redirect_uri': 'http://localhost'
}

response = requests.post(token_uri, data=data)

if response.status_code == 200:
    token_data = response.json()
    with open(TOKEN_FILE, 'w') as token:
        json.dump(token_data, token)
    print(f"✓ Token guardado en: {TOKEN_FILE}")
    print("Gmail API está listo para usarse!")
else:
    print(f"Error: {response.text}")
    sys.exit(1)