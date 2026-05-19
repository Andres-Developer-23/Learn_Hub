from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import csv, json
from enrollment.models import Student, Course, CourseContent, Exam, Question, QuestionOption, CourseFile, EnrollmentRequest, Instructor
from notificaciones.models import Notification


# ─── Auth ─────────────────────────────────────────────────────────────────────

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Credenciales incorrectas o sin permisos de administrador.')
    return render(request, 'panel/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required(login_url='admin_login')
@never_cache
def dashboard(request):
    total    = Student.objects.count()
    by_level = Student.objects.values('level').annotate(total=Count('level'))
    level_data = {i['level']: i['total'] for i in by_level}

    week_ago = timezone.now() - timedelta(days=7)
    recent   = Student.objects.filter(created_at__gte=week_ago).count()

    pending  = Student.objects.filter(status='pending').count()
    accepted = Student.objects.filter(status='accepted').count()
    rejected = Student.objects.filter(status='rejected').count()

    pending_enrollments = EnrollmentRequest.objects.filter(status='pending').count()
    unread_notifications = Notification.objects.filter(is_read=False).count()
    total_pending = pending + pending_enrollments + unread_notifications

    students_qs    = Student.objects.select_related('user').all().order_by('-created_at')
    paginator = Paginator(students_qs, 20)
    page_num = request.GET.get('page')
    students = paginator.get_page(page_num)

    context = {
        'total': total,
        'principiante': level_data.get('principiante', 0),
        'intermedio':   level_data.get('intermedio', 0),
        'avanzado':     level_data.get('avanzado', 0),
        'recent':   recent,
        'pending':  pending,
        'accepted': accepted,
        'rejected': rejected,
        'students': students,
        'total_pending': total_pending,
    }
    return render(request, 'panel/dashboard.html', context)


# ─── Student CRUD ─────────────────────────────────────────────────────────────

@login_required(login_url='admin_login')
@never_cache
def student_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Student, pk=pk).delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('admin_dashboard')
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='admin_login')
@never_cache
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'GET':
        return render(request, 'panel/student_edit.html', {'student': student})
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        new_email = data.get('email', student.email)
        
        if new_email != student.email and Student.objects.filter(email=new_email).exists():
            error_msg = 'El correo electrónico ya está en uso.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': error_msg})
            messages.error(request, error_msg)
            return redirect('student_edit', pk=pk)
        
        student.name  = data.get('name',  student.name)
        student.email = new_email
        student.level = data.get('level', student.level)
        student.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('admin_dashboard')
    return JsonResponse({'status': 'error'}, status=405)


# ─── Export ───────────────────────────────────────────────────────────────────

@login_required(login_url='admin_login')
@never_cache
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="inscritos.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Correo', 'Nivel', 'Estado', 'Usuario', 'Fecha'])
    for s in Student.objects.all().order_by('created_at'):
        writer.writerow([
            s.pk, s.name, s.email,
            s.get_level_display(), s.get_status_display(),
            s.user.username if s.user else '—',
            s.created_at.strftime('%d/%m/%Y %H:%M'),
        ])
    return response


# ─── Courses ──────────────────────────────────────────────────────────────────

@login_required(login_url='admin_login')
@never_cache
def course_list(request):
    courses = Course.objects.all().order_by('order')
    return render(request, 'panel/course_list.html', {'courses': courses})


@login_required(login_url='admin_login')
@never_cache
def course_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        icon = request.POST.get('icon', '📚').strip()
        duration = request.POST.get('duration', '16 semanas').strip()
        level = request.POST.get('level', 'principiante')
        order = int(request.POST.get('order', 0))
        is_active = request.POST.get('is_active') == 'on'
        if title:
            course = Course.objects.create(
                title=title, description=description, icon=icon,
                duration=duration, level=level, order=order, is_active=is_active
            )
            if request.FILES.get('image'):
                course.image = request.FILES['image']
                course.save()
            messages.success(request, 'Curso creado correctamente.')
            return redirect('course_list')
        messages.error(request, 'El título es obligatorio.')
    return render(request, 'panel/course_form.html', {'course': None})


@login_required(login_url='admin_login')
@never_cache
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.title = request.POST.get('title', course.title).strip()
        course.description = request.POST.get('description', course.description).strip()
        course.icon = request.POST.get('icon', course.icon).strip()
        course.duration = request.POST.get('duration', course.duration).strip()
        course.level = request.POST.get('level', course.level)
        course.order = int(request.POST.get('order', course.order) or 0)
        course.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('image'):
            course.image = request.FILES['image']
        course.save()
        messages.success(request, 'Curso actualizado correctamente.')
        return redirect('course_list')
    return render(request, 'panel/course_form.html', {'course': course})


@login_required(login_url='admin_login')
@never_cache
def course_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Course, pk=pk).delete()
        messages.success(request, 'Curso eliminado.')
    return redirect('course_list')


@login_required(login_url='admin_login')
@never_cache
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    contents = course.contents.select_related('course').all()
    exams = course.exams.select_related('course').all()
    files = course.files.select_related('course').all()
    return render(request, 'panel/course_detail.html', {
        'course': course, 'contents': contents, 'exams': exams, 'files': files
    })


# ─── Course Content ───────────────────────────────────────────────────────────

@login_required(login_url='admin_login')
@never_cache
def content_create(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        section_type = request.POST.get('section_type')
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        order = request.POST.get('order', 0)
        uploaded_file = request.FILES.get('file')
        if title:
            obj = CourseContent.objects.create(
                course=course, section_type=section_type, title=title,
                content=content, order=order
            )
            if uploaded_file:
                obj.file = uploaded_file
                obj.save()
            messages.success(request, 'Contenido agregado.')
            return redirect('course_detail', pk=course.pk)
        messages.error(request, 'El título es obligatorio.')
    return render(request, 'panel/content_form.html', {'course': course})


@login_required(login_url='admin_login')
@never_cache
def content_delete(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(CourseContent, pk=pk)
        course_pk = obj.course.pk
        obj.delete()
        messages.success(request, 'Contenido eliminado.')
        return redirect('course_detail', pk=course_pk)
    return redirect('course_list')


# ─── Exams ────────────────────────────────────────────────────────────────────

@login_required(login_url='admin_login')
@never_cache
def exam_create(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        passing_score = request.POST.get('passing_score', 70)
        time_limit = request.POST.get('time_limit_minutes', 30)
        if title:
            exam = Exam.objects.create(
                course=course, title=title, description=description,
                passing_score=passing_score, time_limit_minutes=time_limit
            )
            # Save questions
            questions_text = request.POST.getlist('question_text[]')
            for qi, qt in enumerate(questions_text):
                if qt.strip():
                    q = Question.objects.create(exam=exam, text=qt.strip(), order=qi)
                    for oi in range(4):
                        opt_key = f'option_{qi}_{oi}'
                        opt_text = request.POST.get(opt_key, '').strip()
                        if opt_text:
                            is_correct = request.POST.get(f'correct_{qi}') == str(oi)
                            QuestionOption.objects.create(
                                question=q, text=opt_text,
                                is_correct=is_correct, order=oi
                            )
            messages.success(request, 'Examen creado.')
            return redirect('course_detail', pk=course.pk)
        messages.error(request, 'El título es obligatorio.')
    return render(request, 'panel/exam_form.html', {'course': course, 'exam': None})


@login_required(login_url='admin_login')
@never_cache
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.title = request.POST.get('title', exam.title).strip()
        exam.description = request.POST.get('description', exam.description).strip()
        exam.passing_score = request.POST.get('passing_score', exam.passing_score)
        exam.time_limit_minutes = request.POST.get('time_limit_minutes', exam.time_limit_minutes)
        exam.save()

        existing = {q.pk for q in exam.questions.all()}
        submitted = set()
        questions_text = request.POST.getlist('question_text[]')
        for qi, qt in enumerate(questions_text):
            if qt.strip():
                qid = request.POST.get(f'question_id_{qi}')
                if qid and int(qid) in existing:
                    q = Question.objects.get(pk=int(qid))
                    q.text = qt.strip()
                    q.order = qi
                    q.save()
                    submitted.add(q.pk)
                else:
                    q = Question.objects.create(exam=exam, text=qt.strip(), order=qi)
                # Update options
                q.options.all().delete()
                for oi in range(4):
                    opt_key = f'option_{qi}_{oi}'
                    opt_text = request.POST.get(opt_key, '').strip()
                    if opt_text:
                        is_correct = request.POST.get(f'correct_{qi}') == str(oi)
                        QuestionOption.objects.create(
                            question=q, text=opt_text, is_correct=is_correct, order=oi
                        )
        # Remove deleted questions
        for qid in existing - submitted:
            Question.objects.filter(pk=qid).delete()

        messages.success(request, 'Examen actualizado.')
        return redirect('course_detail', pk=exam.course.pk)
    return render(request, 'panel/exam_form.html', {'course': exam.course, 'exam': exam})


@login_required(login_url='admin_login')
@never_cache
def exam_delete(request, pk):
    if request.method == 'POST':
        exam = get_object_or_404(Exam, pk=pk)
        course_pk = exam.course.pk
        exam.delete()
        messages.success(request, 'Examen eliminado.')
        return redirect('course_detail', pk=course_pk)
    return redirect('course_list')


# ─── Files ────────────────────────────────────────────────────────────────────

@login_required(login_url='admin_login')
@never_cache
def file_upload(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        uploaded_file = request.FILES.get('file')
        if title and uploaded_file:
            CourseFile.objects.create(course=course, title=title, file=uploaded_file)
            messages.success(request, 'Archivo subido.')
        else:
            messages.error(request, 'Título y archivo son obligatorios.')
        return redirect('course_detail', pk=course.pk)
    return redirect('course_detail', pk=course.pk)


@login_required(login_url='admin_login')
@never_cache
def file_delete(request, pk):
    if request.method == 'POST':
        cf = get_object_or_404(CourseFile, pk=pk)
        course_pk = cf.course.pk
        cf.delete()
        messages.success(request, 'Archivo eliminado.')
        return redirect('course_detail', pk=course_pk)
    return redirect('course_list')


@login_required(login_url='admin_login')
@never_cache
def notifications_view(request):
    pending_students = Student.objects.filter(status='pending').order_by('-created_at')
    pending_enrollments = EnrollmentRequest.objects.filter(status='pending').select_related('student', 'course').order_by('-created_at')
    unread_qs = Notification.objects.filter(is_read=False).select_related('student').order_by('-created_at')
    read_qs = Notification.objects.filter(is_read=True).select_related('student').order_by('-created_at')

    paginator = Paginator(unread_qs, 20)
    page_num = request.GET.get('page')
    unread_notifications = paginator.get_page(page_num)

    read_paginator = Paginator(read_qs, 20)
    read_page_num = request.GET.get('rpage')
    read_notifications = read_paginator.get_page(read_page_num)

    pending_students_count = Student.objects.filter(status='pending').count()
    pending_enrollments_count = pending_enrollments.count()
    total_unread = Notification.objects.filter(is_read=False).count()
    total_read = Notification.objects.filter(is_read=True).count()
    total_pending = pending_students_count + pending_enrollments_count + total_unread

    context = {
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
        'pending_students': pending_students,
        'pending_enrollments': pending_enrollments,
        'pending_students_count': pending_students_count,
        'pending_enrollments_count': pending_enrollments_count,
        'unread_notifications_count': total_unread,
        'read_notifications_count': total_read,
        'total_pending': total_pending,
    }
    return render(request, 'panel/notifications.html', context)


@login_required(login_url='admin_login')
@never_cache
def enrollment_accept(request, pk):
    if request.method == 'POST':
        try:
            from email_service.services import send_enrollment_accepted_email
        except ImportError:
            messages.error(request, 'Error: Servicio de email no disponible')
            return redirect('notifications_view')
        
        enrollment = get_object_or_404(EnrollmentRequest, pk=pk)
        enrollment.status = 'accepted'
        enrollment.save()
        enrollment.student.courses.add(enrollment.course)
        
        try:
            sent = send_enrollment_accepted_email(enrollment)
            if not sent:
                messages.warning(request, 'Inscripción aceptada pero el email no pudo ser enviado.')
        except Exception as e:
            messages.warning(request, 'Inscripción aceptada pero el email no pudo ser enviado.')
        
        Notification.objects.create(
            student=enrollment.student,
            title='Inscripción al curso aprobada',
            message=f'{enrollment.student.name}, tu solicitud para el curso "{enrollment.course.title}" ha sido aceptada.',
            notif_type='success'
        )
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('notifications_view')
    return JsonResponse({'status': 'error'}, status=405)


@login_required(login_url='admin_login')
@never_cache
def enrollment_reject(request, pk):
    if request.method == 'POST':
        try:
            from email_service.services import send_enrollment_rejected_email
        except ImportError:
            messages.error(request, 'Error: Servicio de email no disponible')
            return redirect('notifications_view')
        
        enrollment = get_object_or_404(EnrollmentRequest, pk=pk)
        enrollment.status = 'rejected'
        enrollment.save()
        
        try:
            send_enrollment_rejected_email(enrollment)
        except Exception as e:
            messages.warning(request, f'Inscripción rechazada pero el email no pudo ser enviado.')
        
        Notification.objects.create(
            student=enrollment.student,
            title='Inscripción al curso rechazada',
            message=f'{enrollment.student.name}, tu solicitud para el curso "{enrollment.course.title}" ha sido rechazada.',
            notif_type='error'
        )
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('notifications_view')
    return JsonResponse({'status': 'error'}, status=405)


# ─── Instructors ─────────────────────────────────────────────────────────────

@login_required(login_url='admin_login')
@never_cache
def instructor_list(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        bio = request.POST.get('bio', '').strip()
        password = request.POST.get('password', '').strip()

        if not name or not email:
            messages.error(request, 'Nombre y correo son obligatorios.')
            return redirect('instructor_list')

        if Instructor.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe un instructor con ese correo.')
            return redirect('instructor_list')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe un usuario con ese correo.')
            return redirect('instructor_list')

        if not password:
            password = User.objects.make_random_password(length=10)

        base_username = email.split('@')[0].lower().replace('.', '_')
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name.split()[0],
            last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
        )
        Instructor.objects.create(user=user, name=name, email=email, bio=bio)
        messages.success(request, f'Instructor creado. Usuario: {username}, Contraseña: {password}')
        return redirect('instructor_list')

    instructors = Instructor.objects.select_related('user').all().order_by('-created_at')
    return render(request, 'panel/instructor_list.html', {'instructors': instructors})


@login_required(login_url='admin_login')
@never_cache
def instructor_edit(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        bio = request.POST.get('bio', '').strip()
        new_password = request.POST.get('password', '').strip()

        if not name or not email:
            messages.error(request, 'Nombre y correo son obligatorios.')
            return redirect('instructor_edit', pk=pk)

        email_exists = Instructor.objects.filter(email=email).exclude(pk=pk).exists()
        if email_exists:
            messages.error(request, 'Ya existe otro instructor con ese correo.')
            return redirect('instructor_edit', pk=pk)

        instructor.name = name
        instructor.email = email
        instructor.bio = bio
        instructor.save()

        if instructor.user:
            if email != instructor.user.email:
                instructor.user.email = email
            instructor.user.first_name = name.split()[0]
            instructor.user.last_name = ' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
            if new_password:
                instructor.user.set_password(new_password)
            instructor.user.save()

        messages.success(request, 'Instructor actualizado.')
        return redirect('instructor_list')

    return render(request, 'panel/instructor_list.html', {
        'instructors': Instructor.objects.select_related('user').all().order_by('-created_at'),
        'edit_instructor': instructor,
    })


@login_required(login_url='admin_login')
@never_cache
def instructor_delete(request, pk):
    if request.method == 'POST':
        instructor = get_object_or_404(Instructor, pk=pk)
        user = instructor.user
        instructor.delete()
        if user:
            user.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        messages.success(request, 'Instructor eliminado.')
        return redirect('instructor_list')
    return JsonResponse({'status': 'error'}, status=405)
