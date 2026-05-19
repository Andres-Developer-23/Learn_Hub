import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_project.settings')
django.setup()

from enrollment.models import Course

cursos_data = [
    {
        'id': 1,
        'title': 'Fundamentos de IA',
        'description': (
            'Introducción completa a la Inteligencia Artificial: historia, conceptos clave y tipos de IA. '
            'Fundamentos matemáticos esenciales: álgebra lineal, probabilidad y estadística aplicada. '
            'Ética en IA y casos de uso reales en la industria.'
        ),
        'level': 'principiante',
        'duration': 'Semanas 1-2',
        'instructor_name': 'Dra. María Elena Vásquez',
        'instructor_bio': (
            'Doctora en Ciencias de la Computación por la UNAM con más de 12 años de experiencia en investigación de IA. '
            'Ex investigadora en Google DeepMind y autora de 30+ publicaciones en conferencias internacionales. '
            'Especialista en fundamentos de machine learning y ética en IA.'
        ),
        'instructor_avatar_url': 'https://ui-avatars.com/api/?name=Maria+Vasquez&background=0D8ABC&color=fff&size=200',
        'category': 'inteligencia-artificial',
    },
    {
        'id': 2,
        'title': 'Machine Learning',
        'description': (
            'Aprende los algoritmos fundamentales de Machine Learning: regresión lineal y logística, '
            'árboles de decisión, random forests, SVM y clustering (K-Means, DBSCAN). '
            'Validación cruzada, métricas de evaluación y optimización de hiperparámetros con Scikit-Learn. '
            'Proyectos prácticos con datasets reales.'
        ),
        'level': 'intermedio',
        'duration': 'Semanas 3-5',
        'instructor_name': 'Ing. Carlos Andrés Mendoza',
        'instructor_bio': (
            'Ingeniero de Machine Learning en Amazon Web Services con 8 años de experiencia construyendo '
            'sistemas de recomendación y modelos predictivos a escala. Contribuidor open-source en Scikit-Learn '
            'y mentor en programas de formación de datos en Latinoamérica.'
        ),
        'instructor_avatar_url': 'https://ui-avatars.com/api/?name=Carlos+Mendoza&background=6B4C9A&color=fff&size=200',
    },
    {
        'id': 3,
        'title': 'Redes Neuronales',
        'description': (
            'Desde el perceptrón simple hasta arquitecturas profundas: backpropagation, funciones de activación '
            '(ReLU, sigmoid, tanh, GELU), regularización (dropout, batch normalization) y optimizadores (Adam, SGD). '
            'Construcción de redes con TensorFlow/Keras. Introducción a GANs y autoencoders.'
        ),
        'level': 'intermedio',
        'duration': 'Semanas 6-8',
        'instructor_name': 'Dr. Roberto Alejandro Silva',
        'instructor_bio': (
            'PhD en Deep Learning por el MIT con experiencia en NVIDIA y OpenAI. '
            'Investigador principal en arquitecturas de redes neuronales eficientes. '
            'Ha formado a más de 5,000 estudiantes en deep learning a nivel global.'
        ),
        'instructor_avatar_url': 'https://ui-avatars.com/api/?name=Roberto+Silva&background=2E8B57&color=fff&size=200',
    },
    {
        'id': 4,
        'title': 'Lenguaje Natural (NLP)',
        'description': (
            'Procesamiento de Lenguaje Natural moderno: tokenización, stemming, lematización, '
            'word embeddings (Word2Vec, GloVe, FastText), arquitecturas transformer (BERT, GPT). '
            'Fine-tuning de modelos pre-entrenados con Hugging Face. '
            'Aplicaciones: análisis de sentimiento, chatbots, traducción automática y generación de texto.'
        ),
        'level': 'avanzado',
        'duration': 'Semanas 9-11',
        'instructor_name': 'Dra. Ana Lucía Fernández',
        'instructor_bio': (
            'Doctora en Lingüística Computacional por la Universidad de Barcelona. '
            'Investigadora en NLP para idiomas de bajos recursos, con enfoque en español y lenguas indígenas. '
            'Colaboradora activa en Hugging Face y conferencista en ACL y EMNLP.'
        ),
        'instructor_avatar_url': 'https://ui-avatars.com/api/?name=Ana+Fernandez&background=C0392B&color=fff&size=200',
    },
    {
        'id': 5,
        'title': 'Visión Computacional',
        'description': (
            'Redes convolucionales (CNN) desde cero: convoluciones, pooling, architectures clásicas '
            '(AlexNet, VGG, ResNet, EfficientNet). Detección de objetos con YOLO y Faster R-CNN. '
            'Segmentación semántica e instancial. Transfer learning y data augmentation. '
            'Proyectos con OpenCV y PyTorch: reconocimiento facial, OCR y análisis médico.'
        ),
        'level': 'avanzado',
        'duration': 'Semanas 12-14',
        'instructor_name': 'MSc. Diego Andrés Herrera',
        'instructor_bio': (
            'Máster en Visión Computacional por Carnegie Mellon University. '
            'Ingeniero de Computer Vision en Tesla, trabajando en sistemas de percepción para vehículos autónomos. '
            'Publicado en CVPR y ICCV con más de 50 citas.'
        ),
        'instructor_avatar_url': 'https://ui-avatars.com/api/?name=Diego+Herrera&background=E67E22&color=fff&size=200',
    },
    {
        'id': 6,
        'title': 'Proyecto Final',
        'description': (
            'Integración de todos los conocimientos en un proyecto real de IA: desde la definición del problema '
            'y recolección de datos hasta el despliegue en producción con Docker y APIs REST. '
            'Metodologías ágiles, documentación técnica y presentación ejecutiva. '
            'Evaluación por panel de expertos de la industria.'
        ),
        'level': 'avanzado',
        'duration': 'Semanas 15-16',
        'instructor_name': 'Dr. Javier Antonio Ruiz',
        'instructor_bio': (
            'Director de Ingeniería de IA en Microsoft con 15 años de experiencia liderando equipos de producto. '
            'Ex CTO de startup de IA adquirida por Salesforce. Mentor de aceleradoras como Y Combinator y Techstars. '
            'Apasionado por la formación de talento en IA en Latinoamérica.'
        ),
        'instructor_avatar_url': 'https://ui-avatars.com/api/?name=Javier+Ruiz&background=8E44AD&color=fff&size=200',
    },
]

for data in cursos_data:
    course = Course.objects.get(id=data['id'])
    course.title = data['title']
    course.description = data['description']
    course.level = data['level']
    course.duration = data['duration']
    course.instructor_name = data['instructor_name']
    course.instructor_bio = data['instructor_bio']
    course.instructor_avatar_url = data['instructor_avatar_url']
    course.category = data.get('category', course.category)
    course.save()
    print(f'Actualizado: {course.title} (nivel: {course.level})')

print('\nTodos los cursos han sido actualizados correctamente.')
