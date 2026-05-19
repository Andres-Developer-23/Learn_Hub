from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.template import loader
from email_service.services import send_password_reset_email
import logging

logger = logging.getLogger(__name__)


class GmailAPIPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email,
                  html_email_template_name=None):
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        logger.info(f"Enviando correo de recuperación a {to_email} via Gmail API")
        sent = send_password_reset_email(subject, body, to_email)
        if not sent:
            logger.error(f"Fallo al enviar correo de recuperación a {to_email}")
        return sent


class GmailAPIPasswordResetView(PasswordResetView):
    form_class = GmailAPIPasswordResetForm
