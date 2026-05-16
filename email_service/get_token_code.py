"""
Script para obtener el token usando el código de autorización.
Ejecutar después de obtener el código desde el navegador.
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
from google_auth_oauthlib.flow import InstalledAppFlow

CREDENTIALS_FILE = settings.GMAIL_API_CREDENTIALS_FILE
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

if len(sys.argv) < 2:
    print("Uso: python email_service/get_token_code.py <código_autorización>")
    sys.exit(1)

code = sys.argv[1].strip()

flow = InstalledAppFlow.from_client_secrets_file(
    str(CREDENTIALS_FILE), 
    SCOPES
)

flow.redirect_uri = 'http://localhost'
flow.fetch_token(code=code)
creds = flow.credentials

with open(TOKEN_FILE, 'w') as token:
    token.write(creds.to_json())

print(f"✓ Token guardado en: {TOKEN_FILE}")
print("Gmail API está listo para usarse!")