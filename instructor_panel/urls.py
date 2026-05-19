from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.instructor_login, name='instructor_login'),
    path('logout/', views.instructor_logout, name='instructor_logout'),
    path('', views.dashboard, name='instructor_dashboard'),
    path('curso/<int:pk>/', views.course_detail, name='instructor_course_detail'),
    path('curso/<int:pk>/contenido/nuevo/', views.content_create, name='instructor_content_create'),
    path('curso/contenido/<int:pk>/eliminar/', views.content_delete, name='instructor_content_delete'),
    path('curso/<int:pk>/examen/nuevo/', views.exam_create, name='instructor_exam_create'),
    path('curso/examen/<int:pk>/editar/', views.exam_edit, name='instructor_exam_edit'),
    path('curso/examen/<int:pk>/eliminar/', views.exam_delete, name='instructor_exam_delete'),
    path('curso/<int:pk>/archivos/subir/', views.file_upload, name='instructor_file_upload'),
    path('curso/archivos/<int:pk>/eliminar/', views.file_delete, name='instructor_file_delete'),
    path('curso/<int:pk>/estudiantes/', views.student_list, name='instructor_student_list'),
    path('perfil/editar/', views.profile_edit, name='instructor_profile_edit'),
]
