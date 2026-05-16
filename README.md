# Learn Hub

Plataforma educativa integral para la gestión de cursos, estudiantes y evaluaciones, construida con Django. Ofrece un panel administrativo completo, un portal interactivo para estudiantes y una terminal Python integrada en el navegador.

## Características

- **Catálogo público de cursos** — Landing page con listado, detalle y previsualización de cursos
- **Inscripción con flujo de aprobación** — Los administradores revisan y aceptan/rechazan solicitudes
- **Panel administrativo** — Dashboard con estadísticas, gestión de cursos (CRUD), estudiantes y notificaciones
- **Portal de estudiantes** — Dashboard personalizado, examenes por curso, actualización de perfil
- **Terminal Python interactiva** — Consola Python en el navegador, integrada con el portal
- **Sistema de notificaciones** — Centro de notificaciones para administradores
- **Integración con Gmail API** — Envío automatizado de correos mediante OAuth2
- **Exportación a CSV** — Descarga de datos de estudiantes

## Stack Tecnológico

| Tecnología | Versión |
|---|---|
| Django | 6.0.5 |
| Python | 3.x |
| SQLite | — |
| Gmail API | Google OAuth2 |
| HTML5 / CSS3 / JavaScript | — |

## Estructura del Proyecto

```
Learn_Hub/
├── ai_project/              # Configuración principal de Django
├── email_service/           # Servicio de correo (Gmail API OAuth2)
├── enrollment/              # Inscripciones, cursos y contenidos
│   ├── models.py            # Student, Course, Exam, Content, EnrollmentRequest
│   ├── views.py             # Landing, detalle de curso, preview
│   └── templatetags/        # Tags personalizados para templates
├── panel/                   # Panel de administración
│   ├── views.py             # Dashboard, CRUD de cursos y estudiantes
│   └── templates/panel/     # Templates del panel
├── student_portal/          # Portal de estudiantes
│   ├── views.py             # Dashboard, exámenes, perfil
│   └── templates/student_portal/
├── terminal/                # Terminal Python interactiva en el navegador
├── notificaciones/          # Sistema de notificaciones
├── media/                   # Archivos subidos (imágenes de perfil, etc.)
├── manage.py                # CLI de Django
└── requirements.txt         # Dependencias del proyecto
```

## Instalación

### Requisitos previos

- Python 3.10 o superior
- pip
- Git

### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/Andres-Developer-23/Learn_Hub.git
cd Learn_Hub

# Crear y activar entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor de desarrollo
python manage.py runserver
```

### Configuración de Gmail API (opcional)

1. Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitar la Gmail API
3. Descargar las credenciales OAuth2 y guardarlas como `client_secret.json`
4. Ejecutar el servidor — el token se generará automáticamente al enviar el primer correo

## Rutas del Sistema

### Públicas
| Ruta | Descripción |
|---|---|
| `/` | Catálogo de cursos |
| `/curso/<id>/` | Detalle y previsualización del curso |

### Panel de Administración
| Ruta | Descripción |
|---|---|
| `/panel/login/` | Inicio de sesión |
| `/panel/` | Dashboard con estadísticas |
| `/panel/cursos/` | Gestión de cursos |
| `/panel/estudiantes/` | Gestión de estudiantes |
| `/panel/notificaciones/` | Centro de notificaciones |

### Portal de Estudiantes
| Ruta | Descripción |
|---|---|
| `/estudiante/login/` | Inicio de sesión |
| `/estudiante/` | Dashboard del estudiante |
| `/estudiante/examen/<id>/` | Evaluación del curso |
| `/estudiante/python/` | Terminal Python interactiva |

### Terminal
| Ruta | Descripción |
|---|---|
| `/terminal/` | Consola Python en el navegador |

## Modelos Principales

### Student
| Campo | Tipo | Descripción |
|---|---|---|
| user | OneToOneField | Usuario de Django asociado |
| name | CharField | Nombre completo |
| email | EmailField | Correo electrónico (único) |
| level | CharField | Nivel: principiante, intermedio, avanzado |
| status | CharField | Estado: pending, accepted, rejected |
| created_at | DateTimeField | Fecha de registro |

### Course
| Campo | Tipo | Descripción |
|---|---|---|
| title | CharField | Título del curso |
| description | TextField | Descripción |
| level | CharField | Nivel del curso |
| image | ImageField | Imagen de portada |
| instructor | CharField | Nombre del instructor |
| created_at | DateTimeField | Fecha de creación |

### Exam
| Campo | Tipo | Descripción |
|---|---|---|
| course | ForeignKey | Curso asociado |
| title | CharField | Título del examen |
| questions | JSONField | Preguntas y respuestas |
| passing_score | IntegerField | Puntaje mínimo para aprobar |
| time_limit | IntegerField | Límite de tiempo en minutos |

## Flujo de Inscripción

1. El estudiante se registra a través del formulario público
2. La solicitud queda en estado **pendiente**
3. El administrador revisa la solicitud desde el panel
4. Al aceptar, se crea automáticamente un usuario de Django
5. El estudiante recibe sus credenciales y accede al portal

## Licencia

Este proyecto es de uso educativo y privado.
