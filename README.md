# Sistema de Gestión de Inscripciones

Plataforma web desarrollada en Django para la gestión de inscripciones de estudiantes, con panel de administración, portal de estudiantes y terminal interactiva.

## Características

- Formulario público de inscripción de estudiantes
- Panel de administración para gestionar solicitudes
- Portal de estudiantes
- Gestión de usuarios automática
- Exportación de datos a CSV
- Sistema de notificaciones
- Terminal Python interactiva
- Integración con Gmail API para envío de correos
- Console de Python integrado

## Estructura del Proyecto

```
Laboratorio_Andres_Bravo/
├── ai_project/          # Configuración principal de Django
│   ├── settings.py      # Configuración del proyecto
│   ├── urls.py          # Rutas principales
│   └── wsgi.py          # Punto de entrada WSGI
├── enrollment/          # App de inscripciones
│   ├── models.py        # Modelos: Student, Course, EnrollmentRequest
│   ├── views.py         # Vistas del formulario público
│   ├── urls.py          # Rutas de inscripción
│   └── migrations/     # Migraciones de base de datos
├── panel/               # Panel de administración
│   ├── views.py         # Vistas del dashboard y gestión
│   └── urls.py          # Rutas del panel admin
├── student_portal/      # Portal de estudiantes
│   ├── views.py         # Vistas del portal estudiantil
│   └── templates/      # Plantillas HTML
├── terminal/            # Terminal Python interactiva
│   ├── views.py         # Vistas de la terminal
│   └── urls.py          # Rutas de la terminal
├── notificaciones/      # Sistema de notificaciones
│   ├── models.py        # Modelos de notificaciones
│   └── views.py         # Vistas de notificaciones
├── email_service/       # Servicio de correo electrónico
├── db.sqlite3           # Base de datos SQLite
├── requirements.txt     # Dependencias del proyecto
└── manage.py            # Utilidad de Django
```

## Tecnologías

- **Framework**: Django 6.0.5
- **Base de datos**: SQLite
- **Python**: 3.x
- **API de correo**: Gmail API (Google OAuth2)
- **Frontend**: HTML5, CSS3, JavaScript

## Modelos de Datos

### Student
| Campo | Descripción |
|-------|-------------|
| user | Relación con usuario de Django (OneToOne) |
| name | Nombre completo del estudiante |
| email | Correo electrónico único |
| level | Nivel del estudiante (principiante, intermedio, avanzado) |
| status | Estado de la inscripción (pending, accepted, rejected) |
| created_at | Fecha de creación |
| updated_at | Fecha de última actualización |

### Notification
| Campo | Descripción |
|-------|-------------|
| student | Relación con el estudiante |
| is_read | Indica si la notificación ha sido leída |
| created_at | Fecha de creación |

## Rutas del Sistema

### Inscripción (Pública)
- `/` - Formulario de inscripción

### Panel de Administración
- `/panel/login/` - Inicio de sesión admin
- `/panel/` - Dashboard principal
- `/panel/logout/` - Cerrar sesión

### Portal de Estudiantes
- `/estudiante/login/` - Inicio de sesión estudiantes
- `/estudiante/` - Dashboard del estudiante
- `/estudiante/examen/` - Evaluación del curso
- `/estudiante/python/` - Console Python interactivo

### Terminal
- `/terminal/` - Terminal Python interactiva
- `/terminal/python/` - Console de Python

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd Laboratorio_Andres_Bravo
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar Gmail API (opcional):
   - Crear proyecto en Google Cloud Console
   - Habilitar Gmail API
   - Descargar archivo de credenciales OAuth2
   - Renombrar a `client_secret.json`
   - Ejecutar inicialización: el sistema generará el token automáticamente

3. Ejecutar migraciones:
```bash
python manage.py migrate
```

4. Crear superusuario (para acceso al panel admin):
```bash
python manage.py createsuperuser
```

5. Iniciar servidor:
```bash
python manage.py runserver
```

## Uso del Sistema

### Flujo de Inscripción
1. El estudiante accede a la página principal y completa el formulario
2. La solicitud queda en estado "pendiente"
3. El administrador revisa las solicitudes desde el panel
4. Al aceptar, se crea automáticamente un usuario Django para el estudiante

### Panel de Administración
- Ver estadísticas de inscripciones por nivel y estado
- Aceptar o rechazar solicitudes
- Editar información de estudiantes
- Exportar datos a CSV
- Ver notificaciones de nuevas inscripciones

### Portal de Estudiantes
- Los estudiantes aceptados pueden iniciar sesión
- Ver su estado de inscripción
- Actualizar perfil y contraseña
- Realizar evaluaciones/exámenes
- Acceder a terminal Python integrada

### Terminal Python
- Console interactivo de Python en el navegador
- Ejecutar código Python directamente desde la web
- Integración con el portal de estudiantes