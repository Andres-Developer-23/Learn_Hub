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
