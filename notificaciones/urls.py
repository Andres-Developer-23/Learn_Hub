from django.urls import path
from . import views

urlpatterns = [
    path('notificacion/<int:pk>/aceptar/',  views.notification_accept,      name='notification_accept'),
    path('notificacion/<int:pk>/rechazar/', views.notification_reject,       name='notification_reject'),
    path('notificacion/<int:pk>/leer/',     views.notification_mark_read,   name='notification_mark_read'),
    path('notificacion/<int:pk>/desleer/',  views.notification_mark_unread, name='notification_mark_unread'),
    path('contar/',                        views.notifications_count,     name='notifications_count'),
]
