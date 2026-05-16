from django.urls import path
from . import views

app_name = 'terminal'

urlpatterns = [
    path('<int:pk>/', views.python_console, name='terminal_console'),
]
