"""
Script alternativo para obtener token de acceso de Gmail API.
Este método permite generar el token sin necesidad de navegador.
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

CREDENTIALS_FILE = settings.GMAIL_API_CREDENTIALS_FILE
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

if not CREDENTIALS_FILE.exists():
    print(f"ERROR: No se encontró {CREDENTIALS_FILE}")
    sys.exit(1)

print("=" * 60)
print("Obteniendo token de acceso para Gmail API")
print("=" * 60)

print("\nIniciando flujo de OAuth...")

flow = InstalledAppFlow.from_client_secrets_file(
    str(CREDENTIALS_FILE), 
    SCOPES
)

flow.redirect_uri = 'http://localhost'

authorization_url, _ = flow.authorization_url(
    access_type='offline',
    prompt='consent'
)

import secrets
import base64
import hashlib

code_verifier = secrets.token_urlsafe(64)[:128]
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b'=').decode()

print(f"CODE_VERIFIER={code_verifier}")
print(f"CODE_CHALLENGE={code_challenge}")

print(f"\n1. Abre esta URL en tu navegador:\n{authorization_url}")
print("\n2. Después de iniciar sesión, copia el código de la URL")
print("   (está después de 'code=')")
print("\n3. Ejecuta:")
print(f'   python email_service/get_token_code.py <código>')
print("\nPor ejemplo: python email_service/get_token_code.py 4/0A...........")
print("\n" + "=" * 60)
sys.exit(0)

with open(TOKEN_FILE, 'w') as token:
    token.write(creds.to_json())

print(f"\n✓ Token guardado en: {TOKEN_FILE}")
print("La configuración de Gmail API está completa!")