from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    bio = models.TextField(blank=True, default='')
    avatar_url = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('instructor_dashboard')


class Course(models.Model):
    LEVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio',   'Intermedio'),
        ('avanzado',     'Avanzado'),
    ]
    CATEGORY_CHOICES = [
        ('desarrollo-web',      'Desarrollo Web'),
        ('inteligencia-artificial', 'Inteligencia Artificial'),
        ('ciencia-de-datos',    'Ciencia de Datos'),
        ('desarrollo-movil',    'Desarrollo Móvil'),
        ('diseno-ux-ui',        'Diseño UX/UI'),
        ('cloud-devops',        'Cloud & DevOps'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='📚')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    duration = models.CharField(max_length=100, default='16 semanas')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='principiante')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True, verbose_name='Categoría')
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
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
    passing_score = models.PositiveIntegerField(default=70, help_text='Porcentaje mínimo para aprobar')
    time_limit_minutes = models.PositiveIntegerField(default=30, help_text='Tiempo límite en minutos')
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


class ContentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='content_progress')
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name='progress')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'content']
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.student.name} → {self.content.title}"


class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
