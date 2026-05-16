"""
Script para obtener token con el flujo completo (guarda el verifier).
"""

import os
import sys
import json
import secrets
import base64
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILE = BASE_DIR / 'token.json'
VERIFIER_FILE = BASE_DIR / 'code_verifier.json'

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_project.settings')

import django
django.setup()

from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow

CREDENTIALS_FILE = settings.GMAIL_API_CREDENTIALS_FILE
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

if len(sys.argv) < 2:
    print("Generando URL de autorización...")
    
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE), 
        SCOPES
    )
    
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip('=')
    
    flow.redirect_uri = 'http://localhost'
    
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        code_challenge=code_challenge,
        code_challenge_method='S256'
    )
    
    with open(VERIFIER_FILE, 'w') as f:
        json.dump({'verifier': code_verifier}, f)
    
    print("\n" + "=" * 60)
    print("1. Abre esta URL en tu navegador:")
    print(authorization_url)
    print("\n2. Después de permitir el acceso, copia el código")
    print("   de la URL (después de 'code=')")
    print(f"\n3. Ejecuta: python email_service/get_token_flow.py <código>")
    print("=" * 60)
    sys.exit(0)

code = sys.argv[1].strip()

with open(VERIFIER_FILE, 'r') as f:
    verifier_data = json.load(f)

code_verifier = verifier_data['verifier']

flow = InstalledAppFlow.from_client_secrets_file(
    str(CREDENTIALS_FILE), 
    SCOPES
)

flow.redirect_uri = 'http://localhost'
flow.fetch_token(code=code, code_verifier=code_verifier)
creds = flow.credentials

with open(TOKEN_FILE, 'w') as token:
    token.write(creds.to_json())

print(f"✓ Token guardado en: {TOKEN_FILE}")
print("Gmail API está listo para usarse!")

Path(VERIFIER_FILE).unlink(missing_ok=True)