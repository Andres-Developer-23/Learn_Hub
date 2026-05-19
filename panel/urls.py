from django.urls import path
from . import views

urlpatterns = [
    path('login/',   views.admin_login,  name='admin_login'),
    path('logout/',  views.admin_logout, name='admin_logout'),
    path('',         views.dashboard,    name='admin_dashboard'),

    # Students
    path('estudiante/<int:pk>/editar/',   views.student_edit,   name='student_edit'),
    path('estudiante/<int:pk>/eliminar/', views.student_delete, name='student_delete'),

    # Courses
    path('cursos/',                         views.course_list,     name='course_list'),
    path('cursos/nuevo/',                   views.course_create,   name='course_create'),
    path('cursos/<int:pk>/editar/',         views.course_edit,     name='course_edit'),
    path('cursos/<int:pk>/eliminar/',       views.course_delete,   name='course_delete'),
    path('cursos/<int:pk>/',                views.course_detail,   name='course_detail'),

    # Course Content
    path('cursos/<int:pk>/contenido/nuevo/',       views.content_create,  name='content_create'),
    path('cursos/contenido/<int:pk>/eliminar/',    views.content_delete,  name='content_delete'),

    # Exams
    path('cursos/<int:pk>/examen/nuevo/',          views.exam_create,     name='exam_create'),
    path('cursos/examen/<int:pk>/editar/',         views.exam_edit,       name='exam_edit'),
    path('cursos/examen/<int:pk>/eliminar/',       views.exam_delete,     name='exam_delete'),

    # Files
    path('cursos/<int:pk>/archivos/subir/',        views.file_upload,     name='file_upload'),
    path('cursos/archivos/<int:pk>/eliminar/',     views.file_delete,     name='file_delete'),

    # Export
    path('exportar/csv/', views.export_csv, name='export_csv'),

    # Notifications & Requests
    path('notificaciones/', views.notifications_view, name='notifications_view'),
    path('inscripcion/<int:pk>/aceptar/', views.enrollment_accept, name='enrollment_accept'),
    path('inscripcion/<int:pk>/rechazar/', views.enrollment_reject, name='enrollment_reject'),

    # Instructors
    path('instructores/',                       views.instructor_list,   name='instructor_list'),
    path('instructores/<int:pk>/editar/',       views.instructor_edit,   name='instructor_edit'),
    path('instructores/<int:pk>/eliminar/',     views.instructor_delete, name='instructor_delete'),
]
