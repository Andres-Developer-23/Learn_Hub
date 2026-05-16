"""
Script para obtener credenciales de Gmail API.

Para usar la Gmail API necesitas:
1. credentials.json: Archivo de credenciales OAuth2 de Google Cloud Console
2. token.json: Token de acceso para autenticación

Este script te guiará en el proceso de obtención de credenciales.
"""

import os
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent.parent


def get_credentials():
    """
    Obtiene credenciales OAuth2 para Gmail API.
    
    Requiere un archivo de credenciales en el directorio raíz del proyecto.
    Este archivo se obtiene desde Google Cloud Console:
    1. Ve a https://console.cloud.google.com/
    2. Crea un proyecto o usa uno existente
    3. Habilita la Gmail API
    4. Crea credenciales OAuth2 (tipo Aplicación de escritorio)
    5. Descarga el archivo JSON y colócalo en la raíz del proyecto
    """
    import django
    import sys
    import os
    
    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_project.settings')
    django.setup()
    
    from django.conf import settings
    
    credentials_path = getattr(settings, 'GMAIL_API_CREDENTIALS_FILE', None)
    token_path = getattr(settings, 'GMAIL_API_TOKEN_FILE', None)
    
    if not credentials_path or not Path(credentials_path).exists():
        print(f"\nERROR: No se encontró {credentials_path}")
        print("\nPara obtener credenciales:")
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Crea un proyecto o selecciona uno existente")
        print("3. Busca y habilita 'Gmail API'")
        print("4. Ve a 'Credenciales' > 'Crear Credenciales' > 'ID de cliente OAuth'")
        print("5. Selecciona 'Aplicación de escritorio'")
        print("6. Descarga el archivo JSON y guárdalo como 'credentials.json'")
        print(f"   en: {BASE_DIR}")
        return None
    
    scopes = ['https://www.googleapis.com/auth/gmail.send']
    
    creds = None
    
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), scopes
            )
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds


def test_gmail_api():
    """Prueba la conexión con Gmail API."""
    print("\n--- Probando conexión con Gmail API ---")
    
    try:
        creds = get_credentials()
        
        if not creds:
            print("No se pudieron obtener credenciales")
            return False
        
        service = build('gmail', 'v1', credentials=creds)
        
        user_info = service.users().getProfile(userId='me').execute()
        print(f"✓ Conexión exitosa!")
        print(f"  Email asociado: {user_info['emailAddress']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error al conectar con Gmail API: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("Configuración de Gmail API")
    print("=" * 60)
    
    test_gmail_api()