import base64
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)

_gmail_service = None


def _get_gmail_service():
    """Inicializa y retorna el servicio de Gmail API con renovación automática del token."""
    global _gmail_service
    
    if _gmail_service is not None:
        return _gmail_service
    
    if not getattr(settings, 'GMAIL_API_ENABLED', False):
        logger.warning("Gmail API no está habilitada")
        return None
    
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        token_path = getattr(settings, 'GMAIL_API_TOKEN_FILE', None)
        scopes = getattr(settings, 'GMAIL_API_SCOPES', ['https://www.googleapis.com/auth/gmail.send'])
        
        if not token_path:
            logger.error("Falta configuración de token de Gmail API")
            return None
        
        token_info = _load_token_info(token_path)
        credentials = Credentials.from_authorized_user_info(
            info=token_info,
            scopes=scopes
        )
        
        if credentials.expired and credentials.refresh_token:
            logger.info("Token expirado, renovando automáticamente...")
            credentials.refresh(Request())
            _save_token(token_path, credentials)
            logger.info("Token renovado y guardado exitosamente")
        
        _gmail_service = build('gmail', 'v1', credentials=credentials)
        logger.info("Gmail API service inicializado correctamente")
        return _gmail_service
        
    except Exception as e:
        logger.error(f"Error al inicializar Gmail API service: {e}")
        return None


def _load_token_info(token_path):
    """Carga la información del token desde un archivo JSON."""
    token_file = Path(token_path)
    if not token_file.exists():
        raise FileNotFoundError(f"Token file no encontrado: {token_path}")
    
    with open(token_file, 'r') as f:
        return json.load(f)


def _save_token(token_path, credentials):
    """Guarda las credenciales renovadas en el archivo token.json."""
    token_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry': credentials.expiry.isoformat() if credentials.expiry else None,
    }
    with open(token_path, 'w') as f:
        json.dump(token_data, f, indent=2)


def _create_gmail_message(sender, to, subject, text_body, html_body=None):
    """Crea un mensaje de Gmail en formato RFC 2822 con soporte HTML."""
    if html_body:
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message.attach(MIMEText(text_body, 'plain'))
        message.attach(MIMEText(html_body, 'html'))
    else:
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message.attach(MIMEText(text_body, 'plain'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def _send_via_gmail_api(service, sender, to, subject, text_body, html_body=None):
    """Envía el email usando la Gmail API con soporte HTML."""
    try:
        message = _create_gmail_message(sender, to, subject, text_body, html_body)

        send_response = service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        logger.info(f"Email enviado exitosamente a {to}, mensaje ID: {send_response['id']}")
        return True

    except Exception as e:
        logger.error(f"Error al enviar email via Gmail API a {to}: {e}")
        return False


def _build_html_template(title, content_html):
    """Construye la plantilla HTML profesional para los correos."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:0; background-color:#f0f2f5; font-family:'Segoe UI',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f2f5;">
    <tr>
      <td align="center" style="padding:30px 15px;">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px; width:100%;">

          <tr>
            <td style="background:linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius:16px 16px 0 0; padding:35px 30px; text-align:center;">
              <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
                <tr>
                  <td style="background:rgba(255,255,255,0.15); border-radius:12px; padding:8px 20px; text-align:center;">
                    <span style="color:#ffffff; font-size:24px; font-weight:800; letter-spacing:1px;">LearnHub</span>
                  </td>
                </tr>
              </table>
              <h1 style="color:#ffffff; font-size:26px; margin:20px 0 0 0; font-weight:700;">{title}</h1>
            </td>
          </tr>

          <tr>
            <td style="background-color:#ffffff; padding:35px 30px; border-left:1px solid #e5e7eb; border-right:1px solid #e5e7eb;">
              {content_html}
            </td>
          </tr>

          <tr>
            <td style="background-color:#1e293b; border-radius:0 0 16px 16px; padding:25px 30px; text-align:center; border-left:1px solid #1e293b; border-right:1px solid #1e293b;">
              <p style="color:#94a3b8; font-size:13px; margin:0 0 4px 0;">&copy; 2026 LearnHub &mdash; Plataforma de Aprendizaje</p>
              <p style="color:#64748b; font-size:12px; margin:0;">Este es un mensaje autom&aacute;tico. Por favor no respondas a este correo.</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def _build_credentials_box(username, password):
    """Construye el bloque HTML para mostrar credenciales."""
    return f"""
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; margin:20px 0;">
        <tr>
          <td style="background:linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius:12px 12px 0 0; padding:12px 20px;">
            <p style="color:#ffffff; font-size:14px; font-weight:700; margin:0; letter-spacing:1px; text-transform:uppercase;">Credenciales de Acceso</p>
          </td>
        </tr>
        <tr>
          <td style="padding:20px;">
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td width="100" style="padding:8px 0; color:#64748b; font-size:14px; font-weight:600;">Usuario:</td>
                <td style="padding:8px 0; color:#1e293b; font-size:15px; font-family:'Courier New',monospace; font-weight:700; word-break:break-word;">{username}</td>
              </tr>
              <tr>
                <td width="100" style="padding:8px 0; color:#64748b; font-size:14px; font-weight:600; border-top:1px solid #e2e8f0;">Contrase&ntilde;a:</td>
                <td style="padding:8px 0; color:#1e293b; font-size:15px; font-family:'Courier New',monospace; font-weight:700; border-top:1px solid #e2e8f0; word-break:break-word;">{password}</td>
              </tr>
            </table>
          </td>
        </tr>
      </table>"""


def send_student_welcome_email(student, username, password):
    """
    Envía un email de bienvenida al estudiante aceptado con sus credenciales.
    """
    subject = 'Bienvenido a LearnHub - Tus credenciales de acceso'

    text_body = f"""Hola {student.name}!

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

Equipo LearnHub"""

    content_html = f"""
      <p style="color:#475569; font-size:16px; line-height:1.6; margin:0 0 20px 0;">
        Hola <strong style="color:#1e293b;">{student.name}</strong>,
      </p>
      <p style="color:#475569; font-size:16px; line-height:1.6; margin:0 0 25px 0;">
        Tu solicitud de inscripci&oacute;n ha sido <strong style="color:#059669;">APROBADA</strong>.
        &iexcl;Bienvenido a <strong>LearnHub</strong>!
      </p>

      {_build_credentials_box(username, password)}

      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center" style="padding:25px 0;">
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="background:linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius:8px; text-align:center;">
                  <a href="http://127.0.0.1:8000/estudiante/login/" style="display:inline-block; padding:14px 40px; color:#ffffff; font-size:16px; font-weight:700; text-decoration:none; border-radius:8px;">Acceder a la Plataforma</a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <p style="color:#475569; font-size:15px; line-height:1.6; margin:0 0 10px 0;">
        Una vez dentro, podr&aacute;s:
      </p>
      <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 20px 0;">
        <tr>
          <td style="padding:5px 0 5px 20px; color:#475569; font-size:14px;">&#10003; Acceder a todos tus cursos matriculados</td>
        </tr>
        <tr>
          <td style="padding:5px 0 5px 20px; color:#475569; font-size:14px;">&#10003; Ver tu progreso y calificaciones</td>
        </tr>
        <tr>
          <td style="padding:5px 0 5px 20px; color:#475569; font-size:14px;">&#10003; Participar en evaluaciones y ex&aacute;menes</td>
        </tr>
        <tr>
          <td style="padding:5px 0 5px 20px; color:#475569; font-size:14px;">&#10003; Acceder a recursos y materiales de estudio</td>
        </tr>
      </table>

      <hr style="border:none; border-top:1px solid #e2e8f0; margin:25px 0;">

      <p style="color:#64748b; font-size:14px; line-height:1.5; margin:0 0 5px 0;">
        Si tienes alguna duda, contacta al administrador.
      </p>
      <p style="color:#475569; font-size:15px; line-height:1.5; margin:0;">
        &iexcl;&Eacute;xito en tu aprendizaje!
      </p>
      <p style="color:#1e293b; font-size:15px; font-weight:600; margin:5px 0 0 0;">
        Equipo LearnHub
      </p>"""

    sender = getattr(settings, 'DEFAULT_FROM_EMAIL', 'LearnHub <noreply@learnhub.com>')
    html_body = _build_html_template('&iexcl;Bienvenido a LearnHub!', content_html)

    if getattr(settings, 'GMAIL_API_ENABLED', False):
        service = _get_gmail_service()
        if service:
            return _send_via_gmail_api(service, sender, student.email, subject, text_body, html_body)

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

    text_body = f"""¡Hola {student.name}!

Tu solicitud de inscripción al curso "{course.title}" ha sido APROBADA. ¡Bienvenido a LearnHub!

DETALLES DEL CURSO
----------------------------------------------
Curso: {course.title}
----------------------------------------------

TUS CREDENCIALES DE ACCESO
----------------------------------------------
Usuario: {username}
Contraseña: {password}
----------------------------------------------

Accede a la plataforma: http://127.0.0.1:8000/estudiante/login/

Una vez dentro, podrás:
- Acceder a tus cursos matriculados
- Ver tu progreso y calificaciones
- Participar en evaluaciones y exámenes
- Acceder a recursos y materiales de estudio

Si tienes alguna duda, contacta al administrador.

¡Éxito en tu aprendizaje!

Equipo LearnHub"""

    content_html = f"""
      <p style="color:#475569; font-size:16px; line-height:1.6; margin:0 0 20px 0;">
        &iexcl;Hola <strong style="color:#1e293b;">{student.name}</strong>,
      </p>
      <p style="color:#475569; font-size:16px; line-height:1.6; margin:0 0 25px 0;">
        Tu solicitud de inscripci&oacute;n al curso
        <strong style="color:#4f46e5;">&ldquo;{course.title}&rdquo;</strong>
        ha sido <strong style="color:#059669;">APROBADA</strong>.
        &iexcl;Bienvenido a <strong>LearnHub</strong>!
      </p>

      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; margin:0 0 20px 0;">
        <tr>
          <td style="background:linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius:12px 12px 0 0; padding:12px 20px;">
            <p style="color:#ffffff; font-size:14px; font-weight:700; margin:0; letter-spacing:1px; text-transform:uppercase;">Detalles del Curso</p>
          </td>
        </tr>
        <tr>
          <td style="padding:20px;">
            <p style="color:#1e293b; font-size:16px; font-weight:700; margin:0; word-break:break-word;">{course.title}</p>
          </td>
        </tr>
      </table>

      {_build_credentials_box(username, password)}

      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center" style="padding:25px 0;">
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="background:linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius:8px; text-align:center;">
                  <a href="http://127.0.0.1:8000/estudiante/login/" style="display:inline-block; padding:14px 40px; color:#ffffff; font-size:16px; font-weight:700; text-decoration:none; border-radius:8px;">Acceder a la Plataforma</a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <p style="color:#475569; font-size:15px; line-height:1.6; margin:0 0 10px 0;">
        Una vez dentro, podr&aacute;s:
      </p>
      <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 20px 0;">
        <tr>
          <td style="padding:5px 0 5px 20px; color:#475569; font-size:14px;">&#10003; Acceder a tus cursos matriculados</td>
        </tr>
        <tr>
          <td style="padding:5px 0 5px 20px; color:#475569; font-size:14px;">&#10003; Ver tu progreso y calificaciones</td>
        </tr>
        <tr>
          <td style="padding:5px 0 5px 20px; color:#475569; font-size:14px;">&#10003; Participar en evaluaciones y ex&aacute;menes</td>
        </tr>
        <tr>
          <td style="padding:5px 0 5px 20px; color:#475569; font-size:14px;">&#10003; Acceder a recursos y materiales de estudio</td>
        </tr>
      </table>

      <hr style="border:none; border-top:1px solid #e2e8f0; margin:25px 0;">

      <p style="color:#64748b; font-size:14px; line-height:1.5; margin:0 0 5px 0;">
        Si tienes alguna duda, contacta al administrador.
      </p>
      <p style="color:#475569; font-size:15px; line-height:1.5; margin:0;">
        &iexcl;&Eacute;xito en tu aprendizaje!
      </p>
      <p style="color:#1e293b; font-size:15px; font-weight:600; margin:5px 0 0 0;">
        Equipo LearnHub
      </p>"""

    sender = getattr(settings, 'DEFAULT_FROM_EMAIL', 'LearnHub <noreply@learnhub.com>')
    html_body = _build_html_template('&iexcl;Inscripci&oacute;n Aprobada!', content_html)

    if getattr(settings, 'GMAIL_API_ENABLED', False):
        service = _get_gmail_service()
        if service:
            return _send_via_gmail_api(service, sender, student.email, subject, text_body, html_body)

    logger.warning("Gmail API no disponible, intentando con método alternativo")
    return False


def send_enrollment_rejected_email(enrollment):
    """
    Envía un email al estudiante cuando su inscripción a un curso es rechazada.
    """
    student = enrollment.student
    course = enrollment.course

    subject = f'Inscripción rechazada al curso: {course.title}'

    text_body = f"""Hola {student.name},

Lamentamos informarte que tu solicitud de inscripción al curso "{course.title}" ha sido RECHAZADA.

Información:
----------------------------------------------
Curso: {course.title}
----------------------------------------------

Por favor, contacta al administrador para más información.

Equipo LearnHub"""

    content_html = f"""
      <p style="color:#475569; font-size:16px; line-height:1.6; margin:0 0 20px 0;">
        Hola <strong style="color:#1e293b;">{student.name}</strong>,
      </p>

      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#fef2f2; border:1px solid #fecaca; border-radius:12px; margin:0 0 25px 0;">
        <tr>
          <td style="padding:20px; text-align:center;">
            <p style="color:#dc2626; font-size:18px; font-weight:700; margin:0 0 8px 0;">Solicitud Rechazada</p>
            <p style="color:#991b1b; font-size:15px; line-height:1.5; margin:0;">
              Lamentamos informarte que tu solicitud de inscripci&oacute;n al curso
              <strong>&ldquo;{course.title}&rdquo;</strong> no ha sido aprobada.
            </p>
          </td>
        </tr>
      </table>

      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; margin:0 0 25px 0;">
        <tr>
          <td style="background:linear-gradient(135deg, #64748b 0%, #475569 100%); border-radius:12px 12px 0 0; padding:12px 20px;">
            <p style="color:#ffffff; font-size:14px; font-weight:700; margin:0; letter-spacing:1px; text-transform:uppercase;">Informaci&oacute;n del Curso</p>
          </td>
        </tr>
        <tr>
          <td style="padding:20px;">
            <p style="color:#1e293b; font-size:16px; font-weight:700; margin:0 0 4px 0; word-break:break-word;">{course.title}</p>
          </td>
        </tr>
      </table>

      <hr style="border:none; border-top:1px solid #e2e8f0; margin:25px 0;">

      <p style="color:#64748b; font-size:14px; line-height:1.5; margin:0 0 5px 0;">
        Por favor, contacta al administrador para m&aacute;s informaci&oacute;n sobre esta decisi&oacute;n.
      </p>
      <p style="color:#475569; font-size:15px; line-height:1.5; margin:0;">
        Quedamos a tu disposici&oacute;n.
      </p>
      <p style="color:#1e293b; font-size:15px; font-weight:600; margin:5px 0 0 0;">
        Equipo LearnHub
      </p>"""

    sender = getattr(settings, 'DEFAULT_FROM_EMAIL', 'LearnHub <noreply@learnhub.com>')
    html_body = _build_html_template('Inscripci&oacute;n Rechazada', content_html)

    if getattr(settings, 'GMAIL_API_ENABLED', False):
        service = _get_gmail_service()
        if service:
            return _send_via_gmail_api(service, sender, student.email, subject, text_body, html_body)

    logger.warning("Gmail API no disponible, intentando con método alternativo")
    return False