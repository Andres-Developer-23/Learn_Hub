from django.db import migrations

def create_courses(apps, schema_editor):
    Course = apps.get_model('enrollment', 'Course')
    courses = [
        {'title': 'Fundamentos de IA', 'description': 'Historia, conceptos clave, tipos de IA y matemáticas esenciales: álgebra lineal, probabilidad y estadística.', 'icon': '🧠', 'duration': 'Semanas 1-2', 'order': 1},
        {'title': 'Machine Learning', 'description': 'Regresión, clasificación, clustering, árboles de decisión y validación de modelos con Scikit-Learn.', 'icon': '🤖', 'duration': 'Semanas 3-5', 'order': 2},
        {'title': 'Redes Neuronales', 'description': 'Perceptrón, backpropagation, funciones de activación y construcción de redes con TensorFlow/Keras.', 'icon': '🕸️', 'duration': 'Semanas 6-8', 'order': 3},
        {'title': 'Lenguaje Natural (NLP)', 'description': 'Tokenización, embeddings, transformers y construcción de modelos de lenguaje como GPT básico.', 'icon': '💬', 'duration': 'Semanas 9-11', 'order': 4},
        {'title': 'Visión Computacional', 'description': 'Redes convolucionales (CNN), detección de objetos y clasificación de imágenes con OpenCV y PyTorch.', 'icon': '👁️', 'duration': 'Semanas 12-14', 'order': 5},
        {'title': 'Proyecto Final', 'description': 'Desarrollo y presentación de un proyecto de IA real, desde la idea hasta el deploy en producción.', 'icon': '🚀', 'duration': 'Semanas 15-16', 'order': 6},
    ]
    for c in courses:
        Course.objects.get_or_create(title=c['title'], defaults=c)

def delete_courses(apps, schema_editor):
    Course = apps.get_model('enrollment', 'Course')
    Course.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('enrollment', '0006_course_student_courses'),
    ]
    operations = [
        migrations.RunPython(create_courses, delete_courses),
    ]