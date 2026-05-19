from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from enrollment.models import Student
from email_service.services import send_student_welcome_email
from django.http import JsonResponse
import secrets, string
import logging

from .models import Notification

logger = logging.getLogger(__name__)


def _unread_count():
    return Notification.objects.filter(is_read=False).count()


def _generate_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$"
    return ''.join(secrets.choice(chars) for _ in range(length))


def _create_student_user(student):
    """Create a Django User for the accepted student. Returns (username, raw_password)."""
    base = student.email.split('@')[0].lower().replace('.', '_')
    username = base
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1

    raw_password = _generate_password()
    user = User.objects.create_user(
        username=username,
        email=student.email,
        password=raw_password,
        first_name=student.name.split()[0],
        last_name=' '.join(student.name.split()[1:]) if len(student.name.split()) > 1 else '',
        is_staff=False,
        is_superuser=False,
    )
    student.user = user
    student.generated_password = raw_password
    student.save()
    return username, raw_password


@login_required(login_url='admin_login')
def notification_accept(request, pk):
    if request.method == 'POST':
        
        student = get_object_or_404(Student, pk=pk)
        student.status = 'accepted'

        Notification.objects.filter(student=student, is_read=False).update(is_read=True)

        credentials = None
        if not student.user:
            try:
                username, raw_pw = _create_student_user(student)
                credentials = {'username': username, 'password': raw_pw}
                send_student_welcome_email(student, username, raw_pw)
            except Exception as e:
                logger.error(f"Error al crear usuario o enviar email: {e}")
                student.save()
        else:
            student.save()

        msg = f'{student.name}, tu solicitud de inscripción ha sido aprobada. Ya puedes acceder a la plataforma.'
        if credentials:
            msg += f' Tus credenciales son: Usuario: {credentials["username"]}, Contraseña: {credentials["password"]}'
        Notification.objects.create(
            student=student, title='Inscripción aprobada',
            message=msg, notif_type='success'
        )

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'new_status': 'accepted',
                'unread': _unread_count(),
                'credentials': credentials,
            })
        return redirect('admin_dashboard')
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='admin_login')
def notification_reject(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=pk)
        student.status = 'rejected'
        Notification.objects.filter(student=student, is_read=False).update(is_read=True)
        student.save()
        Notification.objects.create(
            student=student, title='Inscripción rechazada',
            message=f'{student.name}, tu solicitud de inscripción ha sido rechazada. Contacta al administrador para más información.',
            notif_type='error'
        )

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'new_status': 'rejected', 'unread': _unread_count()})
        return redirect('admin_dashboard')
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='admin_login')
def notification_mark_read(request, pk):
    if request.method == 'POST':
        notif = get_object_or_404(Notification, pk=pk)
        notif.is_read = True
        notif.save()
        return JsonResponse({'status': 'success', 'unread': _unread_count()})
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='admin_login')
def notification_mark_unread(request, pk):
    if request.method == 'POST':
        notif = get_object_or_404(Notification, pk=pk)
        notif.is_read = False
        notif.save()
        return JsonResponse({'status': 'success', 'unread': _unread_count()})
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='admin_login')
def notifications_count(request):
    return JsonResponse({'unread': _unread_count()})
