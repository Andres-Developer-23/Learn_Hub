# Learn Hub

> Plataforma educativa integral para gestión de cursos, estudiantes y evaluaciones, construida con Django.

Plataforma LMS (Learning Management System) enfocada en cursos de IA/ML. Incluye panel administrativo, portal interactivo para estudiantes, terminal Python en el navegador, sistema de notificaciones, exámenes con seguimiento de progreso e integración con Gmail API.

🌐 **Demo en vivo**: [https://learn-hub-bhxvd.ondigitalocean.app](https://learn-hub-bhxvd.ondigitalocean.app)

---

## Características

- **Catálogo público de cursos** — Landing page con listado, filtro por categoría, detalle y previsualización de cursos
- **Inscripción con flujo de aprobación** — Registro público + solicitud de inscripción; administradores revisan y aceptan/rechazan
- **Panel administrativo** — Dashboard con estadísticas, gestión completa de cursos (CRUD), estudiantes, contenido, exámenes y archivos
- **Portal de estudiantes** — Dashboard personalizado con progreso por curso, exámenes, contenido interactivo y actualización de perfil
- **Terminal Python interactiva** — Consola Python en el navegador integrada con los cursos
- **Sistema de notificaciones** — Centro de notificaciones para administradores y estudiantes con tipos (info/success/warning/error)
- **Exámenes por curso** — Creación de exámenes con preguntas de opción múltiple, límite de tiempo, puntaje de aprobación e historial de intentos
- **Seguimiento de progreso** — Registro de contenido visto por estudiante con porcentaje de avance por curso
- **Integración con Gmail API** — Envío automatizado de correos (bienvenida, aceptación/rechazo, recuperación de contraseña) mediante OAuth2
- **Recuperación de contraseña** — Flujo completo de password reset vía Gmail API
- **Exportación a CSV** — Descarga de datos de estudiantes
- **Diseño responsive** — Interfaz adaptada para móviles, tablets y escritorio

---

## Stack Tecnológico

| Tecnología | Versión |
|---|---|
| **Django** | 6.0.5 |
| **Python** | 3.12 |
| **Base de datos** | PostgreSQL 17 (producción) / SQLite (desarrollo) |
| **Servidor** | Gunicorn |
| **Static files** | WhiteNoise |
| **Email** | Gmail API (Google OAuth2) |
| **Imágenes** | Pillow |
| **Frontend** | HTML5 / CSS3 / JavaScript |
| **Despliegue** | DigitalOcean App Platform |

---

## Estructura del Proyecto

```
Learn_Hub/
├── ai_project/                 # Configuración principal de Django
│   ├── settings.py             # Settings del proyecto
│   ├── urls.py                 # Enrutamiento raíz
│   ├── views.py                # Password reset vía Gmail API
│   ├── middleware.py           # NoCacheForAuthenticatedMiddleware
│   ├── wsgi.py                 # WSGI para producción
│   └── asgi.py                 # ASGI
│
├── enrollment/                 # App principal: cursos, estudiantes e inscripciones
│   ├── models.py               # Student, Course, CourseContent, Exam, Question, etc.
│   ├── views.py                # Landing, detalle público, API de cursos
│   ├── urls.py                 # Rutas públicas de cursos
│   ├── admin.py                # Configuración del admin de Django
│   ├── templatetags/           # Tags personalizados para templates
│   ├── migrations/             # Migraciones de base de datos
│   └── static/enrollment/      # JS (code-runner, matrix, console, script)
│
├── panel/                      # Panel de administración
│   ├── views.py                # Dashboard, CRUD de cursos/estudiantes, export CSV
│   ├── urls.py                 # Rutas del panel
│   └── templates/panel/        # Templates del panel admin
│
├── student_portal/             # Portal de estudiantes
│   ├── views.py                # Dashboard, exámenes, perfil, notificaciones
│   ├── urls.py                 # Rutas del portal
│   ├── admin.py                # Admin de Django para Student
│   ├── tests.py                # Tests del portal
│   └── templates/student_portal/
│
├── terminal/                   # Terminal Python interactiva
│   ├── views.py                # Vista de consola Python en el navegador
│   ├── urls.py                 # Rutas de la terminal
│   └── templates/terminal/
│
├── notificaciones/             # Sistema de notificaciones
│   ├── models.py               # Modelo Notification
│   ├── views.py                # Aceptar/rechazar estudiantes, marcar leído/no leído
│   ├── urls.py                 # Rutas de notificaciones
│   └── templates/              
│
├── email_service/              # Servicio de correo (Gmail API OAuth2)
│   ├── services.py             # Servicio principal de envío de emails
│   └── get_token*.py           # Scripts auxiliares para obtener token OAuth2
│
├── templates/                  # Templates globales
│   └── registration/           # Templates de password reset
│
├── media/                      # Archivos subidos (imágenes de perfil, cursos)
├── staticfiles/                # Archivos estáticos compilados (producción)
│
├── manage.py                   # CLI de Django
├── requirements.txt            # Dependencias del proyecto
├── Procfile                    # Configuración de despliegue
├── .gitignore                  # Archivos ignorados por git
│
├── create_new_courses.py       # Script: crea cursos 7-8 con contenido completo
├── update_courses.py           # Script: actualiza metadatos de cursos 1-6
└── add_course_content.py       # Script: agrega contenido completo a cursos 1-6
```

---

## Instalación

### Requisitos previos

- Python 3.12 o superior
- pip
- Git
- PostgreSQL (opcional, por defecto usa SQLite)

### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/Andres-Developer-23/Learn_Hub.git
cd Learn_Hub

# Crear y activar entorno virtual
python -m venv venv

# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env   # Crear si no existe (ver sección Variables de Entorno)

# Ejecutar migraciones
python manage.py migrate

# Cargar datos iniciales (opcional)
python manage.py createsuperuser
python create_new_courses.py   # Crea cursos con contenido completo
python add_course_content.py   # Agrega contenido a cursos existentes
python update_courses.py       # Actualiza metadatos de cursos

# Iniciar servidor de desarrollo
python manage.py runserver
```

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Base de datos (SQLite por defecto, PostgreSQL para producción)
DATABASE_URL=postgres://usuario:password@host:5432/learnhub

# Configuración del sitio
SITE_URL=https://learn-hub-bhxvd.ondigitalocean.app
ALLOWED_HOSTS=localhost,127.0.0.1,learn-hub-bhxvd.ondigitalocean.app
DEBUG=True

# Email SMTP (fallback)
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-app
DEFAULT_FROM_EMAIL=LearnHub <tu-email@gmail.com>

# Gmail API Token (alternativa a token.json)
GMAIL_API_TOKEN_JSON={"token": "...", "refresh_token": "...", ...}
```

| Variable | Descripción | Requerido |
|---|---|---|
| `DATABASE_URL` | URL de conexión a la base de datos | No (usa SQLite por defecto) |
| `SITE_URL` | URL base del sitio para enlaces en correos | Sí |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por coma) | No (usa `*` por defecto) |
| `DEBUG` | Modo debug (`True`/`False`) | No |
| `EMAIL_HOST_USER` | Usuario SMTP (fallback) | No |
| `EMAIL_HOST_PASSWORD` | Contraseña SMTP (fallback) | No |
| `DEFAULT_FROM_EMAIL` | Remitente por defecto para correos | No |
| `GMAIL_API_TOKEN_JSON` | Token JSON de Gmail API (alternativa a archivo) | No |

### Configuración de Gmail API

El proyecto usa la **Gmail API** como método principal de envío de correos (con SMTP como fallback).

1. Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitar la **Gmail API**
3. Crear credenciales OAuth2 → **Aplicación de escritorio**
4. Descargar el archivo JSON y colocarlo en la raíz como `client_secret_<id>.apps.googleusercontent.com.json`
5. Ejecutar el servidor; el token se generará automáticamente al enviar el primer correo, o ejecutar uno de los scripts de obtención de token:
   ```bash
   python email_service/get_token_flow.py
   ```

> ⚠️ Los archivos `client_secret_*.json`, `token.json` y `code_verifier.json` están en `.gitignore`.

### Scripts de utilidad

| Script | Descripción |
|---|---|
| `create_new_courses.py` | Crea los cursos **Regresión Lineal** y **Algoritmo Genético** con contenido, ejemplos y exámenes completos |
| `update_courses.py` | Actualiza metadatos (descripción, instructor, categoría, nivel, duración) de los cursos 1-6 |
| `add_course_content.py` | **Borra** y recrea todo el contenido, exámenes y preguntas de los cursos 1-6 |

---

## Rutas del Sistema

### Públicas

| Ruta | Vista | Descripción |
|---|---|---|
| `/` | `enrollment:index` | Catálogo de cursos con filtro por categoría |
| `/curso/<id>/` | `enrollment:enrollment_course_detail` | Detalle y previsualización del curso |
| `/api/curso/<id>/` | `enrollment:course_detail_api` | API JSON con detalle del curso |
| `/admin/` | Admin de Django | Panel de administración de Django |

### Panel de Administración (`/panel/`)

| Ruta | Vista | Descripción |
|---|---|---|
| `/panel/login/` | `admin_login` | Inicio de sesión para administradores |
| `/panel/logout/` | `admin_logout` | Cerrar sesión |
| `/panel/` | `admin_dashboard` | Dashboard con estadísticas y lista de estudiantes |
| `/panel/estudiante/<pk>/editar/` | `student_edit` | Editar datos de un estudiante |
| `/panel/estudiante/<pk>/eliminar/` | `student_delete` | Eliminar un estudiante |
| `/panel/exportar/csv/` | `export_csv` | Exportar estudiantes a CSV |
| `/panel/cursos/` | `course_list` | Listado de cursos |
| `/panel/cursos/nuevo/` | `course_create` | Crear nuevo curso |
| `/panel/cursos/<pk>/` | `course_detail` | Detalle del curso (contenido, exámenes, archivos) |
| `/panel/cursos/<pk>/editar/` | `course_edit` | Editar curso |
| `/panel/cursos/<pk>/eliminar/` | `course_delete` | Eliminar curso |
| `/panel/cursos/<pk>/contenido/nuevo/` | `content_create` | Agregar contenido al curso |
| `/panel/cursos/contenido/<pk>/eliminar/` | `content_delete` | Eliminar contenido |
| `/panel/cursos/<pk>/examen/nuevo/` | `exam_create` | Crear examen con preguntas |
| `/panel/cursos/examen/<pk>/editar/` | `exam_edit` | Editar examen |
| `/panel/cursos/examen/<pk>/eliminar/` | `exam_delete` | Eliminar examen |
| `/panel/cursos/<pk>/archivos/subir/` | `file_upload` | Subir archivo al curso |
| `/panel/cursos/archivos/<pk>/eliminar/` | `file_delete` | Eliminar archivo |
| `/panel/notificaciones/` | `notifications_view` | Centro de notificaciones y solicitudes |
| `/panel/inscripcion/<pk>/aceptar/` | `enrollment_accept` | Aceptar solicitud de inscripción a curso |
| `/panel/inscripcion/<pk>/rechazar/` | `enrollment_reject` | Rechazar solicitud de inscripción |

### Portal de Estudiantes (`/estudiante/`)

| Ruta | Vista | Descripción |
|---|---|---|
| `/estudiante/login/` | `student_login` | Inicio de sesión para estudiantes |
| `/estudiante/logout/` | `student_logout` | Cerrar sesión |
| `/estudiante/` | `student_dashboard` | Dashboard con cursos y progreso |
| `/estudiante/perfil/editar/` | `student_update_profile` | Editar perfil (nombre, teléfono, dirección, foto) |
| `/estudiante/perfil/password/` | `student_change_password` | Cambiar contraseña |
| `/estudiante/inscribir/` | `student_enroll_course` | Solicitar inscripción a un curso (JSON) |
| `/estudiante/curso/<pk>/` | `student_course_detail` | Contenido del curso con pestañas (explicación/ejemplo/demo) |
| `/estudiante/curso/<pk>/examen/` | `take_exam` | Realizar examen del curso |
| `/estudiante/curso/<pk>/examen/<attempt_pk>/resultado/` | `exam_result` | Resultado del examen |
| `/estudiante/contenido/<pk>/visto/` | `mark_content_viewed` | Marcar contenido como visto (JSON) |
| `/estudiante/notificacion/<pk>/leer/` | `student_mark_read` | Marcar notificación como leída |
| `/estudiante/notificaciones/leer-todas/` | `student_mark_all_read` | Marcar todas como leídas |
| `/estudiante/notificaciones/contar/` | `student_notifications_count` | Contar no leídas (JSON) |

### Terminal Python

| Ruta | Vista | Descripción |
|---|---|---|
| `/terminal/<pk>/` | `terminal:terminal_console` | Consola Python en el navegador (requiere inscripción al curso) |

### Notificaciones (Admin) (`/notificaciones/`)

| Ruta | Vista | Descripción |
|---|---|---|
| `/notificaciones/notificacion/<pk>/aceptar/` | `notification_accept` | Aceptar estudiante pendiente (crea usuario Django) |
| `/notificaciones/notificacion/<pk>/rechazar/` | `notification_reject` | Rechazar estudiante pendiente |
| `/notificaciones/notificacion/<pk>/leer/` | `notification_mark_read` | Marcar notificación admin como leída |
| `/notificaciones/notificacion/<pk>/desleer/` | `notification_mark_unread` | Marcar notificación admin como no leída |
| `/notificaciones/contar/` | `notifications_count` | Contar no leídas (JSON) |

### Recuperación de Contraseña

| Ruta | Descripción |
|---|---|
| `/password-reset/` | Solicitar restablecimiento de contraseña |
| `/password-reset/done/` | Confirmación de envío |
| `/password-reset/<uidb64>/<token>/` | Establecer nueva contraseña |
| `/password-reset/complete/` | Contraseña restablecida exitosamente |

---

## Modelos Principales

### `Student`
Representa un estudiante registrado en la plataforma.

| Campo | Tipo | Descripción |
|---|---|---|
| `user` | `OneToOneField(User)` | Usuario de Django asociado (nullable, se crea al aceptar) |
| `generated_password` | `CharField(50)` | Contraseña temporal generada al aceptar |
| `name` | `CharField(150)` | Nombre completo |
| `email` | `EmailField` | Correo electrónico (único) |
| `phone` | `CharField(20)` | Teléfono (opcional) |
| `address` | `TextField` | Dirección (opcional) |
| `profile_picture` | `ImageField` | Foto de perfil (default: `default.png`) |
| `level` | `CharField` | Nivel: `principiante`, `intermedio`, `avanzado` |
| `status` | `CharField` | Estado: `pending`, `accepted`, `rejected` |
| `courses` | `ManyToManyField(Course)` | Cursos en los que está inscrito |
| `created_at` | `DateTimeField` | Fecha de registro |
| `updated_at` | `DateTimeField` | Última actualización |

### `Course`
Curso disponible en la plataforma.

| Campo | Tipo | Descripción |
|---|---|---|
| `title` | `CharField(200)` | Título del curso |
| `description` | `TextField` | Descripción detallada |
| `icon` | `CharField(50)` | Emoji ícono (default: `📚`) |
| `image` | `ImageField` | Imagen de portada |
| `duration` | `CharField(100)` | Duración estimada |
| `level` | `CharField` | Nivel del curso |
| `category` | `CharField` | Categoría: `desarrollo-web`, `inteligencia-artificial`, `ciencia-de-datos`, `desarrollo-movil`, `diseno-ux-ui`, `cloud-devops` |
| `instructor_name` | `CharField(150)` | Nombre del instructor |
| `instructor_bio` | `TextField` | Biografía del instructor |
| `instructor_avatar_url` | `CharField(500)` | URL del avatar del instructor |
| `is_active` | `BooleanField` | Visible en catálogo (default: `True`) |
| `order` | `PositiveIntegerField` | Orden de aparición |

### `CourseContent`
Contenido educativo dentro de un curso.

| Campo | Tipo | Descripción |
|---|---|---|
| `course` | `ForeignKey(Course)` | Curso al que pertenece |
| `section_type` | `CharField` | Tipo: `explicacion`, `ejemplo`, `demo` |
| `title` | `CharField(200)` | Título del contenido |
| `content` | `TextField` | Contenido HTML |
| `file` | `FileField` | Archivo adjunto (opcional) |
| `order` | `PositiveIntegerField` | Orden dentro del curso |

### `CourseFile`
Archivos adicionales asociados a un curso.

| Campo | Tipo | Descripción |
|---|---|---|
| `course` | `ForeignKey(Course)` | Curso asociado |
| `title` | `CharField(200)` | Nombre del archivo |
| `file` | `FileField` | Archivo |
| `uploaded_at` | `DateTimeField` | Fecha de subida |

### `Exam`
Examen asociado a un curso.

| Campo | Tipo | Descripción |
|---|---|---|
| `course` | `ForeignKey(Course)` | Curso asociado |
| `title` | `CharField(200)` | Título del examen |
| `description` | `TextField` | Descripción |
| `passing_score` | `PositiveIntegerField` | Puntaje mínimo para aprobar (%) |
| `time_limit_minutes` | `PositiveIntegerField` | Límite de tiempo (minutos) |

### `Question`
Pregunta de un examen.

| Campo | Tipo | Descripción |
|---|---|---|
| `exam` | `ForeignKey(Exam)` | Examen al que pertenece |
| `text` | `TextField` | Texto de la pregunta |
| `order` | `PositiveIntegerField` | Orden |

### `QuestionOption`
Opción de respuesta para una pregunta.

| Campo | Tipo | Descripción |
|---|---|---|
| `question` | `ForeignKey(Question)` | Pregunta asociada |
| `text` | `CharField(255)` | Texto de la opción |
| `is_correct` | `BooleanField` | Si es la respuesta correcta |
| `order` | `PositiveIntegerField` | Orden |

### `ExamAttempt`
Registro de un intento de examen por un estudiante.

| Campo | Tipo | Descripción |
|---|---|---|
| `student` | `ForeignKey(Student)` | Estudiante |
| `exam` | `ForeignKey(Exam)` | Examen |
| `score` | `PositiveIntegerField` | Puntaje obtenido |
| `total` | `PositiveIntegerField` | Puntaje total posible |
| `passed` | `BooleanField` | Si aprobó |
| `started_at` | `DateTimeField` | Inicio del intento |
| `completed_at` | `DateTimeField` | Finalización |

### `EnrollmentRequest`
Solicitud de inscripción a un curso.

| Campo | Tipo | Descripción |
|---|---|---|
| `student` | `ForeignKey(Student)` | Estudiante solicitante |
| `course` | `ForeignKey(Course)` | Curso solicitado |
| `status` | `CharField` | Estado: `pending`, `accepted`, `rejected` |
| `created_at` | `DateTimeField` | Fecha de solicitud |

### `ContentProgress`
Progreso de visualización de contenido por estudiante.

| Campo | Tipo | Descripción |
|---|---|---|
| `student` | `ForeignKey(Student)` | Estudiante |
| `content` | `ForeignKey(CourseContent)` | Contenido visto |
| `viewed_at` | `DateTimeField` | Fecha de visualización |

### `Notification`
Notificación para un estudiante.

| Campo | Tipo | Descripción |
|---|---|---|
| `student` | `ForeignKey(Student)` | Estudiante destinatario |
| `title` | `CharField(200)` | Título (default: `Notificación`) |
| `message` | `TextField` | Mensaje |
| `notif_type` | `CharField` | Tipo: `info`, `success`, `warning`, `error` |
| `is_read` | `BooleanField` | Leída o no |
| `created_at` | `DateTimeField` | Fecha de creación |

---

## Flujo de Inscripción

### Registro de estudiante
1. El estudiante se registra desde el formulario público en la landing page (`/`)
2. La solicitud queda en estado **`pending`**
3. El administrador revisa desde `/notificaciones/` o `/panel/notificaciones/`
4. Al **aceptar**, se crea automáticamente un usuario de Django con contraseña generada
5. El estudiante recibe un correo de bienvenida con sus credenciales
6. El estudiante inicia sesión en `/estudiante/login/`

### Inscripción a curso
1. El estudiante autenticado solicita inscripción desde el detalle del curso
2. Se crea un `EnrollmentRequest` en estado `pending`
3. El administrador acepta/rechaza desde el panel
4. Si es aceptado, el estudiante accede al contenido del curso

---

## Despliegue

### DigitalOcean App Platform

El proyecto incluye un `Procfile` para despliegue en plataformas como DigitalOcean o Heroku:

```
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn ai_project.wsgi --log-file - --bind 0.0.0.0:$PORT
```

**Fase `release`**: Ejecuta migraciones y recolecta archivos estáticos antes de desplegar.
**Proceso `web`**: Inicia Gunicorn en el puerto asignado por la plataforma.

### Variables requeridas en producción

```
DATABASE_URL=<postgres-url>
SITE_URL=https://tu-dominio.com
ALLOWED_HOSTS=tu-dominio.com
DEBUG=False
```

---

## Seguridad

- **CSRF** protegido con `CSRF_COOKIE_SECURE = True` y `SameSite=Lax`
- **Sesiones** seguras con `SESSION_COOKIE_SECURE = True`, `HttpOnly` y `SameSite=Lax`
- Nombre personalizado de cookie de sesión: `learnhub_sessionid`
- Sesión expira al cerrar el navegador (`SESSION_EXPIRE_AT_BROWSER_CLOSE = True`)
- Proxy SSL header configurado (`SECURE_PROXY_SSL_HEADER`)
- Middleware `NoCacheForAuthenticatedMiddleware` previene caché del navegador para usuarios autenticados
- `DEBUG = False` en producción
- Archivos sensibles (credenciales OAuth, tokens, `.env`) excluidos vía `.gitignore`

---

## Licencia

Este proyecto es de uso educativo y privado.
