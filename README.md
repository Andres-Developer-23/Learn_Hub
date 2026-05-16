# Learn Hub

Plataforma educativa desarrollada en Django para la gestión de cursos, estudiantes y evaluaciones. Incluye panel de administración, portal de estudiantes y terminal Python interactiva.

## Características

- Landing pública con catálogo de cursos
- Inscripción de estudiantes con aprobación manual
- Panel de administración con dashboard de estadísticas
- Gestión completa de cursos (CRUD) con niveles y contenidos
- Exámenes y evaluaciones por curso
- Portal de estudiantes con dashboard personalizado
- Terminal Python interactiva integrada en el navegador
- Sistema de notificaciones
- Integración con Gmail API para envío de correos
- Exportación de datos a CSV

## Estructura del Proyecto

```
Learn_Hub/
├── ai_project/              # Configuración principal de Django
├── email_service/           # Servicio de correo (Gmail API)
├── enrollment/              # App de inscripciones y cursos
│   ├── models.py            # Student, Course, Exam, Content, etc.
│   ├── views.py             # Landing, detalle de curso, preview
│   └── templatetags/        # Tags personalizados
├── panel/                   # Panel de administración
│   ├── views.py             # Dashboard, CRUD cursos, estudiantes
│   └── templates/           # Interfaz del panel
├── student_portal/          # Portal de estudiantes
│   ├── views.py             # Dashboard, exámenes, perfil
│   └── templates/           # Interfaz del portal
├── terminal/                # Terminal Python interactiva
├── notificaciones/          # Sistema de notificaciones
├── media/                   # Archivos subidos (imágenes, etc.)
├── manage.py                # Utilidad de Django
└── requirements.txt         # Dependencias
```

## Tecnologías

- **Framework**: Django 6.0.5
- **Base de datos**: SQLite (desarrollo)
- **Python**: 3.x
- **API de correo**: Gmail API (Google OAuth2)
- **Frontend**: HTML5, CSS3, JavaScript

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Andres-Developer-23/Learn_Hub.git
cd Learn_Hub
```

2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Iniciar servidor:
```bash
python manage.py runserver
```

## Uso del Sistema

### Landing y Cursos
- `/` - Catálogo público de cursos
- `/curso/<id>/` - Detalle y previsualización del curso

### Panel de Administración
- `/panel/login/` - Inicio de sesión
- `/panel/` - Dashboard con estadísticas
- `/panel/cursos/` - Gestión de cursos (crear, editar, eliminar)
- `/panel/estudiantes/` - Gestión de estudiantes
- `/panel/notificaciones/` - Centro de notificaciones

### Portal de Estudiantes
- `/estudiante/login/` - Inicio de sesión
- `/estudiante/` - Dashboard del estudiante
- `/estudiante/examen/<id>/` - Evaluación del curso
- `/estudiante/python/` - Terminal Python interactiva

### Terminal
- `/terminal/` - Terminal Python interactiva
