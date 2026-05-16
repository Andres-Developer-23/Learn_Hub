# Guía para Crear el Proyecto Django Desde Cero

Este documento contiene instrucciones paso a paso para recreate el proyecto "Sistema de Gestión de Inscripciones LearnHub" desde cero.

---

## 1. Preparación del Entorno

### 1.1 Crear directorio y entorno virtual

```bash
# Crear carpeta del proyecto
mkdir Laboratorio_Andres_Bravo
cd Laboratorio_Andres_Bravo

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 1.2 Instalar dependencias

Crear archivo `requirements.txt`:

```text
Django==6.0.5
google-api-python-client>=2.10.0
google-auth-httplib2>=0.1.0
google-auth-oauthlib>=0.5.0
Pillow>=10.0.0
```

Instalar:

```bash
pip install -r requirements.txt
```

---

## 2. Crear Proyecto Django

### 2.1 Crear el proyecto principal

```bash
python manage.py startproject ai_project .
```

### 2.2 Crear las aplicaciones (apps)

```bash
python manage.py startapp enrollment
python manage.py startapp panel
python manage.py startapp student_portal
python manage.py startapp terminal
python manage.py startapp notificaciones
python manage.py startapp email_service
```

---

## 3. Configuración Principal

### 3.1 Editar `ai_project/settings.py`

Agregar lo siguiente:

```python
# En INSTALLED_APPS agregar:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'enrollment',
    'panel',
    'student_portal',
    'terminal',
    'notificaciones',
    'email_service',
]

# Agregar al final:
LOGIN_URL = '/panel/login/'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'app_django@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_password'
DEFAULT_FROM_EMAIL = 'LearnHub <app_django@gmail.com>'
EMAIL_TIMEOUT = 30

# Gmail API Configuration
GMAIL_API_ENABLED = True
GMAIL_API_CREDENTIALS_FILE = BASE_DIR / 'client_secret_xxx.apps.googleusercontent.com.json'
GMAIL_API_TOKEN_FILE = BASE_DIR / 'token.json'
GMAIL_API_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
```

### 3.2 Editar `ai_project/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('enrollment.urls')),
    path('panel/', include('panel.urls')),
    path('estudiante/', include('student_portal.urls')),
    path('estudiantes/', include('student_portal.urls')),
    path('terminal/', include('terminal.urls')),
    path('notificaciones/', include('notificaciones.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 4. App: enrollment

### 4.1 Editar `enrollment/models.py`

```python
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    LEVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio',   'Intermedio'),
        ('avanzado',     'Avanzado'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='📚')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    duration = models.CharField(max_length=100, default='16 semanas')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='principiante')
    instructor_name = models.CharField(max_length=150, default='Instructor')
    instructor_bio = models.TextField(blank=True, default='')
    instructor_avatar_url = models.CharField(max_length=500, blank=True, default='')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Student(models.Model):
    LEVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio',   'Intermedio'),
        ('avanzado',     'Avanzado'),
    ]
    STATUS_CHOICES = [
        ('pending',  'Pendiente'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado'),
    ]

    user       = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='student')
    generated_password = models.CharField(max_length=50, blank=True, null=True)
    name       = models.CharField(max_length=150)
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=20, blank=True, null=True)
    address    = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='default.png')
    level      = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    courses    = models.ManyToManyField(Course, blank=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


class CourseContent(models.Model):
    SECTION_TYPES = [
        ('explicacion', 'Explicación'),
        ('ejemplo', 'Ejemplo'),
        ('demo', 'Demo'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='course_demos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['course', 'order']

    def __str__(self):
        return f"{self.get_section_type_display()}: {self.title}"


class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    passing_score = models.PositiveIntegerField(default=70)
    time_limit_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['course', '-created_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Pregunta')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['exam', 'order']

    def __str__(self):
        return self.text[:60]


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255, verbose_name='Opción')
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['question', 'order']

    def __str__(self):
        return self.text[:40]


class ExamAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.student.name} - {self.exam.title} ({self.score}/{self.total})"


class EnrollmentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pendiente'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado'),
    ]
    student  = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollment_requests')
    course   = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_requests')
    status   = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.name} → {self.course.title} ({self.get_status_display()})"


class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
```

### 4.2 Editar `enrollment/views.py`

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Student, Course, CourseContent, Exam, CourseFile, Question
from notificaciones.models import Notification
import json


def course_detail(request, course_id):
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
                student, created = Student.objects.update_or_create(
                    email=email,
                    defaults={'name': name, 'level': level, 'status': 'pending'}
                )
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

    return render(request, 'enrollment/index.html', {
        'courses': courses,
        'featured_courses': featured_courses
    })
```

### 4.3 Editar `enrollment/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('course/<int:course_id>/', views.course_detail, name='enrollment_course_detail'),
    path('api/course/<int:course_id>/', views.course_detail_api, name='course_detail_api'),
]
```

### 4.4 Crear directorio de templates

Crear carpeta: `enrollment/templates/enrollment/`

#### `enrollment/templates/enrollment/index.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LearnHub - Plataforma de Aprendizaje</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f5f5f5; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; }
        .container { max-width: 1200px; margin: 0 auto; }
        .hero { text-align: center; padding: 3rem 0; }
        .hero h1 { font-size: 2.5rem; margin-bottom: 1rem; }
        .hero p { font-size: 1.2rem; opacity: 0.9; }
        .enroll-form { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); max-width: 600px; margin: 2rem auto; }
        .enroll-form h2 { color: #333; margin-bottom: 1.5rem; }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; color: #555; }
        .form-group input, .form-group select { width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px; }
        .btn { background: #667eea; color: white; padding: 1rem 2rem; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 1rem; }
        .btn:hover { background: #5568d3; }
        .courses-section { padding: 3rem 0; }
        .courses-section h2 { text-align: center; margin-bottom: 2rem; color: #333; }
        .courses-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; }
        .course-card { background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.1); transition: transform 0.3s; }
        .course-card:hover { transform: translateY(-5px); }
        .course-icon { font-size: 4rem; text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .course-info { padding: 1.5rem; }
        .course-info h3 { color: #333; margin-bottom: 0.5rem; }
        .course-info p { color: #666; font-size: 0.9rem; }
        .course-meta { display: flex; gap: 1rem; margin-top: 1rem; font-size: 0.8rem; color: #888; }
        .message { padding: 1rem; border-radius: 5px; margin-bottom: 1rem; display: none; }
        .message.success { background: #d4edda; color: #155724; }
        .message.error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="hero">
                <h1>LearnHub - Transforma tu Futuro</h1>
                <p>Únete a nuestra plataforma de aprendizaje online y desarrolla nuevas habilidades</p>
            </div>
        </div>
    </header>

    <div class="container">
        <div class="enroll-form">
            <h2>Inscríbete Ahora</h2>
            <div id="message" class="message"></div>
            <form id="enrollmentForm">
                <div class="form-group">
                    <label for="name">Nombre Completo</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">Correo Electrónico</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="level">Nivel de Conocimiento</label>
                    <select id="level" name="level" required>
                        <option value="">Selecciona un nivel</option>
                        <option value="principiante">Principiante</option>
                        <option value="intermedio">Intermedio</option>
                        <option value="avanzado">Avanzado</option>
                    </select>
                </div>
                <button type="submit" class="btn">Enviar Solicitud</button>
            </form>
        </div>

        <section class="courses-section">
            <h2>Nuestros Cursos</h2>
            <div class="courses-grid">
                {% for course in courses %}
                <div class="course-card">
                    <div class="course-icon">{{ course.icon }}</div>
                    <div class="course-info">
                        <h3>{{ course.title }}</h3>
                        <p>{{ course.description }}</p>
                        <div class="course-meta">
                            <span>{{ course.get_level_display }}</span>
                            <span>{{ course.duration }}</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
    </div>

    <script>
        document.getElementById('enrollmentForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('{% url "index" %}', {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': '{{ csrf_token }}' }
            })
            .then(response => response.json())
            .then(data => {
                const msgEl = document.getElementById('message');
                msgEl.style.display = 'block';
                if (data.status === 'success') {
                    msgEl.className = 'message success';
                    msgEl.textContent = data.message;
                    this.reset();
                } else {
                    msgEl.className = 'message error';
                    msgEl.textContent = data.message;
                }
            });
        });
    </script>
</body>
</html>
```

(El resto de templates se encuentran en la carpeta del proyecto original)

---

## 5. App: panel (Administración)

### 5.1 Editar `panel/views.py`

Contiene funciones para:
- `admin_login`: Login de administrador
- `admin_logout`: Logout
- `dashboard`: Panel principal con estadísticas
- `student_delete`: Eliminar estudiante
- `student_edit`: Editar estudiante
- `export_csv`: Exportar a CSV
- `course_list`, `course_create`, `course_edit`, `course_delete`, `course_detail`: Gestión de cursos
- `content_create`, `content_delete`: Gestión de contenidos
- `exam_create`, `exam_edit`, `exam_delete`: Gestión de exámenes
- `file_upload`, `file_delete`: Gestión de archivos
- `notifications_view`: Ver notificaciones
- `enrollment_accept`, `enrollment_reject`: Aceptar/rechazar inscripciones

### 5.2 Editar `panel/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/',   views.admin_login,  name='admin_login'),
    path('logout/',  views.admin_logout, name='admin_logout'),
    path('',         views.dashboard,    name='admin_dashboard'),
    path('estudiante/<int:pk>/editar/',   views.student_edit,   name='student_edit'),
    path('estudiante/<int:pk>/eliminar/', views.student_delete, name='student_delete'),
    path('cursos/',                         views.course_list,     name='course_list'),
    path('cursos/nuevo/',                   views.course_create,   name='course_create'),
    path('cursos/<int:pk>/editar/',         views.course_edit,     name='course_edit'),
    path('cursos/<int:pk>/eliminar/',       views.course_delete,   name='course_delete'),
    path('cursos/<int:pk>/',                views.course_detail,   name='course_detail'),
    path('cursos/<int:pk>/contenido/nuevo/',       views.content_create,  name='content_create'),
    path('cursos/contenido/<int:pk>/eliminar/',    views.content_delete,  name='content_delete'),
    path('cursos/<int:pk>/examen/nuevo/',          views.exam_create,     name='exam_create'),
    path('cursos/examen/<int:pk>/editar/',         views.exam_edit,       name='exam_edit'),
    path('cursos/examen/<int:pk>/eliminar/',       views.exam_delete,     name='exam_delete'),
    path('cursos/<int:pk>/archivos/subir/',        views.file_upload,     name='file_upload'),
    path('cursos/archivos/<int:pk>/eliminar/',     views.file_delete,     name='file_delete'),
    path('exportar/csv/', views.export_csv, name='export_csv'),
    path('notificaciones/', views.notifications_view, name='notifications_view'),
    path('inscripcion/<int:pk>/aceptar/', views.enrollment_accept, name='enrollment_accept'),
    path('inscripcion/<int:pk>/rechazar/', views.enrollment_reject, name='enrollment_reject'),
]
```

---

## 6. App: student_portal

### 6.1 Editar `student_portal/views.py`

Contiene funciones para:
- `student_login`, `student_logout`: Autenticación de estudiantes
- `student_dashboard`: Dashboard principal
- `student_update_profile`: Actualizar perfil
- `student_enroll_course`: Inscribirse a curso
- `student_change_password`: Cambiar contraseña
- `course_detail`: Ver detalle del curso
- `student_mark_read`, `student_mark_all_read`: Marcar notificaciones
- `take_exam`: Realizar examen
- `exam_result`: Ver resultado

### 6.2 Editar `student_portal/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/',            views.student_login,           name='student_login'),
    path('logout/',           views.student_logout,          name='student_logout'),
    path('',                  views.student_dashboard,       name='student_dashboard'),
    path('perfil/editar/',   views.student_update_profile,  name='student_update_profile'),
    path('perfil/password/', views.student_change_password, name='student_change_password'),
    path('inscribir/',       views.student_enroll_course,   name='student_enroll_course'),
    path('notificacion/<int:pk>/leer/',      views.student_mark_read,      name='student_mark_read'),
    path('notificaciones/leer-todas/',       views.student_mark_all_read,  name='student_mark_all_read'),
    path('notificaciones/contar/',           views.student_notifications_count, name='student_notifications_count'),
    path('curso/<int:pk>/',                  views.course_detail, name='student_course_detail'),
    path('curso/<int:pk>/examen/',           views.take_exam,     name='take_exam'),
    path('curso/<int:pk>/examen/<int:attempt_pk>/resultado/', views.exam_result, name='exam_result'),
]
```

---

## 7. App: terminal

### 7.1 Editar `terminal/views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from enrollment.models import Student, Course


@login_required(login_url='student_login')
def python_console(request, pk):
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

    return render(request, 'terminal/python_console.html', {
        'course': course,
        'student': student,
    })
```

### 7.2 Editar `terminal/urls.py`

```python
from django.urls import path
from . import views

app_name = 'terminal'

urlpatterns = [
    path('<int:pk>/', views.python_console, name='terminal_console'),
]
```

---

## 8. App: notificaciones

### 8.1 Editar `notificaciones/models.py`

```python
from django.db import models

class Notification(models.Model):
    NOTIF_TYPES = [
        ('info',    'Información'),
        ('success', 'Éxito'),
        ('warning', 'Advertencia'),
        ('error',   'Error'),
    ]
    student    = models.ForeignKey('enrollment.Student', on_delete=models.CASCADE, related_name='notifications')
    title      = models.CharField(max_length=200, default='Notificación')
    message    = models.TextField(blank=True, default='')
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='info')
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.student.name}"

    class Meta:
        ordering = ['-created_at']
        db_table = 'enrollment_notification'
```

### 8.2 Crear `notificaciones/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    # Las notificaciones se gestionan desde panel y student_portal
]
```

---

## 9. App: email_service

### 9.1 Editar `email_service/services.py`

Este archivo contiene las funciones para enviar emails via Gmail API:
- `send_student_welcome_email`: Email de bienvenida
- `send_enrollment_accepted_email`: Inscripción aceptada
- `send_enrollment_rejected_email`: Inscripción rechazada

### 9.2 Crear `email_service/__init__.py`

```python
```

### 9.3 Crear `email_service/apps.py`

```python
from django.apps import AppConfig

class EmailServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'email_service'
```

---

## 10. Migraciones y Base de Datos

### 10.1 Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 10.2 Crear superusuario

```bash
python manage.py createsuperuser
```

### 10.3 (Opcional) Crear cursos iniciales

Crear archivo `seeds.py` o ejecutarlo desde shell:

```bash
python manage.py shell
```

```python
from enrollment.models import Course

courses = [
    {'title': 'Python para Principiantes', 'description': 'Aprende Python desde cero', 'icon': '🐍', 'level': 'principiante', 'duration': '12 semanas'},
    {'title': 'Desarrollo Web con Django', 'description': 'Crea aplicaciones web con Django', 'icon': '🌐', 'level': 'intermedio', 'duration': '16 semanas'},
    {'title': 'Machine Learning con Python', 'description': 'Introducción al aprendizaje automático', 'icon': '🤖', 'level': 'avanzado', 'duration': '20 semanas'},
]

for c in courses:
    Course.objects.create(**c)
```

---

## 11. Archivos de Configuración Adicionales

### 11.1 Templates requeridos

Debes crear los siguientes templates (los tienes en el proyecto original):

**Enrollment:**
- `enrollment/templates/enrollment/index.html`
- `enrollment/templates/enrollment/course_detail.html`
- `enrollment/templates/enrollment/course_preview.html`

**Panel:**
- `panel/templates/panel/login.html`
- `panel/templates/panel/dashboard.html`
- `panel/templates/panel/student_edit.html`
- `panel/templates/panel/course_list.html`
- `panel/templates/panel/course_form.html`
- `panel/templates/panel/course_detail.html`
- `panel/templates/panel/content_form.html`
- `panel/templates/panel/exam_form.html`
- `panel/templates/panel/notifications.html`

**Student Portal:**
- `student_portal/templates/student_portal/login.html`
- `student_portal/templates/student_portal/dashboard.html`
- `student_portal/templates/student_portal/curso.html`
- `student_portal/templates/student_portal/examen.html`
- `student_portal/templates/student_portal/resultado.html`
- `student_portal/templates/student_portal/python_console.html`

**Terminal:**
- `terminal/templates/terminal/python_console.html`

---

## 12. Iniciar el Servidor

```bash
python manage.py runserver
```

Acceder a:
- Panel Admin: `http://127.0.0.1:8000/panel/login/`
- Portal Estudiantes: `http://127.0.0.1:8000/estudiante/login/`
- Página principal: `http://127.0.0.1:8000/`

---

## 13. Configuración de Gmail API (Opcional)

1. Ir a Google Cloud Console
2. Crear proyecto
3. Habilitar Gmail API
4. Crear credenciales OAuth2
5. Descargar `client_secret_xxx.json`
6. Generar token usando el script de inicialización

---

## Notas Importantes

1. El proyecto usa SQLite por defecto
2. Las imágenes se guardan en `media/`
3. El sistema automáticamente crea usuarios Django cuando se aceptan estudiantes
4. Los estudiantes solo pueden acceder a cursos en los que están inscritos
5. El panel admin solo es accesible para usuarios con `is_staff=True`