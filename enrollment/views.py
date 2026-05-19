from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from .models import Student, Course, CourseContent, Exam, CourseFile, Question
from notificaciones.models import Notification
import json


def course_detail(request, course_id):
    """Show public preview for anonymous users, redirect enrolled students to portal."""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    if request.user.is_authenticated:
        try:
            student = request.user.student
            if course in student.courses.all():
                return redirect('student_course_detail', pk=course.id)
        except Student.DoesNotExist:
            pass

    contents = course.contents.all()
    exams = course.exams.all()
    files = course.files.all()
    questions_count = Question.objects.filter(exam__course=course).count()
    return render(request, 'enrollment/course_preview.html', {
        'course': course,
        'contents': contents,
        'exams': exams,
        'files': files,
        'questions_count': questions_count,
    })


def course_detail_api(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    contents = course.contents.all().values('section_type', 'title', 'content', 'order')
    exams = course.exams.all().values('id', 'title', 'passing_score', 'time_limit_minutes')
    return JsonResponse({
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'icon': course.icon,
        'duration': course.duration,
        'level': course.get_level_display(),
        'instructor_name': course.instructor_name,
        'instructor_bio': course.instructor_bio,
        'instructor_avatar_url': course.instructor_avatar_url,
        'contents': list(contents),
        'exams': list(exams),
        'exams_count': exams.count(),
    })


def index(request):
    courses = Course.objects.filter(is_active=True).order_by('order')
    
    category = request.GET.get('categoria')
    if category:
        courses = courses.filter(category=category)
    
    featured_courses = courses[:6]
    
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            name  = data.get('name', '').strip()
            email = data.get('email', '').strip()
            level = data.get('level', '').strip()

            if name and email and level:
                # Create or update, always reset to pending on new submission
                student, created = Student.objects.update_or_create(
                    email=email,
                    defaults={'name': name, 'level': level, 'status': 'pending'}
                )
                # Create notification
                Notification.objects.create(
                    student=student, title='Solicitud de inscripción',
                    message='Tu solicitud de inscripción ha sido recibida y está pendiente de revisión.',
                    notif_type='info'
                )
                return JsonResponse({
                    'status': 'success',
                    'message': '¡Solicitud enviada! El administrador revisará tu inscripción y recibirás una respuesta pronto.'
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Faltan datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    category_counts = dict(
        Course.objects.filter(is_active=True, category__isnull=False)
        .values('category').annotate(count=Count('id'))
        .values_list('category', 'count')
    )
    categories_meta = [
        {'slug': 'desarrollo-web', 'name': 'Desarrollo Web', 'count': category_counts.get('desarrollo-web', 0), 'icon': 'fa-code', 'color': 'linear-gradient(135deg, #60a5fa, #3b82f6)'},
        {'slug': 'inteligencia-artificial', 'name': 'Inteligencia Artificial', 'count': category_counts.get('inteligencia-artificial', 0), 'icon': 'fa-brain', 'color': 'linear-gradient(135deg, #34d399, #10b981)'},
        {'slug': 'ciencia-de-datos', 'name': 'Ciencia de Datos', 'count': category_counts.get('ciencia-de-datos', 0), 'icon': 'fa-database', 'color': 'linear-gradient(135deg, #a78bfa, #7c3aed)'},
        {'slug': 'desarrollo-movil', 'name': 'Desarrollo Móvil', 'count': category_counts.get('desarrollo-movil', 0), 'icon': 'fa-mobile-alt', 'color': 'linear-gradient(135deg, #fbbf24, #f59e0b)'},
        {'slug': 'diseno-ux-ui', 'name': 'Diseño UX/UI', 'count': category_counts.get('diseno-ux-ui', 0), 'icon': 'fa-palette', 'color': 'linear-gradient(135deg, #f472b6, #ec4899)'},
        {'slug': 'cloud-devops', 'name': 'Cloud & DevOps', 'count': category_counts.get('cloud-devops', 0), 'icon': 'fa-cloud', 'color': 'linear-gradient(135deg, #22d3ee, #06b6d4)'},
    ]

    return render(request, 'enrollment/index.html', {
        'courses': courses,
        'featured_courses': featured_courses,
        'categories_meta': categories_meta,
        'active_category': category,
    })
