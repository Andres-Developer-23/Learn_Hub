from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from enrollment.models import Student, Course, CourseContent, Exam, Question, QuestionOption, ExamAttempt, CourseFile, EnrollmentRequest, ContentProgress
from notificaciones.models import Notification
from email_service.certificate import generate_certificate
from email_service.services import send_certificate_email
from django.utils import timezone


def student_login(request):
    """Login page for accepted students."""
    # If already logged in as student (not staff), go to portal
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('student_dashboard')
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user and not user.is_staff:
            try:
                student = user.student
                if student.status == 'accepted':
                    login(request, user)
                    return redirect('student_dashboard')
                else:
                    messages.error(request, 'Tu inscripción aún no ha sido aprobada.')
            except Student.DoesNotExist:
                messages.error(request, 'No se encontró un perfil de estudiante para este usuario.')
        elif user and user.is_staff:
            messages.error(request, 'Los administradores deben ingresar por el panel de administración.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'student_portal/login.html')


def student_logout(request):
    logout(request)
    return redirect('student_login')


@login_required(login_url='student_login')
@never_cache
def student_dashboard(request):
    """Main student portal dashboard."""
    if request.user.is_staff:
        return redirect('admin_dashboard')
    try:
        student = request.user.student
    except Student.DoesNotExist:
        logout(request)
        return redirect('student_login')

    all_courses = Course.objects.filter(is_active=True)
    enrolled_courses = student.courses.all()
    notifications = student.notifications.all()[:10]
    unread_count = student.notifications.filter(is_read=False).count()

    progress_data = {}
    for course in enrolled_courses:
        total = course.contents.count()
        if total > 0:
            viewed = ContentProgress.objects.filter(student=student, content__course=course).count()
            progress_data[course.id] = {'viewed': viewed, 'total': total, 'pct': int((viewed / total * 100))}
        else:
            progress_data[course.id] = {'viewed': 0, 'total': 0, 'pct': 0}

    return render(request, 'student_portal/dashboard.html', {
        'student': student,
        'all_courses': all_courses,
        'enrolled_courses': enrolled_courses,
        'notifications': notifications,
        'unread_count': unread_count,
        'progress_data': progress_data,
    })


@login_required(login_url='student_login')
@never_cache
def student_update_profile(request):
    """Allow student to update their profile."""
    if request.method == 'POST':
        try:
            student = request.user.student

            if request.content_type.startswith('multipart/form-data'):
                name = request.POST.get('name', '').strip()
                phone = request.POST.get('phone', '').strip()
                address = request.POST.get('address', '').strip()
                profile_picture = request.FILES.get('profile_picture')

                if name:
                    student.name = name
                    request.user.first_name = name.split()[0]
                    request.user.last_name = ' '.join(name.split()[1:])
                    request.user.save()

                if phone is not None:
                    student.phone = phone
                if address is not None:
                    student.address = address
                if profile_picture:
                    student.profile_picture = profile_picture

                student.save()
                return JsonResponse({'status': 'success'})
            else:
                data = json.loads(request.body)
                name = data.get('name', '').strip()
                phone = data.get('phone', '').strip()
                address = data.get('address', '').strip()

                if name:
                    student.name = name
                    request.user.first_name = name.split()[0]
                    request.user.last_name = ' '.join(name.split()[1:])
                    request.user.save()

                if phone is not None:
                    student.phone = phone
                if address is not None:
                    student.address = address

                student.save()
                return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='student_login')
@never_cache
def student_enroll_course(request):
    """Request enrollment in a course (requires admin approval)."""
    if request.method == 'POST':
        try:
            student = request.user.student
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
            course_id = data.get('course_id')

            course = Course.objects.get(id=course_id)
            if course in student.courses.all():
                return JsonResponse({'status': 'info', 'message': 'Ya estás inscrito en este curso.'})

            # Check if already requested
            existing = EnrollmentRequest.objects.filter(student=student, course=course).first()
            if existing:
                if existing.status == 'pending':
                    return JsonResponse({'status': 'info', 'message': 'Ya tienes una solicitud pendiente para este curso.'})
                elif existing.status == 'rejected':
                    existing.status = 'pending'
                    existing.save()
                    return JsonResponse({'status': 'success', 'message': 'Solicitud enviada de nuevo. Espera la confirmación del administrador.'})
                else:
                    return JsonResponse({'status': 'info', 'message': 'Ya estás inscrito en este curso.'})

            EnrollmentRequest.objects.create(student=student, course=course)
            return JsonResponse({'status': 'success', 'message': 'Solicitud enviada. Espera la confirmación del administrador.'})
        except Course.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Curso no encontrado.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='student_login')
@never_cache
def student_change_password(request):
    """Allow student to change their password."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            current  = data.get('current_password', '')
            new_pw   = data.get('new_password', '')
            confirm  = data.get('confirm_password', '')

            if not request.user.check_password(current):
                return JsonResponse({'status': 'error', 'message': 'La contraseña actual es incorrecta.'}, status=400)
            if len(new_pw) < 6:
                return JsonResponse({'status': 'error', 'message': 'La nueva contraseña debe tener al menos 6 caracteres.'}, status=400)
            if new_pw != confirm:
                return JsonResponse({'status': 'error', 'message': 'Las contraseñas no coinciden.'}, status=400)

            request.user.set_password(new_pw)
            request.user.save()
            user = authenticate(request, username=request.user.username, password=new_pw)
            if user:
                login(request, user)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)


# ─── Course Detail ────────────────────────────────────────────────────────────

@login_required(login_url='student_login')
@never_cache
def course_detail(request, pk):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('student_login')

    course = get_object_or_404(Course, pk=pk, is_active=True)
    if course not in student.courses.all():
        messages.warning(request, 'Debes inscribirte al curso para acceder a su contenido.')
        return redirect('student_dashboard')

    tab = request.GET.get('tab', 'explicacion')
    contents = course.contents.filter(section_type=tab)
    all_contents = course.contents.all().order_by('order')

    exams = course.exams.all()
    attempts = ExamAttempt.objects.filter(student=student, exam__course=course)
    files = course.files.all()
    questions_count = Question.objects.filter(exam__course=course).count()

    viewed_ids = set(ContentProgress.objects.filter(
        student=student, content__course=course
    ).values_list('content_id', flat=True))

    total_contents = all_contents.count()
    viewed_count = len(viewed_ids)
    progress_pct = int((viewed_count / total_contents * 100)) if total_contents > 0 else 0

    context = {
        'course': course, 'student': student,
        'tab': tab, 'contents': contents, 'all_contents': all_contents,
        'exams': exams, 'attempts': attempts, 'files': files,
        'questions_count': questions_count,
        'viewed_ids': viewed_ids,
        'progress_pct': progress_pct,
        'viewed_count': viewed_count,
        'total_contents': total_contents,
    }
    return render(request, 'student_portal/curso.html', context)


@login_required(login_url='student_login')
@never_cache
def mark_content_viewed(request, pk):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=403)

    content = get_object_or_404(CourseContent, pk=pk)
    ContentProgress.objects.get_or_create(student=student, content=content)

    total = content.course.contents.count()
    viewed = ContentProgress.objects.filter(student=student, content__course=content.course).count()

    return JsonResponse({'status': 'success', 'viewed': viewed, 'total': total, 'progress': int((viewed / total * 100)) if total > 0 else 0})


# ─── Notifications ─────────────────────────────────────────────────────────────

@login_required(login_url='student_login')
@never_cache
def student_mark_read(request, pk):
    if request.method == 'POST':
        notif = get_object_or_404(Notification, pk=pk, student__user=request.user)
        notif.is_read = True
        notif.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='student_login')
@never_cache
def student_mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(student__user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='student_login')
@never_cache
def student_notifications_count(request):
    count = Notification.objects.filter(student__user=request.user, is_read=False).count()
    return JsonResponse({'count': count})


# ─── Take Exam ────────────────────────────────────────────────────────────────

@login_required(login_url='student_login')
@never_cache
def take_exam(request, pk):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('student_login')

    exam = get_object_or_404(Exam, pk=pk, course__is_active=True)
    questions = exam.questions.all()

    if request.method == 'POST':
        total = questions.count()
        score = 0
        for q in questions:
            selected = request.POST.get(f'q_{q.pk}')
            correct_opt = q.options.filter(is_correct=True).first()
            if correct_opt and selected == str(correct_opt.pk):
                score += 1

        passed = (score / total * 100) >= exam.passing_score if total > 0 else False
        attempt = ExamAttempt.objects.create(
            student=student, exam=exam,
            score=score, total=total, passed=passed,
            completed_at=timezone.now()
        )
        return redirect('exam_result', pk=exam.pk, attempt_pk=attempt.pk)

    previous = ExamAttempt.objects.filter(student=student, exam=exam).order_by('-started_at').first()
    return render(request, 'student_portal/examen.html', {
        'exam': exam, 'questions': questions, 'previous': previous
    })


# ─── Certificate ─────────────────────────────────────────────────────────────

@login_required(login_url='student_login')
@never_cache
def send_certificate(request, pk):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Metodo no permitido.'}, status=405)

    if request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Acceso denegado.'}, status=403)

    try:
        student = request.user.student
    except Student.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Estudiante no encontrado.'}, status=404)

    course = get_object_or_404(Course, pk=pk, is_active=True)

    if course not in student.courses.all():
        return JsonResponse({'status': 'error', 'message': 'No estas inscrito en este curso.'}, status=403)

    total_contents = course.contents.count()
    viewed_contents = ContentProgress.objects.filter(student=student, content__course=course).count()
    all_content_viewed = total_contents > 0 and viewed_contents >= total_contents

    exams = course.exams.all()
    all_exams_passed = True
    if exams.exists():
        for exam in exams:
            passed_attempt = exam.attempts.filter(student=student, passed=True).exists()
            if not passed_attempt:
                all_exams_passed = False
                break
    else:
        all_exams_passed = True

    if not all_content_viewed or not all_exams_passed:
        missing = []
        if not all_content_viewed:
            missing.append(f"completar todo el contenido ({viewed_contents}/{total_contents})")
        if not all_exams_passed:
            missing.append("aprobar todos los examenes")
        msg = "Debes " + " y ".join(missing) + " para obtener tu certificado."
        return JsonResponse({'status': 'error', 'message': msg}, status=400)

    try:
        pdf_buffer = generate_certificate(student, course)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al generar el certificado: {str(e)}'}, status=500)

    try:
        sent = send_certificate_email(student, course, pdf_buffer)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al enviar el correo: {str(e)}'}, status=500)

    if sent:
        return JsonResponse({'status': 'success', 'message': 'Certificado enviado a tu correo electronico.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'No se pudo enviar el certificado. Intenta mas tarde.'}, status=500)


# ─── Exam Result ──────────────────────────────────────────────────────────────

@login_required(login_url='student_login')
@never_cache
def exam_result(request, pk, attempt_pk):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('student_login')

    exam = get_object_or_404(Exam, pk=pk)
    attempt = get_object_or_404(ExamAttempt, pk=attempt_pk, student=student, exam=exam)
    questions = exam.questions.all()

    return render(request, 'student_portal/resultado.html', {
        'exam': exam, 'attempt': attempt, 'questions': questions
    })
