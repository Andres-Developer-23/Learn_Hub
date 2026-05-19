from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from enrollment.models import Instructor, Course, CourseContent, Exam, Question, QuestionOption, CourseFile, Student, ContentProgress, ExamAttempt
from django.utils import timezone
from datetime import timedelta
import json


def instructor_login(request):
    if request.user.is_authenticated:
        try:
            if request.user.instructor:
                return redirect('instructor_dashboard')
        except Instructor.DoesNotExist:
            pass
        return redirect('admin_dashboard')

    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            try:
                instructor = user.instructor
                login(request, user)
                return redirect('instructor_dashboard')
            except Instructor.DoesNotExist:
                messages.error(request, 'El usuario no tiene perfil de instructor.')
        else:
            messages.error(request, 'Credenciales incorrectas.')
    return render(request, 'instructor_panel/login.html')


def instructor_logout(request):
    logout(request)
    return redirect('instructor_login')


@login_required(login_url='instructor_login')
@never_cache
def dashboard(request):
    try:
        instructor = request.user.instructor
    except Instructor.DoesNotExist:
        return redirect('admin_dashboard')

    courses = instructor.courses.all().order_by('order')
    total_students = Student.objects.filter(courses__in=courses).distinct().count()
    total_contents = CourseContent.objects.filter(course__in=courses).count()
    total_exams = Exam.objects.filter(course__in=courses).count()

    week_ago = timezone.now() - timedelta(days=7)
    recent_attempts = ExamAttempt.objects.filter(exam__course__in=courses, completed_at__gte=week_ago).count()

    context = {
        'instructor': instructor,
        'courses': courses,
        'total_courses': courses.count(),
        'total_students': total_students,
        'total_contents': total_contents,
        'total_exams': total_exams,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'instructor_panel/dashboard.html', context)


@login_required(login_url='instructor_login')
@never_cache
def course_detail(request, pk):
    try:
        instructor = request.user.instructor
    except Instructor.DoesNotExist:
        return redirect('admin_dashboard')

    course = get_object_or_404(Course, pk=pk, instructor=instructor)
    contents = course.contents.all().order_by('order')
    exams = course.exams.all()
    files = course.files.all()

    students = Student.objects.filter(courses=course)
    total_students = students.count()

    attempts = ExamAttempt.objects.filter(student__in=students, exam__course=course)
    avg_score = 0
    if attempts.exists():
        avg_score = int(sum(a.score / a.total * 100 for a in attempts if a.total > 0) / attempts.count())

    context = {
        'instructor': instructor,
        'course': course,
        'contents': contents,
        'exams': exams,
        'files': files,
        'total_students': total_students,
        'avg_score': avg_score,
    }
    return render(request, 'instructor_panel/course_detail.html', context)


@login_required(login_url='instructor_login')
@never_cache
def content_create(request, pk):
    try:
        instructor = request.user.instructor
    except Instructor.DoesNotExist:
        return redirect('admin_dashboard')
    course = get_object_or_404(Course, pk=pk, instructor=instructor)

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
            return redirect('instructor_course_detail', pk=course.pk)
        messages.error(request, 'El título es obligatorio.')
    return render(request, 'instructor_panel/content_form.html', {'course': course})


@login_required(login_url='instructor_login')
@never_cache
def content_delete(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(CourseContent, pk=pk)
        try:
            instructor = request.user.instructor
        except Instructor.DoesNotExist:
            return redirect('admin_dashboard')
        if obj.course.instructor != instructor:
            return redirect('instructor_dashboard')
        course_pk = obj.course.pk
        obj.delete()
        messages.success(request, 'Contenido eliminado.')
        return redirect('instructor_course_detail', pk=course_pk)
    return redirect('instructor_dashboard')


@login_required(login_url='instructor_login')
@never_cache
def exam_create(request, pk):
    try:
        instructor = request.user.instructor
    except Instructor.DoesNotExist:
        return redirect('admin_dashboard')
    course = get_object_or_404(Course, pk=pk, instructor=instructor)

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
            questions_text = request.POST.getlist('question_text[]')
            for qi, qt in enumerate(questions_text):
                if qt.strip():
                    q = Question.objects.create(exam=exam, text=qt.strip(), order=qi)
                    for oi in range(4):
                        opt_key = f'option_{qi}_{oi}'
                        opt_text = request.POST.get(opt_key, '').strip()
                        if opt_text:
                            is_correct = request.POST.get(f'correct_{qi}') == str(oi)
                            QuestionOption.objects.create(question=q, text=opt_text, is_correct=is_correct, order=oi)
            messages.success(request, 'Examen creado.')
            return redirect('instructor_course_detail', pk=course.pk)
        messages.error(request, 'El título es obligatorio.')
    return render(request, 'instructor_panel/exam_form.html', {'course': course, 'exam': None})


@login_required(login_url='instructor_login')
@never_cache
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    try:
        instructor = request.user.instructor
    except Instructor.DoesNotExist:
        return redirect('admin_dashboard')
    if exam.course.instructor != instructor:
        return redirect('instructor_dashboard')

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
                q.options.all().delete()
                for oi in range(4):
                    opt_key = f'option_{qi}_{oi}'
                    opt_text = request.POST.get(opt_key, '').strip()
                    if opt_text:
                        is_correct = request.POST.get(f'correct_{qi}') == str(oi)
                        QuestionOption.objects.create(question=q, text=opt_text, is_correct=is_correct, order=oi)
        for qid in existing - submitted:
            Question.objects.filter(pk=qid).delete()
        messages.success(request, 'Examen actualizado.')
        return redirect('instructor_course_detail', pk=exam.course.pk)
    return render(request, 'instructor_panel/exam_form.html', {'course': exam.course, 'exam': exam})


@login_required(login_url='instructor_login')
@never_cache
def exam_delete(request, pk):
    if request.method == 'POST':
        exam = get_object_or_404(Exam, pk=pk)
        try:
            instructor = request.user.instructor
        except Instructor.DoesNotExist:
            return redirect('admin_dashboard')
        if exam.course.instructor != instructor:
            return redirect('instructor_dashboard')
        course_pk = exam.course.pk
        exam.delete()
        messages.success(request, 'Examen eliminado.')
        return redirect('instructor_course_detail', pk=course_pk)
    return redirect('instructor_dashboard')


@login_required(login_url='instructor_login')
@never_cache
def file_upload(request, pk):
    try:
        instructor = request.user.instructor
    except Instructor.DoesNotExist:
        return redirect('admin_dashboard')
    course = get_object_or_404(Course, pk=pk, instructor=instructor)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        uploaded_file = request.FILES.get('file')
        if title and uploaded_file:
            CourseFile.objects.create(course=course, title=title, file=uploaded_file)
            messages.success(request, 'Archivo subido.')
        else:
            messages.error(request, 'Título y archivo son obligatorios.')
        return redirect('instructor_course_detail', pk=course.pk)
    return redirect('instructor_course_detail', pk=course.pk)


@login_required(login_url='instructor_login')
@never_cache
def file_delete(request, pk):
    if request.method == 'POST':
        cf = get_object_or_404(CourseFile, pk=pk)
        try:
            instructor = request.user.instructor
        except Instructor.DoesNotExist:
            return redirect('admin_dashboard')
        if cf.course.instructor != instructor:
            return redirect('instructor_dashboard')
        course_pk = cf.course.pk
        cf.delete()
        messages.success(request, 'Archivo eliminado.')
        return redirect('instructor_course_detail', pk=course_pk)
    return redirect('instructor_dashboard')


@login_required(login_url='instructor_login')
@never_cache
def student_list(request, pk):
    try:
        instructor = request.user.instructor
    except Instructor.DoesNotExist:
        return redirect('admin_dashboard')

    course = get_object_or_404(Course, pk=pk, instructor=instructor)
    students = Student.objects.filter(courses=course).order_by('-created_at')

    progress_data = []
    for s in students:
        total = course.contents.count()
        viewed = ContentProgress.objects.filter(student=s, content__course=course).count()
        pct = int((viewed / total * 100)) if total > 0 else 0
        passed_exams = ExamAttempt.objects.filter(student=s, exam__course=course, passed=True).count()
        total_exams = Exam.objects.filter(course=course).count()
        progress_data.append({
            'student': s,
            'progress_pct': pct,
            'viewed': viewed,
            'total_contents': total,
            'passed_exams': passed_exams,
            'total_exams': total_exams,
        })

    context = {
        'instructor': instructor,
        'course': course,
        'progress_data': progress_data,
    }
    return render(request, 'instructor_panel/student_list.html', context)


@login_required(login_url='instructor_login')
@never_cache
def profile_edit(request):
    try:
        instructor = request.user.instructor
    except Instructor.DoesNotExist:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        if request.content_type.startswith('multipart/form-data'):
            name = request.POST.get('name', '').strip()
            bio = request.POST.get('bio', '').strip()
            avatar_url = request.POST.get('avatar_url', '').strip()
            if name:
                instructor.name = name
                instructor.bio = bio
                instructor.avatar_url = avatar_url
                instructor.save()
                messages.success(request, 'Perfil actualizado.')
                return redirect('instructor_dashboard')
            messages.error(request, 'El nombre es obligatorio.')
    return render(request, 'instructor_panel/profile_edit.html', {'instructor': instructor})
