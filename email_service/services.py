import base64
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings

logger = logging.getLogger(__name__)

_gmail_service = None


def _get_gmail_service():
    """Inicializa y retorna el servicio de Gmail API."""
    global _gmail_service
    
    if _gmail_service is not None:
        return _gmail_service
    
    if not getattr(settings, 'GMAIL_API_ENABLED', False):
        logger.warning("Gmail API no está habilitada")
        return None
    
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        credentials_path = getattr(settings, 'GMAIL_API_CREDENTIALS_FILE', None)
        token_path = getattr(settings, 'GMAIL_API_TOKEN_FILE', None)
        
        if not credentials_path or not token_path:
            logger.error("Faltan configuraciones de credenciales de Gmail API")
            return None
        
        credentials = Credentials.from_authorized_user_info(
            info=_load_token_info(token_path),
            scopes=getattr(settings, 'GMAIL_API_SCOPES', ['https://www.googleapis.com/auth/gmail.send'])
        )
        
        _gmail_service = build('gmail', 'v1', credentials=credentials)
        logger.info("Gmail API service inicializado correctamente")
        return _gmail_service
        
    except Exception as e:
        logger.error(f"Error al inicializar Gmail API service: {e}")
        return None


def _load_token_info(token_path):
    """Carga la información del token desde un archivo JSON."""
    import json
    from pathlib import Path
    
    token_file = Path(token_path)
    if not token_file.exists():
        raise FileNotFoundError(f"Token file no encontrado: {token_path}")
    
    with open(token_file, 'r') as f:
        return json.load(f)


def _create_gmail_message(sender, to, subject, body):
    """Crea un mensaje de Gmail en formato RFC 2822 codificado en base64."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def _send_via_gmail_api(service, sender, to, subject, body):
    """Envía el email usando la Gmail API."""
    try:
        message = _create_gmail_message(sender, to, subject, body)
        
        send_response = service.users().messages().send(
            userId='me',
            body=message
        ).execute()
        
        logger.info(f"Email enviado exitosamente a {to}, mensaje ID: {send_response['id']}")
        return True
        
    except Exception as e:
        logger.error(f"Error al enviar email via Gmail API a {to}: {e}")
        return False


def send_student_welcome_email(student, username, password):
    """
    Envía un email de bienvenida al estudiante aceptado con sus credenciales.
    """
    subject = 'Bienvenido a LearnHub - Tus credenciales de acceso'
    
    body = f"""Hola {student.name}!

Tu solicitud de inscripción ha sido APROBADA. Bienvenido a LearnHub!

TUS CREDENCIALES DE ACCESO:
----------------------------------------------
Usuario: {username}
Contraseña: {password}
----------------------------------------------

Accede a la plataforma: http://127.0.0.1:8000/estudiante/login/

Una vez dentro, podrás:
- Acceder a todos tus cursos matriculados
- Ver tu progreso y calificaciones
- Participar en evaluaciones y exámenes
- Acceder a recursos y materiales de estudio

Si tienes alguna duda, contacta al administrador.

Éxito en tu aprendizaje!

Equipo LearnHub
"""
    
    sender = getattr(settings, 'DEFAULT_FROM_EMAIL', 'LearnHub <noreply@learnhub.com>')
    
    if getattr(settings, 'GMAIL_API_ENABLED', False):
        service = _get_gmail_service()
        if service:
            return _send_via_gmail_api(service, sender, student.email, subject, body)
    
    logger.warning("Gmail API no disponible, intentando con método alternativo")
    return False


def send_enrollment_accepted_email(enrollment):
    """
    Envía un email al estudiante cuando su inscripción a un curso es aceptada.
    """
    student = enrollment.student
    course = enrollment.course
    
    username = student.user.username if student.user else student.email.split('@')[0]
    password = student.generated_password or 'N/A'
    
    subject = f'Inscripción aprobada al curso: {course.title}'
    
    body = f"""¡Hola {student.name}!

Tu solicitud de inscripción al curso "{course.title}" ha sido APROBADA. ¡Bienvenido a LearnHub!

📚 DETALLES DEL CURSO
----------------------------------------------
Curso: {course.title}
----------------------------------------------

🔑 TUS CREDENCIALES DE ACCESO
----------------------------------------------
Usuario: {username}
Contraseña: {password}
----------------------------------------------

🔗 ENLACE DE ACCESO
http://127.0.0.1:8000/estudiante/login/

Una vez dentro, podrás:
✅ Acceder a tus cursos matriculados
✅ Ver tu progreso y calificaciones
✅ Participar en evaluaciones y exámenes
✅ Acceder a recursos y materiales de estudio

Si tienes alguna duda, contacta al administrador.

¡Éxito en tu aprendizaje!

Equipo LearnHub
"""
    
    sender = getattr(settings, 'DEFAULT_FROM_EMAIL', 'LearnHub <noreply@learnhub.com>')
    
    if getattr(settings, 'GMAIL_API_ENABLED', False):
        service = _get_gmail_service()
        if service:
            return _send_via_gmail_api(service, sender, student.email, subject, body)
    
    logger.warning("Gmail API no disponible, intentando con método alternativo")
    return False


def send_enrollment_rejected_email(enrollment):
    """
    Envía un email al estudiante cuando su inscripción a un curso es rechazada.
    """
    student = enrollment.student
    course = enrollment.course
    
    subject = f'Inscripción rechazada al curso: {course.title}'
    
    body = f"""Hola {student.name},

Lamentamos informarte que tu solicitud de inscripción al curso "{course.title}" ha sido RECHAZADA.

Información:
----------------------------------------------
Curso: {course.title}
----------------------------------------------

Por favor, contacta al administrador para más información.

Equipo LearnHub
"""
    
    sender = getattr(settings, 'DEFAULT_FROM_EMAIL', 'LearnHub <noreply@learnhub.com>')
    
    if getattr(settings, 'GMAIL_API_ENABLED', False):
        service = _get_gmail_service()
        if service:
            return _send_via_gmail_api(service, sender, student.email, subject, body)
    
    logger.warning("Gmail API no disponible, intentando con método alternativo")
    return False