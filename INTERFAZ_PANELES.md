# Interfaz del Panel de Administración y Panel de Estudiante

Este documento describe la estructura y componentes de las interfaces de usuario del sistema.

---

## 1. Panel de Administración

**Ubicación:** `panel/templates/panel/dashboard.html`

El panel de administración es donde los administradores gestionan estudiantes, cursos y notificaciones.

### 1.1 Estructura Visual

El diseño utiliza un tema oscuro con acentos en azul (`#4f8ef7`) y tiene soporte para modo claro mediante la variable CSS `[data-theme="light"]`.

### 1.2 Barra Lateral (Sidebar)

Ancho: 250px, fija a la izquierda.

**Secciones del menú:**

| Sección | Icono | Descripción |
|---------|-------|-------------|
| Dashboard | 📊 | Vista principal con estadísticas |
| Estudiantes | 👥 | Lista de estudiantes inscritos |
| Notificaciones | 🔔 | Gestión de notificaciones |
| Cursos | 📚 | Lista de cursos disponibles |
| Exportar CSV | 📥 | Exportar datos a CSV |
| Ver sitio web | 🌐 | Ir al sitio público |
| Django Admin | ⚙️ | Panel admin de Django |

**Información del usuario:**

- Avatar con iniciales del nombre
- Nombre de usuario
- Rol: Administrador
- Botón para cerrar sesión

### 1.3 Panel Principal

#### Vista de Estadísticas (Overview)

Muestra 5 tarjetas con métricas:

- **Total Inscritos:** Cantidad total de estudiantes registrados
- **Pendientes:** Estudiantes esperando revisión
- **Aceptados:** Inscripciones confirmadas
- **Rechazados:** Solicitudes no aprobadas
- **Esta Semana:** Nuevas solicitudes de la semana actual

#### Gráficos

- **Distribución por Nivel (Dona):** Muestra principiante, intermedio, avanzado
- **Por Estado (Barras):** Pendientes, aceptados, rechazados

#### Vista de Estudiantes

Tabla con columnas:

- `#` - ID del estudiante
- **Nombre / Correo** - Datos del estudiante
- **Nivel** - Badge colored: principiante (verde), intermedio (amarillo), avanzado (morado)
- **Estado** - Badge: Pendiente (amarillo), Aceptado (verde), Rechazado (rojo)
- **Usuario / Clave** - Credenciales generadas (solo si fueron creadas)
- **Acciones** - Editar (🖉) y Eliminar (🗑️)

**Funcionalidades:**

- Buscador en tiempo real por nombre o correo
- Modal para editar estudiante (nombre, correo, nivel)
- Modal de confirmación para eliminar
- Modal para mostrar credenciales al aceptar estudiante

### 1.4 Modales

| Modal | Propósito |
|-------|-----------|
| Editar Estudiante | Modificar nombre, correo, nivel |
| Confirmar eliminación | Validar antes de borrar |
| Credenciales | Mostrar usuario y contraseña generados |

---

## 2. Panel de Estudiante

**Ubicación:** `student_portal/templates/student_portal/dashboard.html`

El portal del estudiante permite a los usuarios gestionar su perfil, cursos y notificaciones.

### 2.1 Estructura Visual

Mismo diseño base que el admin, pero con sidebar de 240px y elementos adaptados para estudiantes.

### 2.2 Barra Lateral (Sidebar)

| Sección | Icono | Descripción |
|---------|-------|-------------|
| Inicio | 🏠 | Dashboard personal |
| Notificaciones | 🔔 | Centro de notificaciones (con badge de no leídas) |
| Mi Curso | 📚 | Cursos disponibles e inscritos |
| Mi Perfil | 👤 | Información personal |
| Seguridad | 🔒 | Cambiar contraseña |
| Sitio Web | 🌐 | Ir al sitio público |

**Información del usuario:**

- Avatar con inicial del nombre
- Nombre del estudiante
- Rol: Estudiante

### 2.3 Panel Principal

#### Sección Inicio (Home)

- **Banner de bienvenida** con el estado de inscripción y nivel
- **Tarjetas de información:**
  - Usuario
  - Correo
  - Nivel (badge colored)
  - Fecha de inscripción

#### Sección Notificaciones

- Lista de notificaciones con icono según tipo (✅ éxito, ❌ error, ⚠️ advertencia, ℹ️ info)
- Badge de "no leída" (punto azul)
- Botón para marcar todas como leídas
- Muestra tiempo relativo (ej: "hace 5 minutos")

#### Sección Mi Curso

- **Cursos inscritos:** Tarjetas con badge "✓ Inscrito"
- **Todos los cursos:** Lista de cursos disponibles
- Cada curso muestra: icono, título, descripción, duración
- Botón "Inscribirse" que abre modal de confirmación

**Modal de inscripción:**

- Icono y nombre del curso
- Mensaje indicando que la solicitud será revisada por admin
- Botones Cancelar y Solicitar

#### Sección Mi Perfil

- **Avatar:** Circular con opción de subir imagen
- **Información editable:**
  - Nombre completo
  - Teléfono
  - Dirección
- **Información de cuenta (solo lectura):**
  - Usuario
  - Correo
  - Nivel
  - Estado

#### Sección Seguridad

- Formulario para cambiar contraseña:
  - Contraseña actual
  - Nueva contraseña
  - Confirmar nueva contraseña

### 2.4 Funcionalidades JavaScript

- Cambio de tema (oscuro/claro)
- Navegación entre secciones sin recarga
- Actualización de perfil con imagen
- Inscripción a cursos vía AJAX
- Marcar notificaciones como leídas
- Cambio de contraseña

---

## 3. Características Comunes

### 3.1 Sistema de Temas

Ambos paneles comparten:

- Variables CSS para colores
- Soporte para tema claro/oscuro
- Transiciones suaves (0.3s)

### 3.2 Toast Notifications

Mensajes emergentes en la esquina inferior derecha:

- Éxito: Fondo verde
- Error: Fondo rojo

### 3.3 Diseño Responsivo

En pantallas menores a 768px, el sidebar se oculta y el contenido ocupa todo el ancho.

### 3.4 Iconos y Tipografía

- **Fuente:** Inter (Google Fonts)
- **Iconos:** Font Awesome 6.5.1
- **Gráficos:** Chart.js

---

## 4. Rutas URL

| Panel | Ruta |
|-------|------|
| Admin Dashboard | `/panel/dashboard/` |
| Student Dashboard | `/estudiante/dashboard/` |
| Login Admin | `/panel/login/` |
| Login Estudiante | `/estudiante/login/` |