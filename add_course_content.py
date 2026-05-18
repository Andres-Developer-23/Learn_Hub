import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_project.settings')
django.setup()

from enrollment.models import Course, CourseContent, Exam, Question, QuestionOption

# Limpiar contenido existente
CourseContent.objects.all().delete()
Exam.objects.all().delete()
Question.objects.all().delete()
QuestionOption.objects.all().delete()

print("Contenido previo limpiado.\n")

# ============================================================
# CURSO 1: Fundamentos de IA
# ============================================================
course1 = Course.objects.get(id=1)

# --- Explicaciones ---
CourseContent.objects.create(course=course1, section_type='explicacion', title='¿Qué es la Inteligencia Artificial?', content='''<h3>Definición de Inteligencia Artificial</h3>
<p>La Inteligencia Artificial (IA) es una rama de las ciencias de la computación que se enfoca en crear sistemas capaces de realizar tareas que normalmente requieren inteligencia humana. Estas tareas incluyen el aprendizaje, el razonamiento, la percepción, la comprensión del lenguaje y la toma de decisiones.</p>

<h3>Definición formal (Russell & Norvig, 2020)</h3>
<p>Según Stuart Russell y Peter Norvig en su libro <em>"Artificial Intelligence: A Modern Approach"</em> (4ta edición), la IA estudia <strong>agentes inteligentes</strong>: sistemas que perciben su entorno y realizan acciones que maximizan sus probabilidades de alcanzar sus objetivos.</p>

<h3>Tipos de IA</h3>
<ul>
<li><strong>IA Narrow (ANI):</strong> Sistemas diseñados para una tarea específica (ej: Siri, AlphaGo, filtros de spam).</li>
<li><strong>IA General (AGI):</strong> Sistemas con capacidad cognitiva equivalente a la humana (aún no existe).</li>
<li><strong>Superinteligencia (ASI):</strong> Sistemas que superan la inteligencia humana en todos los aspectos (hipotética).</li>
</ul>

<h3>Historia resumida</h3>
<table>
<tr><th>Año</th><th>Hito</th></tr>
<tr><td>1950</td><td>Alan Turing publica "Computing Machinery and Intelligence" y propone el Test de Turing</td></tr>
<tr><td>1956</td><td>Conferencia de Dartmouth: nace el término "Inteligencia Artificial" (John McCarthy)</td></tr>
<tr><td>1997</td><td>Deep Blue de IBM vence al campeón mundial de ajedrez Garry Kasparov</td></tr>
<tr><td>2012</td><td>Deep Learning revoluciona la visión computacional (AlexNet en ImageNet)</td></tr>
<tr><td>2017</td><td>Se publica el paper "Attention Is All You Need" (arquitectura Transformer)</td></tr>
<tr><td>2022-2023</td><td>Explosión de modelos de lenguaje: ChatGPT, GPT-4, Claude, Gemini</td></tr>
</table>''', order=1)

CourseContent.objects.create(course=course1, section_type='explicacion', title='Fundamentos Matemáticos de la IA', content='''<h3>Álgebra Lineal</h3>
<p>El álgebra lineal es fundamental para la IA porque los datos se representan como vectores y matrices. Conceptos clave:</p>
<ul>
<li><strong>Vector:</strong> Array ordenado de números. Ej: [2.5, 3.1, 1.0] representa las características de un dato.</li>
<li><strong>Matriz:</strong> Tabla 2D de números. Las imágenes se representan como matrices de píxeles.</li>
<li><strong>Producto punto:</strong> Operación fundamental en redes neuronales. a·b = Σ(aᵢ × bᵢ)</li>
<li><strong>Valores y vectores propios:</strong> Usados en PCA (Análisis de Componentes Principales) para reducción de dimensionalidad.</li>
</ul>

<h3>Probabilidad y Estadística</h3>
<ul>
<li><strong>Distribución normal (Gaussiana):</strong> f(x) = (1/σ√2π) × e^(-(x-μ)²/2σ²)</li>
<li><strong>Teorema de Bayes:</strong> P(A|B) = P(B|A) × P(A) / P(B) — base de clasificadores bayesianos</li>
<li><strong>Esperanza matemática:</strong> E[X] = Σ xᵢ × P(xᵢ)</li>
<li><strong>Varianza:</strong> Var(X) = E[(X - μ)²] — mide la dispersión de los datos</li>
</ul>

<h3>Cálculo</h3>
<ul>
<li><strong>Derivadas:</strong> Fundamentales para el algoritmo de backpropagation en redes neuronales.</li>
<li><strong>Gradiente:</strong> Vector de derivadas parciales ∇f = (∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ)</li>
<li><strong>Regla de la cadena:</strong> d/dx[f(g(x))] = f'(g(x)) × g'(x) — esencial para calcular gradientes en redes profundas</li>
</ul>''', order=2)

CourseContent.objects.create(course=course1, section_type='explicacion', title='Ética en la Inteligencia Artificial', content='''<h3>Principios Éticos Fundamentales</h3>
<p>La ética en IA es un campo interdisciplinario que aborda los impactos morales y sociales de los sistemas inteligentes. Principios clave según la <strong>UNESCO (2021)</strong> y la <strong>Comisión Europea</strong>:</p>

<ul>
<li><strong>Transparencia:</strong> Los sistemas de IA deben ser explicables. Los usuarios deben saber cuándo interactúan con una IA.</li>
<li><strong>Justicia y no discriminación:</strong> Los algoritmos no deben perpetuar sesgos raciales, de género o socioeconómicos.</li>
<li><strong>Privacidad:</strong> Protección de datos personales conforme al GDPR (Reglamento General de Protección de Datos de la UE).</li>
<li><strong>Responsabilidad:</strong> Debe existir un marco claro de responsabilidad cuando un sistema de IA causa daño.</li>
<li><strong>Seguridad:</strong> Los sistemas deben ser robustos contra ataques y fallos.</li>
</ul>

<h3>Casos reales de sesgo algorítmico</h3>
<ul>
<li><strong>COMPAS (2016):</strong> Sistema de evaluación de riesgo criminal en EE.UU. mostró sesgo racial contra personas afroamericanas (ProPublica).</li>
<li><strong>Amazon Recruiting Tool (2018):</strong> Sistema de reclutamiento que discriminaba candidatos mujeres porque fue entrenado con datos históricos predominantemente masculinos.</li>
<li><strong>Reconocimiento facial:</strong> Estudios de Joy Buolamwini (MIT) mostraron tasas de error del 35% para mujeres de piel oscura vs. 0.8% para hombres de piel clara.</li>
</ul>

<h3>Marco regulatorio</h3>
<ul>
<li><strong>EU AI Act (2024):</strong> Primera ley integral de IA en el mundo. Clasifica sistemas por nivel de riesgo: inaceptable, alto, limitado y mínimo.</li>
<li><strong>Executive Order on AI (EE.UU., 2023):</strong> Establece estándares de seguridad y privacidad para el desarrollo de IA.</li>
</ul>''', order=3)

# --- Ejemplos ---
CourseContent.objects.create(course=course1, section_type='ejemplo', title='Ejemplo: Test de Turing en la práctica', content='''<h3>El Test de Turing</h3>
<p>Propuesto por Alan Turing en 1950, el test evalúa si una máquina puede exhibir comportamiento inteligente indistinguible del de un humano.</p>

<h3>Ejemplo de interacción</h3>
<pre><code>Interrogador: ¿Puedes describir cómo te sientes hoy?
Máquina:   Me siento bien, aunque un poco cansado porque
           estuve estudiando hasta tarde para un examen.
Interrogador: ¿Qué tipo de examen?
Máquina:   Un examen de matemáticas sobre cálculo integral.
           Las integrales por partes me cuestan un poco.
</code></pre>

<h3>Implementación básica en Python</h3>
<pre><code>def simple_turing_test(responses, human_responses):
    """
    Compara respuestas de máquina vs humanas.
    En la práctica real, se usan evaluadores humanos ciegos.
    """
    from difflib import SequenceMatcher
    
    similarities = []
    for m_resp, h_resp in zip(responses, human_responses):
        similarity = SequenceMatcher(None, m_resp, h_resp).ratio()
        similarities.append(similarity)
    
    avg_similarity = sum(similarities) / len(similarities)
    return avg_similarity

# En 2023, GPT-4 logró engañar al 54% de los evaluadores
# en tests de Turing adaptados (estudio de Kevin Roose, NYT)
</code></pre>''', order=4)

CourseContent.objects.create(course=course1, section_type='ejemplo', title='Ejemplo: Agente inteligente simple', content='''<h3>Agente basado en reglas (reflejo simple)</h3>
<p>Un agente inteligente percibe su entorno y actúa. El tipo más básico es el agente reflejo simple.</p>

<pre><code>class SimpleAgent:
    """Agente reflejo simple para un robot aspirador."""
    
    def __init__(self):
        self.rules = {
            ('A', 'sucio'): 'aspirar',
            ('A', 'limpio'): 'mover_a_B',
            ('B', 'sucio'): 'aspirar',
            ('B', 'limpio'): 'mover_a_A',
        }
    
    def perceive_and_act(self, location, status):
        percept = (location, status)
        action = self.rules.get(percept, 'esperar')
        return action

# Ejemplo de uso
agent = SimpleAgent()
print(agent.perceive_and_act('A', 'sucio'))   # Output: aspirar
print(agent.perceive_and_act('A', 'limpio'))  # Output: mover_a_B
print(agent.perceive_and_act('B', 'sucio'))   # Output: aspirar
</code></pre>

<p>Este ejemplo proviene del libro <em>"Artificial Intelligence: A Modern Approach"</em> de Russell & Norvig, Capítulo 2.</p>''', order=5)

# --- Demo ---
CourseContent.objects.create(course=course1, section_type='demo', title='Demo: Calculadora de probabilidad bayesiana', content='''<h3>Implementación del Teorema de Bayes</h3>
<p>Esta demo calcula probabilidades condicionales usando el Teorema de Bayes.</p>

<pre><code>def bayes_theorem(p_a, p_b_given_a, p_b_given_not_a):
    """
    Calcula P(A|B) usando el Teorema de Bayes.
    
    P(A|B) = P(B|A) * P(A) / P(B)
    donde P(B) = P(B|A)*P(A) + P(B|¬A)*P(¬A)
    
    Args:
        p_a: Probabilidad previa P(A)
        p_b_given_a: Probabilidad P(B|A)
        p_b_given_not_a: Probabilidad P(B|¬A)
    
    Returns:
        P(A|B): Probabilidad posterior
    """
    p_not_a = 1 - p_a
    p_b = p_b_given_a * p_a + p_b_given_not_a * p_not_a
    
    if p_b == 0:
        return 0
    
    p_a_given_b = (p_b_given_a * p_a) / p_b
    return p_a_given_b

# Ejemplo: Prueba médica
# P(Enfermo) = 0.01 (1% de la población tiene la enfermedad)
# P(Positivo|Enfermo) = 0.95 (sensibilidad)
# P(Positivo|Sano) = 0.05 (falso positivo)

resultado = bayes_theorem(
    p_a=0.01,
    p_b_given_a=0.95,
    p_b_given_not_a=0.05
)
print(f"Probabilidad de estar enfermo dado positivo: {resultado:.4f}")
# Output: 0.1610 (¡solo 16.1%! Contraintuitivo pero correcto)
</code></pre>''', order=6)

# --- Examen ---
exam1 = Exam.objects.create(course=course1, title='Examen: Fundamentos de IA', description='Evaluación de conceptos fundamentales de Inteligencia Artificial', passing_score=70, time_limit_minutes=30)

q1 = Question.objects.create(exam=exam1, text='¿Quién propuso el Test de Turing y en qué año?', order=1)
QuestionOption.objects.create(question=q1, text='Alan Turing en 1950', is_correct=True, order=1)
QuestionOption.objects.create(question=q1, text='John McCarthy en 1956', is_correct=False, order=2)
QuestionOption.objects.create(question=q1, text='Marvin Minsky en 1960', is_correct=False, order=3)
QuestionOption.objects.create(question=q1, text='Claude Shannon en 1948', is_correct=False, order=4)

q2 = Question.objects.create(exam=exam1, text='¿Qué tipo de IA existe actualmente en la práctica?', order=2)
QuestionOption.objects.create(question=q2, text='IA General (AGI)', is_correct=False, order=1)
QuestionOption.objects.create(question=q2, text='IA Narrow (ANI)', is_correct=True, order=2)
QuestionOption.objects.create(question=q2, text='Superinteligencia (ASI)', is_correct=False, order=3)
QuestionOption.objects.create(question=q2, text='IA Consciente', is_correct=False, order=4)

q3 = Question.objects.create(exam=exam1, text='¿Qué conferencia marcó el nacimiento oficial del término "Inteligencia Artificial"?', order=3)
QuestionOption.objects.create(question=q3, text='Conferencia de Dartmouth (1956)', is_correct=True, order=1)
QuestionOption.objects.create(question=q3, text='Conferencia de Princeton (1950)', is_correct=False, order=2)
QuestionOption.objects.create(question=q3, text='Conferencia de Stanford (1962)', is_correct=False, order=3)
QuestionOption.objects.create(question=q3, text='Conferencia de MIT (1958)', is_correct=False, order=4)

q4 = Question.objects.create(exam=exam1, text='¿Qué caso real demostró sesgo racial en un sistema de evaluación de riesgo criminal?', order=4)
QuestionOption.objects.create(question=q4, text='Amazon Recruiting Tool', is_correct=False, order=1)
QuestionOption.objects.create(question=q4, text='COMPAS', is_correct=True, order=2)
QuestionOption.objects.create(question=q4, text='Watson Health', is_correct=False, order=3)
QuestionOption.objects.create(question=q4, text='Google Photos', is_correct=False, order=4)

q5 = Question.objects.create(exam=exam1, text='¿Cuál es la fórmula del Teorema de Bayes?', order=5)
QuestionOption.objects.create(question=q5, text='P(A|B) = P(B|A) × P(A) / P(B)', is_correct=True, order=1)
QuestionOption.objects.create(question=q5, text='P(A|B) = P(A) × P(B) / P(A∩B)', is_correct=False, order=2)
QuestionOption.objects.create(question=q5, text='P(A|B) = P(B|A) + P(A) - P(B)', is_correct=False, order=3)
QuestionOption.objects.create(question=q5, text='P(A|B) = P(A) / P(B)', is_correct=False, order=4)

print(f"Curso 1: {course1.title} - Contenido agregado")

# ============================================================
# CURSO 2: Machine Learning
# ============================================================
course2 = Course.objects.get(id=2)

CourseContent.objects.create(course=course2, section_type='explicacion', title='Regresión Lineal y Logística', content='''<h3>Regresión Lineal</h3>
<p>La regresión lineal modela la relación entre una variable dependiente (y) y una o más variables independientes (X). Es el algoritmo más fundamental del machine learning supervisado.</p>

<h4>Modelo matemático</h4>
<p>y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε</p>
<p>Donde β son los coeficientes y ε es el error.</p>

<h4>Función de costo (Mean Squared Error)</h4>
<p>MSE = (1/n) × Σ(yᵢ - ŷᵢ)²</p>

<h3>Regresión Logística</h3>
<p>A pesar de su nombre, es un algoritmo de <strong>clasificación</strong>. Usa la función sigmoide para predecir probabilidades:</p>

<p>σ(z) = 1 / (1 + e⁻ᶻ)</p>

<p>Si σ(z) ≥ 0.5 → clase 1, si σ(z) < 0.5 → clase 0</p>

<h4>Función de costo (Binary Cross-Entropy)</h4>
<p>Cost = -[y × log(ŷ) + (1-y) × log(1-ŷ)]</p>

<p>Referencia: <em>"Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow"</em> de Aurélien Géron (3ra edición, O\'Reilly 2022), Capítulos 4 y 10.</p>''', order=1)

CourseContent.objects.create(course=course2, section_type='explicacion', title='Árboles de Decisión, Random Forest y SVM', content='''<h3>Árboles de Decisión</h3>
<p>Modelo que divide los datos recursivamente basándose en reglas de decisión. Criterios de división:</p>
<ul>
<li><strong>Gini Impurity:</strong> G = 1 - Σ(pᵢ)²</li>
<li><strong>Entropy (Information Gain):</strong> H = -Σ(pᵢ × log₂(pᵢ))</li>
</ul>

<h3>Random Forest</h3>
<p>Ensemble de múltiples árboles de decisión usando <strong>bagging</strong> (Bootstrap Aggregating). Cada árbol se entrena con una muestra aleatoria del dataset y un subconjunto aleatorio de características.</p>
<p>Predicción final: promedio (regresión) o votación mayoritaria (clasificación).</p>

<h3>Support Vector Machines (SVM)</h3>
<p>Encuentra el hiperplano que maximiza el margen entre clases. Conceptos clave:</p>
<ul>
<li><strong>Vector soporte:</strong> Puntos de datos más cercanos al hiperplano.</li>
<li><strong>Kernel trick:</strong> Transforma datos no linealmente separables a un espacio de mayor dimensión.</li>
<li><strong>Kernels comunes:</strong> Lineal, Polinomial, RBF (Radial Basis Function)</li>
</ul>
<p>RBF: K(x, x\') = exp(-γ × ||x - x\'||²)</p>

<p>Referencia: <em>"Pattern Recognition and Machine Learning"</em> de Christopher Bishop (Springer, 2006), Capítulos 6 y 7.</p>''', order=2)

CourseContent.objects.create(course=course2, section_type='explicacion', title='Clustering: K-Means y DBSCAN', content='''<h3>K-Means</h3>
<p>Algoritmo de clustering particional que divide los datos en K grupos:</p>

<ol>
<li>Inicializar K centroides aleatoriamente.</li>
<li>Asignar cada punto al centroide más cercano (distancia euclidiana).</li>
<li>Recalcular centroides como la media de los puntos asignados.</li>
<li>Repetir hasta convergencia.</li>
</ol>

<p><strong>Método del codo:</strong> Graficar la inercia (suma de distancias al cuadrado) vs. K para encontrar el número óptimo de clusters.</p>

<h3>DBSCAN (Density-Based Spatial Clustering)</h3>
<p>Algoritmo basado en densidad que no requiere especificar el número de clusters:</p>
<ul>
<li><strong>ε (epsilon):</strong> Radio de vecindad.</li>
<li><strong>min_samples:</strong> Número mínimo de puntos para formar un cluster.</li>
<li>Ventaja: detecta clusters de forma arbitraria y puntos de ruido (outliers).</li>
</ul>

<p>Referencia: Ester et al. (1996), <em>"A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise"</em>, KDD-96.</p>''', order=3)

CourseContent.objects.create(course=course2, section_type='ejemplo', title='Ejemplo: Regresión Lineal con Scikit-Learn', content='''<h3>Predicción de precios de casas con regresión lineal</h3>

<pre><code>from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Dataset de ejemplo: tamaño (m²) y precio ($)
X = np.array([[50], [75], [100], [125], [150], [175], [200], [225], [250], [300]])
y = np.array([150000, 200000, 280000, 330000, 400000, 450000, 520000, 580000, 650000, 780000])

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Predicciones
y_pred = model.predict(X_test)

# Evaluación
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Coeficiente (pendiente): ${model.coef_[0]:.2f} por m²")
print(f"Intercepto: ${model.intercept_:.2f}")
print(f"MSE: ${mse:,.2f}")
print(f"R²: {r2:.4f}")
# R² cercano a 1 indica un buen ajuste
</code></pre>''', order=4)

CourseContent.objects.create(course=course2, section_type='ejemplo', title='Ejemplo: Clasificación con Random Forest', content='''<h3>Clasificación del dataset Iris con Random Forest</h3>

<pre><code>from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Cargar dataset Iris (150 muestras, 4 características, 3 clases)
iris = load_iris()
X = iris.data  # sepal_length, sepal_width, petal_length, petal_width
y = iris.target  # 0=setosa, 1=versicolor, 2=virginica

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entrenar Random Forest
rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf.fit(X_train, y_train)

# Evaluar
y_pred = rf.predict(X_test)
print("Matriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\\nReporte de clasificación:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# Importancia de características
importances = rf.feature_importances_
for name, imp in zip(iris.feature_names, importances):
    print(f"{name}: {imp:.4f}")
</code></pre>''', order=5)

CourseContent.objects.create(course=course2, section_type='demo', title='Demo: Validación cruzada y optimización de hiperparámetros', content='''<h3>GridSearchCV con validación cruzada</h3>

<pre><code>from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

# Dataset de cáncer de mama (569 muestras, 30 características)
data = load_breast_cancer()
X, y = data.data, data.target

# Escalar características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Definir grid de hiperparámetros
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# GridSearchCV con validación cruzada de 5 folds
rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(
    rf, param_grid, 
    cv=5, 
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)
grid_search.fit(X_scaled, y)

print(f"Mejores parámetros: {grid_search.best_params_}")
print(f"Mejor accuracy: {grid_search.best_score_:.4f}")

# Validación cruzada del mejor modelo
best_model = grid_search.best_estimator_
cv_scores = cross_val_score(best_model, X_scaled, y, cv=10)
print(f"Accuracy CV (10 folds): {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
</code></pre>''', order=6)

exam2 = Exam.objects.create(course=course2, title='Examen: Machine Learning', description='Evaluación de algoritmos y conceptos de Machine Learning', passing_score=70, time_limit_minutes=45)

q1 = Question.objects.create(exam=exam2, text='¿Qué función usa la regresión logística para predecir probabilidades?', order=1)
QuestionOption.objects.create(question=q1, text='Función sigmoide', is_correct=True, order=1)
QuestionOption.objects.create(question=q1, text='Función ReLU', is_correct=False, order=2)
QuestionOption.objects.create(question=q1, text='Función softmax', is_correct=False, order=3)
QuestionOption.objects.create(question=q1, text='Función lineal', is_correct=False, order=4)

q2 = Question.objects.create(exam=exam2, text='¿Qué técnica usa Random Forest para combinar múltiples árboles?', order=2)
QuestionOption.objects.create(question=q2, text='Boosting', is_correct=False, order=1)
QuestionOption.objects.create(question=q2, text='Bagging (Bootstrap Aggregating)', is_correct=True, order=2)
QuestionOption.objects.create(question=q2, text='Stacking', is_correct=False, order=3)
QuestionOption.objects.create(question=q2, text='Dropout', is_correct=False, order=4)

q3 = Question.objects.create(exam=exam2, text='¿Qué métrica indica la proporción de varianza explicada por un modelo de regresión?', order=3)
QuestionOption.objects.create(question=q3, text='MSE', is_correct=False, order=1)
QuestionOption.objects.create(question=q3, text='R² (Coeficiente de determinación)', is_correct=True, order=2)
QuestionOption.objects.create(question=q3, text='MAE', is_correct=False, order=3)
QuestionOption.objects.create(question=q3, text='Accuracy', is_correct=False, order=4)

q4 = Question.objects.create(exam=exam2, text='¿Cuál es la principal ventaja de DBSCAN sobre K-Means?', order=4)
QuestionOption.objects.create(question=q4, text='Es más rápido', is_correct=False, order=1)
QuestionOption.objects.create(question=q4, text='No requiere especificar el número de clusters y detecta outliers', is_correct=True, order=2)
QuestionOption.objects.create(question=q4, text='Siempre produce mejores resultados', is_correct=False, order=3)
QuestionOption.objects.create(question=q4, text='Solo funciona con datos lineales', is_correct=False, order=4)

q5 = Question.objects.create(exam=exam2, text='¿Qué es el "kernel trick" en SVM?', order=5)
QuestionOption.objects.create(question=q5, text='Una técnica de regularización', is_correct=False, order=1)
QuestionOption.objects.create(question=q5, text='Transformar datos a un espacio de mayor dimensión para hacerlos linealmente separables', is_correct=True, order=2)
QuestionOption.objects.create(question=q5, text='Un método de selección de características', is_correct=False, order=3)
QuestionOption.objects.create(question=q5, text='Una forma de reducir el overfitting', is_correct=False, order=4)

q6 = Question.objects.create(exam=exam2, text='¿Qué método se usa comúnmente para encontrar el número óptimo de clusters en K-Means?', order=6)
QuestionOption.objects.create(question=q6, text='Método del codo (Elbow Method)', is_correct=True, order=1)
QuestionOption.objects.create(question=q6, text='Gradiente descendente', is_correct=False, order=2)
QuestionOption.objects.create(question=q6, text='Backpropagation', is_correct=False, order=3)
QuestionOption.objects.create(question=q6, text='Cross-validation', is_correct=False, order=4)

print(f"Curso 2: {course2.title} - Contenido agregado")

# ============================================================
# CURSO 3: Redes Neuronales
# ============================================================
course3 = Course.objects.get(id=3)

CourseContent.objects.create(course=course3, section_type='explicacion', title='Del Perceptrón a las Redes Profundas', content='''<h3>El Perceptrón (Rosenblatt, 1958)</h3>
<p>El perceptrón es la unidad más básica de una red neuronal. Recibe entradas, las pondera, suma y aplica una función de activación:</p>

<p>y = f(Σ(wᵢ × xᵢ) + b)</p>

<p>Donde w son los pesos, x las entradas, b el sesgo y f la función de activación.</p>

<h3>Backpropagation (Rumelhart, Hinton & Williams, 1986)</h3>
<p>Algoritmo fundamental para entrenar redes neuronales multicapa. Propaga el error desde la salida hacia las capas internas, calculando gradientes con la regla de la cadena.</p>

<p>∂Loss/∂w = ∂Loss/∂output × ∂output/∂z × ∂z/∂w</p>

<h3>Arquitectura de una red profunda</h3>
<ul>
<li><strong>Capa de entrada:</strong> Recibe los datos (n neuronas = n características).</li>
<li><strong>Capas ocultas:</strong> Transforman los datos mediante combinaciones lineales + activación no lineal.</li>
<li><strong>Capa de salida:</strong> Produce la predicción final.</li>
</ul>

<p>Referencia: <em>"Deep Learning"</em> de Ian Goodfellow, Yoshua Bengio y Aaron Courville (MIT Press, 2016), Capítulos 6 y 8.</p>''', order=1)

CourseContent.objects.create(course=course3, section_type='explicacion', title='Funciones de Activación y Optimizadores', content='''<h3>Funciones de Activación</h3>

<h4>ReLU (Rectified Linear Unit)</h4>
<p>f(x) = max(0, x)</p>
<ul><li>Ventaja: computacionalmente eficiente, no sufre vanishing gradient para x > 0</li>
<li>Problema: "Dying ReLU" — neuronas que siempre outputean 0</li></ul>

<h4>Sigmoid</h4>
<p>f(x) = 1 / (1 + e⁻ˣ)</p>
<ul><li>Rango: (0, 1) — ideal para salida de clasificación binaria</li>
<li>Problema: vanishing gradient para valores extremos</li></ul>

<h4>Tanh</h4>
<p>f(x) = (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ)</p>
<ul><li>Rango: (-1, 1) — zero-centered, mejor que sigmoid para capas ocultas</li></ul>

<h4>GELU (Gaussian Error Linear Unit)</h4>
<p>f(x) = x × Φ(x) donde Φ es la CDF normal estándar</p>
<ul><li>Usado en transformers (BERT, GPT)</li></ul>

<h3>Optimizadores</h3>
<ul>
<li><strong>SGD:</strong> w = w - η × ∇L (η = learning rate)</li>
<li><strong>SGD con Momentum:</strong> Agrega inercia para acelerar la convergencia</li>
<li><strong>Adam:</strong> Combina momentum y RMSProp. Adapta el learning rate por parámetro. Es el optimizador más usado en la práctica.</li>
</ul>

<p>Referencia: Kingma & Ba (2014), <em>"Adam: A Method for Stochastic Optimization"</em>, arXiv:1412.6980.</p>''', order=2)

CourseContent.objects.create(course=course3, section_type='explicacion', title='Regularización: Dropout y Batch Normalization', content='''<h3>Overfitting</h3>
<p>Ocurre cuando el modelo memoriza los datos de entrenamiento en lugar de aprender patrones generalizables. Señales: accuracy de entrenamiento >> accuracy de validación.</p>

<h3>Dropout (Srivastava et al., 2014)</h3>
<p>Durante el entrenamiento, "apaga" aleatoriamente un porcentaje de neuronas en cada iteración:</p>
<ul>
<li>Previene co-adaptación de neuronas.</li>
<li>Funciona como ensemble de múltiples sub-redes.</li>
<li>Típicamente: dropout_rate = 0.2 a 0.5</li>
</ul>

<h3>Batch Normalization (Ioffe & Szegedy, 2015)</h3>
<p>Normaliza las activaciones de cada capa para tener media 0 y varianza 1:</p>
<p>x̂ = (x - μ_batch) / √(σ²_batch + ε)</p>
<p>y = γ × x̂ + β (parámetros aprendibles)</p>

<p>Ventajas:</p>
<ul>
<li>Permite learning rates más altos.</li>
<li>Reduce la dependencia de la inicialización.</li>
<li>Actúa como regularizador leve.</li>
</ul>

<p>Referencia: <em>"Deep Learning"</em> de Goodfellow et al., Capítulo 7 (Regularization).</p>''', order=3)

CourseContent.objects.create(course=course3, section_type='ejemplo', title='Ejemplo: Red neuronal desde cero con NumPy', content='''<h3>Clasificación XOR con una red neuronal manual</h3>

<pre><code>import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def sigmoid_derivative(x):
    return x * (1 - x)

# Red: 2 inputs -> 3 hidden -> 1 output
np.random.seed(42)
w1 = np.random.randn(2, 3)
b1 = np.zeros(3)
w2 = np.random.randn(3, 1)
b2 = np.zeros(1)

# Datos XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

lr = 1.0
for epoch in range(5000):
    # Forward
    z1 = X @ w1 + b1
    a1 = sigmoid(z1)
    z2 = a1 @ w2 + b2
    a2 = sigmoid(z2)
    
    # Backward
    error = y - a2
    d2 = error * sigmoid_derivative(a2)
    d1 = (d2 @ w2.T) * sigmoid_derivative(a1)
    
    # Update
    w2 += a1.T @ d2 * lr
    b2 += np.sum(d2, axis=0) * lr
    w1 += X.T @ d1 * lr
    b1 += np.sum(d1, axis=0) * lr

# Resultados
print("Resultados XOR:")
for i in range(4):
    print(f"  {X[i]} -> {a2[i][0]:.4f} (esperado: {y[i][0]})")

# Accuracy
preds = (a2 >= 0.5).astype(int)
acc = np.mean(preds == y) * 100
print(f"\\nAccuracy: {acc:.1f}%")
</code></pre>''', order=4)

CourseContent.objects.create(course=course3, section_type='ejemplo', title='Ejemplo: Visualización de funciones de activación', content='''<h3>Comparación gráfica de funciones de activación</h3>

<pre><code>import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x = np.linspace(-6, 6, 400)

# Funciones de activación
def relu(x):
    return np.maximum(0, x)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def gelu(x):
    # Aproximacion: x * sigmoid(1.702 * x)
    return x / (1 + np.exp(-1.702 * x))

# Crear gráfico
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Funciones de Activación", fontsize=14)

functions = [
    (relu, "ReLU", "red"),
    (sigmoid, "Sigmoid", "blue"),
    (tanh, "Tanh", "green"),
    (gelu, "GELU", "purple"),
]

for i, (fn, name, color) in enumerate(functions):
    ax = axes[i // 2, i % 2]
    try:
        y = fn(x)
        ax.plot(x, y, color=color, linewidth=2)
        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.axvline(x=0, color="gray", linewidth=0.5)
        ax.set_title(name, fontsize=12)
        ax.grid(True, alpha=0.3)
    except Exception:
        ax.text(0.5, 0.5, f"{name}\\n(requiere scipy)", 
                ha="center", va="center", transform=ax.transAxes)

plt.tight_layout()
plt.savefig("/tmp/activation_functions.png", dpi=100)
print("Gráfico guardado en /tmp/activation_functions.png")
print("\\nPropiedades:")
print(f"  ReLU(2)  = {relu(2):.1f}")
print(f"  ReLU(-2) = {relu(-2):.1f}")
print(f"  Sigmoid(0) = {sigmoid(0):.4f}")
print(f"  Tanh(0)    = {tanh(0):.4f}")
</code></pre>''', order=5)

CourseContent.objects.create(course=course3, section_type='demo', title='Demo: Visualización de backpropagation', content='''<h3>Simulación simplificada de backpropagation</h3>

<pre><code>import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Red simple: 2 inputs -> 2 hidden -> 1 output
np.random.seed(42)
weights_input_hidden = np.random.randn(2, 2)
weights_hidden_output = np.random.randn(2, 1)
bias_hidden = np.zeros((1, 2))
bias_output = np.zeros((1, 1))

# Datos de ejemplo: compuerta XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

learning_rate = 0.5

for epoch in range(10000):
    # Forward pass
    hidden_input = np.dot(X, weights_input_hidden) + bias_hidden
    hidden_output = sigmoid(hidden_input)
    
    final_input = np.dot(hidden_output, weights_hidden_output) + bias_output
    final_output = sigmoid(final_input)
    
    # Backward pass
    error = y - final_output
    d_output = error * sigmoid_derivative(final_output)
    
    error_hidden = d_output.dot(weights_hidden_output.T)
    d_hidden = error_hidden * sigmoid_derivative(hidden_output)
    
    # Actualizar pesos
    weights_hidden_output += hidden_output.T.dot(d_output) * learning_rate
    weights_input_hidden += X.T.dot(d_hidden) * learning_rate
    bias_output += np.sum(d_output, axis=0, keepdims=True) * learning_rate
    bias_hidden += np.sum(d_hidden, axis=0, keepdims=True) * learning_rate

# Resultados
print("Resultados después del entrenamiento:")
for i in range(4):
    print(f"Input: {X[i]} -> Output: {final_output[i][0]:.4f} (Expected: {y[i][0]})")
</code></pre>''', order=6)

exam3 = Exam.objects.create(course=course3, title='Examen: Redes Neuronales', description='Evaluación de arquitecturas y conceptos de redes neuronales profundas', passing_score=70, time_limit_minutes=45)

q1 = Question.objects.create(exam=exam3, text='¿Qué algoritmo se usa para calcular gradientes en redes neuronales multicapa?', order=1)
QuestionOption.objects.create(question=q1, text='Backpropagation', is_correct=True, order=1)
QuestionOption.objects.create(question=q1, text='K-Means', is_correct=False, order=2)
QuestionOption.objects.create(question=q1, text='Gradient Boosting', is_correct=False, order=3)
QuestionOption.objects.create(question=q1, text='Simulated Annealing', is_correct=False, order=4)

q2 = Question.objects.create(exam=exam3, text='¿Cuál es la principal ventaja de ReLU sobre sigmoid?', order=2)
QuestionOption.objects.create(question=q2, text='No sufre vanishing gradient para valores positivos', is_correct=True, order=1)
QuestionOption.objects.create(question=q2, text='Produce valores entre 0 y 1', is_correct=False, order=2)
QuestionOption.objects.create(question=q2, text='Es más compleja matemáticamente', is_correct=False, order=3)
QuestionOption.objects.create(question=q2, text='Solo funciona en la capa de salida', is_correct=False, order=4)

q3 = Question.objects.create(exam=exam3, text='¿Qué hace la técnica de Dropout durante el entrenamiento?', order=3)
QuestionOption.objects.create(question=q3, text='Apaga aleatoriamente un porcentaje de neuronas en cada iteración', is_correct=True, order=1)
QuestionOption.objects.create(question=q3, text='Aumenta el learning rate dinámicamente', is_correct=False, order=2)
QuestionOption.objects.create(question=q3, text='Elimina las capas ocultas innecesarias', is_correct=False, order=3)
QuestionOption.objects.create(question=q3, text='Normaliza los datos de entrada', is_correct=False, order=4)

q4 = Question.objects.create(exam=exam3, text='¿Qué optimizador combina momentum y RMSProp adaptando el learning rate por parámetro?', order=4)
QuestionOption.objects.create(question=q4, text='SGD', is_correct=False, order=1)
QuestionOption.objects.create(question=q4, text='Adam', is_correct=True, order=2)
QuestionOption.objects.create(question=q4, text='Adagrad', is_correct=False, order=3)
QuestionOption.objects.create(question=q4, text='RMSProp', is_correct=False, order=4)

q5 = Question.objects.create(exam=exam3, text='¿Qué es una GAN (Generative Adversarial Network)?', order=5)
QuestionOption.objects.create(question=q5, text='Un sistema con dos redes: generador y discriminador que compiten entre sí', is_correct=True, order=1)
QuestionOption.objects.create(question=q5, text='Una red neuronal para clasificación de imágenes', is_correct=False, order=2)
QuestionOption.objects.create(question=q5, text='Un algoritmo de clustering', is_correct=False, order=3)
QuestionOption.objects.create(question=q5, text='Una técnica de regularización', is_correct=False, order=4)

print(f"Curso 3: {course3.title} - Contenido agregado")

# ============================================================
# CURSO 4: Lenguaje Natural (NLP)
# ============================================================
course4 = Course.objects.get(id=4)

CourseContent.objects.create(course=course4, section_type='explicacion', title='Tokenización, Stemming y Lematización', content='''<h3>Tokenización</h3>
<p>Proceso de dividir texto en unidades más pequeñas (tokens). Tipos:</p>
<ul>
<li><strong>Tokenización por palabras:</strong> "El gato come" → ["El", "gato", "come"]</li>
<li><strong>Tokenización por subpalabras:</strong> "unhappiness" → ["un", "happi", "ness"] (usada en BERT/GPT)</li>
<li><strong>Byte-Pair Encoding (BPE):</strong> Algoritmo usado por GPT-2, GPT-3 y GPT-4 para manejar vocabulario abierto.</li>
</ul>

<h3>Stemming</h3>
<p>Reduce palabras a su raíz mediante reglas heurísticas (a veces produce raíces no válidas):</p>
<ul>
<li><strong>Porter Stemmer:</strong> "running" → "run", "studies" → "studi"</li>
<li><strong>Snowball Stemmer:</strong> Versión mejorada de Porter, soporta múltiples idiomas.</li>
</ul>

<h3>Lematización</h3>
<p>Reduce palabras a su forma canónica (lema) usando diccionarios y análisis morfológico:</p>
<ul>
<li>"better" → "good" (adjetivo)</li>
<li>"went" → "go" (verbo)</li>
<li>"mice" → "mouse" (sustantivo)</li>
</ul>

<p>Herramientas: NLTK, spaCy, Hugging Face Tokenizers.</p>

<p>Referencia: <em>"Speech and Language Processing"</em> de Jurafsky & Martin (3ra edición, 2024), Capítulo 2.</p>''', order=1)

CourseContent.objects.create(course=course4, section_type='explicacion', title='Word Embeddings: Word2Vec, GloVe y FastText', content='''<h3>Word2Vec (Mikolov et al., Google, 2013)</h3>
<p>Representa palabras como vectores densos en un espacio continuo. Dos arquitecturas:</p>
<ul>
<li><strong>CBOW (Continuous Bag of Words):</strong> Predice la palabra objetivo dado su contexto.</li>
<li><strong>Skip-gram:</strong> Predice el contexto dada la palabra objetivo. Mejor para palabras raras.</li>
</ul>

<p>Propiedad famosa: <strong>king - man + woman ≈ queen</strong></p>

<h3>GloVe (Pennington et al., Stanford, 2014)</h3>
<p>Combina estadísticas globales de co-ocurrencia con aprendizaje local. Construye una matriz de co-ocurrencia y factoriza para obtener embeddings.</p>

<h3>FastText (Bojanowski et al., Facebook, 2016)</h3>
<p>Extensión de Word2Vec que representa palabras como bags of character n-grams:</p>
<ul>
<li>Ventaja: puede generar embeddings para palabras no vistas (OOV).</li>
<li>Ejemplo: "donde" → ["<do", "don", "ond", "nde", "de>", ...]</li>
<li>Especialmente útil para idiomas con morfología rica como el español.</li>
</ul>

<p>Dimensiones típicas: 50, 100, 200 o 300.</p>''', order=2)

CourseContent.objects.create(course=course4, section_type='explicacion', title='Transformers: BERT, GPT y Fine-Tuning', content='''<h3>Arquitectura Transformer (Vaswani et al., 2017)</h3>
<p>Reemplaza las RNNs con el mecanismo de <strong>Self-Attention</strong>:</p>
<p>Attention(Q, K, V) = softmax(QKᵀ/√dₖ)V</p>

<p>Donde Q (Query), K (Key), V (Value) son proyecciones lineales de las entradas.</p>

<h3>BERT (Devlin et al., Google, 2018)</h3>
<ul>
<li><strong>Bidireccional:</strong> Ve el contexto completo (izquierda y derecha).</li>
<li><strong>Pre-entrenamiento:</strong> Masked Language Modeling (MLM) + Next Sentence Prediction (NSP).</li>
<li><strong>Variantes:</strong> BERT-base (110M params), BERT-large (340M params), RoBERTa, DistilBERT, ALBERT.</li>
</ul>

<h3>GPT (OpenAI, 2018-2024)</h3>
<ul>
<li><strong>Unidireccional (autoregresivo):</strong> Predice la siguiente palabra.</li>
<li><strong>GPT-3 (2020):</strong> 175B parámetros, few-shot learning.</li>
<li><strong>GPT-4 (2023):</strong> Multimodal, ~1.76T parámetros (estimado).</li>
</ul>

<h3>Fine-Tuning con Hugging Face</h3>
<p>Proceso de adaptar un modelo pre-entrenado a una tarea específica:</p>
<ol>
<li>Cargar modelo pre-entrenado (ej: bert-base-spanish).</li>
<li>Agregar capa de clasificación sobre la salida del [CLS] token.</li>
<li>Entrenar con datos etiquetados de la tarea específica.</li>
</ol>

<p>Referencia: <em>"Natural Language Processing with Transformers"</em> de Tunstall, von Werra y Wolf (O\'Reilly, 2022).</p>''', order=3)

CourseContent.objects.create(course=course4, section_type='ejemplo', title='Ejemplo: Análisis de sentimiento con Naive Bayes', content='''<h3>Clasificador de sentimiento desde cero</h3>

<pre><code>from collections import Counter
import math

# Dataset de entrenamiento
train_data = [
    ("me encanta este curso excelente", "pos"),
    ("increible muy bueno fantastico", "pos"),
    ("me gusta mucho perfecto genial", "pos"),
    ("terrible malo pesimo horrible", "neg"),
    ("no me gusta nada decepcionante", "neg"),
    ("horrible malisimo no sirve", "neg"),
]

# Entrenar: contar palabras por clase
word_counts = {"pos": Counter(), "neg": Counter()}
class_counts = {"pos": 0, "neg": 0}
total_words = {"pos": 0, "neg": 0}

for text, label in train_data:
    words = text.split()
    class_counts[label] += 1
    word_counts[label].update(words)
    total_words[label] += len(words)

def predict(text):
    words = text.split()
    total = sum(class_counts.values())
    
    scores = {}
    for label in ["pos", "neg"]:
        # Log probabilidad previa
        score = math.log(class_counts[label] / total)
        # Log probabilidad de cada palabra (con smoothing)
        for w in words:
            count = word_counts[label].get(w, 0)
            score += math.log((count + 1) / (total_words[label] + len(word_counts[label])))
        scores[label] = score
    
    return "pos" if scores["pos"] > scores["neg"] else "neg"

# Probar
tests = [
    "excelente curso me encanta",
    "terrible no me gusta nada",
    "bueno pero podria mejorar",
]
for t in tests:
    print(f"'{t}' -> {predict(t)}")
</code></pre>''', order=4)

CourseContent.objects.create(course=course4, section_type='ejemplo', title='Ejemplo: Tokenización y análisis de texto', content='''<h3>Procesamiento de texto en español con Python puro</h3>

<pre><code>import re
from collections import Counter

# Texto de ejemplo
text = """La inteligencia artificial es una rama de las ciencias
de la computacion que se enfoca en crear sistemas capaces de
realizar tareas que requieren inteligencia humana."""

# Tokenización
tokens = re.findall(r'\b[a-záéíóúñü]+\b', text.lower())
print(f"Total de tokens: {len(tokens)}")
print(f"Tokens unicos: {len(set(tokens))}")

# Frecuencia de palabras
freq = Counter(tokens)
print("\\nTop 10 palabras mas frecuentes:")
for word, count in freq.most_common(10):
    bar = "#" * count
    print(f"  {word:15} {bar} ({count})")

# N-grams (bigramas)
bigrams = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
bigram_freq = Counter(bigrams)
print("\\nTop 5 bigramas:")
for bg, count in bigram_freq.most_common(5):
    print(f"  '{bg[0]} {bg[1]}' ({count})")

# Estadísticas
avg_word_len = sum(len(w) for w in tokens) / len(tokens)
print(f"\\nLongitud promedio de palabra: {avg_word_len:.1f}")
print(f"Vocabulario rico (type/token): {len(set(tokens))/len(tokens):.3f}")
</code></pre>''', order=5)

CourseContent.objects.create(course=course4, section_type='demo', title='Demo: Word embeddings con TF-IDF y similitud de coseno', content='''<h3>Representación vectorial de documentos y similitud</h3>

<pre><code>import math
from collections import Counter

# Documentos de ejemplo
docs = [
    "la inteligencia artificial transforma la tecnologia",
    "el machine learning es parte de la inteligencia artificial",
    "las redes neuronales profundas aprenden patrones complejos",
    "python es un lenguaje popular para machine learning",
    "la vision computacional usa redes neuronales convolucionales",
]

# Crear vocabulario
vocab = set()
for doc in docs:
    vocab.update(doc.split())
vocab = sorted(vocab)
word_to_idx = {w: i for i, w in enumerate(vocab)}

# TF-IDF
def compute_tf(doc):
    words = doc.split()
    return Counter(words)

def compute_idf(docs, word):
    n_docs_with_word = sum(1 for d in docs if word in d.split())
    return math.log(len(docs) / (1 + n_docs_with_word))

# Calcular vectores TF-IDF
tfidf_matrix = []
for doc in docs:
    tf = compute_tf(doc)
    vector = []
    for word in vocab:
        tfidf = tf.get(word, 0) * compute_idf(docs, word)
        vector.append(tfidf)
    tfidf_matrix.append(vector)

def cosine_sim(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a*a for a in v1))
    norm2 = math.sqrt(sum(b*b for b in v2))
    return dot / (norm1 * norm2) if norm1 and norm2 else 0

# Comparar documentos
print("Matriz de similitud (coseno):")
print(f"{'':>45}", end="")
for i in range(len(docs)):
    print(f"Doc{i+1:>6}", end="")
print()

for i, doc in enumerate(docs):
    print(f"Doc{i+1} {doc[:40]:40}", end="")
    for j in range(len(docs)):
        sim = cosine_sim(tfidf_matrix[i], tfidf_matrix[j])
        print(f"{sim:6.3f}", end="")
    print()

print("\\nDocumentos más similares:")
best_sim = 0
best_pair = (0, 0)
for i in range(len(docs)):
    for j in range(i+1, len(docs)):
        sim = cosine_sim(tfidf_matrix[i], tfidf_matrix[j])
        if sim > best_sim:
            best_sim = sim
            best_pair = (i, j)
print(f"  Doc{best_pair[0]+1} <-> Doc{best_pair[1]+1}: {best_sim:.4f}")
</code></pre>''', order=6)

exam4 = Exam.objects.create(course=course4, title='Examen: Procesamiento de Lenguaje Natural', description='Evaluación de conceptos de NLP, embeddings y transformers', passing_score=70, time_limit_minutes=45)

q1 = Question.objects.create(exam=exam4, text='¿Cuál es la diferencia principal entre stemming y lematización?', order=1)
QuestionOption.objects.create(question=q1, text='El stemming usa reglas heurísticas y la lematización usa análisis morfológico con diccionarios', is_correct=True, order=1)
QuestionOption.objects.create(question=q1, text='Son exactamente lo mismo', is_correct=False, order=2)
QuestionOption.objects.create(question=q1, text='La lematización es más rápida que el stemming', is_correct=False, order=3)
QuestionOption.objects.create(question=q1, text='El stemming solo funciona en inglés', is_correct=False, order=4)

q2 = Question.objects.create(exam=exam4, text='¿Qué propiedad famosa demuestra Word2Vec?', order=2)
QuestionOption.objects.create(question=q2, text='king - man + woman ≈ queen', is_correct=True, order=1)
QuestionOption.objects.create(question=q2, text='cat + dog = pet', is_correct=False, order=2)
QuestionOption.objects.create(question=q2, text='hot + cold = warm', is_correct=False, order=3)
QuestionOption.objects.create(question=q2, text='big × small = medium', is_correct=False, order=4)

q3 = Question.objects.create(exam=exam4, text='¿Qué mecanismo reemplazó a las RNNs en la arquitectura Transformer?', order=3)
QuestionOption.objects.create(question=q3, text='Self-Attention', is_correct=True, order=1)
QuestionOption.objects.create(question=q3, text='Convolution', is_correct=False, order=2)
QuestionOption.objects.create(question=q3, text='Pooling', is_correct=False, order=3)
QuestionOption.objects.create(question=q3, text='Dropout', is_correct=False, order=4)

q4 = Question.objects.create(exam=exam4, text='¿Cuál es la diferencia principal entre BERT y GPT?', order=4)
QuestionOption.objects.create(question=q4, text='BERT es bidireccional y GPT es unidireccional (autoregresivo)', is_correct=True, order=1)
QuestionOption.objects.create(question=q4, text='BERT es más grande que GPT', is_correct=False, order=2)
QuestionOption.objects.create(question=q4, text='GPT es para clasificación y BERT para generación', is_correct=False, order=3)
QuestionOption.objects.create(question=q4, text='No hay diferencia significativa', is_correct=False, order=4)

q5 = Question.objects.create(exam=exam4, text='¿Qué ventaja tiene FastText sobre Word2Vec?', order=5)
QuestionOption.objects.create(question=q5, text='Puede generar embeddings para palabras no vistas usando character n-grams', is_correct=True, order=1)
QuestionOption.objects.create(question=q5, text='Es más rápido en todos los casos', is_correct=False, order=2)
QuestionOption.objects.create(question=q5, text='No necesita datos de entrenamiento', is_correct=False, order=3)
QuestionOption.objects.create(question=q5, text='Solo funciona con inglés', is_correct=False, order=4)

print(f"Curso 4: {course4.title} - Contenido agregado")

# ============================================================
# CURSO 5: Visión Computacional
# ============================================================
course5 = Course.objects.get(id=5)

CourseContent.objects.create(course=course5, section_type='explicacion', title='Redes Convolucionales (CNN) desde cero', content='''<h3>¿Qué es una convolución?</h3>
<p>Una convolución aplica un filtro (kernel) sobre una imagen para extraer características:</p>
<p>Output[i,j] = Σ Σ Input[i+m, j+n] × Kernel[m, n]</p>

<h3>Componentes de una CNN</h3>

<h4>Capa Convolucional</h4>
<ul>
<li><strong>Kernels/filtros:</strong> Matrices pequeñas (3×3, 5×5) que detectan patrones como bordes, texturas.</li>
<li><strong>Stride:</strong> Cuántos píxeles se mueve el filtro.</li>
<li><strong>Padding:</strong> Relleno para preservar dimensiones (SAME, VALID).</li>
</ul>

<h4>Capa de Pooling</h4>
<ul>
<li><strong>Max Pooling:</strong> Toma el valor máximo de una región (2×2 típico).</li>
<li><strong>Average Pooling:</strong> Promedia los valores de una región.</li>
<li>Propósito: reducir dimensionalidad y hacer la representación invariante a pequeñas traslaciones.</li>
</ul>

<h4>Capa Fully Connected</h4>
<p>Después de las capas convolucionales, se aplanan las características y se conectan a capas densas para la clasificación final.</p>

<p>Referencia: <em>"Deep Learning"</em> de Goodfellow et al., Capítulo 9 (Convolutional Networks).</p>''', order=1)

CourseContent.objects.create(course=course5, section_type='explicacion', title='Arquitecturas clásicas: AlexNet, VGG, ResNet, EfficientNet', content='''<h3>AlexNet (Krizhevsky et al., 2012)</h3>
<ul>
<li>8 capas (5 conv + 3 FC).</li>
<li>Ganó ImageNet 2012 con 15.3% de error (vs 25.8% del segundo lugar).</li>
<li>Introdujo ReLU y Dropout en visión computacional.</li>
<li>Primera red en usar GPUs (NVIDIA GTX 580) para entrenamiento.</li>
</ul>

<h3>VGG (Simonyan & Zisserman, Oxford, 2014)</h3>
<ul>
<li>Usa solo filtros 3×3 apilados (VGG-16: 16 capas, VGG-19: 19 capas).</li>
<li>Demostró que la profundidad es clave para el rendimiento.</li>
<li>Muy usada como backbone para transfer learning.</li>
</ul>

<h3>ResNet (He et al., Microsoft, 2015)</h3>
<ul>
<li>Introdujo <strong>skip connections</strong> (conexiones residuales): y = F(x) + x</li>
<li>Permite entrenar redes muy profundas (ResNet-50, ResNet-101, ResNet-152).</li>
<li>Ganó ImageNet 2015 con 3.57% de error (superó la precisión humana de ~5%).</li>
</ul>

<h3>EfficientNet (Tan & Le, Google, 2019)</h3>
<ul>
<li>Compound scaling: escala uniformemente profundidad, anchura y resolución.</li>
<li>Mejor relación precisión/eficiencia que arquitecturas anteriores.</li>
<li>EfficientNet-B7 logra 84.4% top-1 accuracy en ImageNet.</li>
</ul>''', order=2)

CourseContent.objects.create(course=course5, section_type='explicacion', title='Detección de objetos: YOLO y Faster R-CNN', content='''<h3>Faster R-CNN (Ren et al., 2015)</h3>
<p>Arquitectura de dos etapas:</p>
<ol>
<li><strong>Region Proposal Network (RPN):</strong> Genera regiones candidatas que pueden contener objetos.</li>
<li><strong>Fast R-CNN:</strong> Clasifica cada región y refina las bounding boxes.</li>
</ol>
<p>Ventaja: alta precisión. Desventaja: lento para tiempo real.</p>

<h3>YOLO (You Only Look Once, Redmon et al., 2016)</h3>
<p>Arquitectura de una sola etapa que detecta objetos en una pasada:</p>
<ul>
<li>Divide la imagen en una cuadrícula S×S.</li>
<li>Cada celda predica B bounding boxes + confianzas + clases.</li>
<li><strong>YOLOv8 (Ultralytics, 2023):</strong> Estado del arte en velocidad/precisión.</li>
<li>Capaz de detectar 80 clases de objetos en tiempo real (>30 FPS).</li>
</ul>

<h3>Métricas de evaluación</h3>
<ul>
<li><strong>IoU (Intersection over Union):</strong> IoU = Área(intersección) / Área(unión)</li>
<li><strong>mAP (mean Average Precision):</strong> Promedio de AP sobre todas las clases.</li>
<li><strong>FPS:</strong> Frames por segundo (velocidad de inferencia).</li>
</ul>

<p>Referencia: <em>"Deep Learning for Computer Vision"</em> de Rajalingappan (Packt, 2022).</p>''', order=3)

CourseContent.objects.create(course=course5, section_type='ejemplo', title='Ejemplo: Operaciones de convolución con NumPy', content='''<h3>Implementación manual de una convolución 2D</h3>

<pre><code>import numpy as np

def convolve2d(image, kernel):
    """Aplica una convolución 2D a una imagen."""
    kh, kw = kernel.shape
    ih, iw = image.shape
    oh = ih - kh + 1
    ow = iw - kw + 1
    output = np.zeros((oh, ow))
    
    for i in range(oh):
        for j in range(ow):
            output[i, j] = np.sum(
                image[i:i+kh, j:j+kw] * kernel
            )
    return output

# Imagen de ejemplo (8x8)
image = np.zeros((8, 8))
image[2:6, 2:6] = 1.0  # Cuadrado blanco en centro
print("Imagen original (8x8):")
for row in image:
    print("  " + "".join(f"{v:2.0f}" for v in row))

# Kernel detector de bordes (Sobel horizontal)
sobel_x = np.array([[-1, -2, -1],
                     [ 0,  0,  0],
                     [ 1,  2,  1]])

# Kernel detector de bordes (Sobel vertical)
sobel_y = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

# Aplicar convoluciones
edges_x = convolve2d(image, sobel_x)
edges_y = convolve2d(image, sobel_y)

print("\\nBordes horizontales (Sobel X):")
for row in np.abs(edges_x):
    print("  " + "".join(f"{abs(v):3.0f}" for v in row))

print("\\nBordes verticales (Sobel Y):")
for row in np.abs(edges_y):
    print("  " + "".join(f"{abs(v):3.0f}" for v in row))

# Magnitud total de bordes
magnitude = np.sqrt(edges_x**2 + edges_y**2)
print("\\nMagnitud de bordes:")
for row in magnitude:
    print("  " + "".join(f"{v:4.1f}" for v in row))
</code></pre>''', order=4)

CourseContent.objects.create(course=course5, section_type='ejemplo', title='Ejemplo: Procesamiento de imágenes con NumPy', content='''<h3>Manipulación de imágenes como arrays numéricos</h3>

<pre><code>import numpy as np

# Crear una imagen sintética (gradiente)
height, width = 16, 16
img = np.zeros((height, width), dtype=np.float64)

# Gradiente horizontal
for x in range(width):
    img[:, x] = x / (width - 1)

print("Gradiente horizontal (16x16):")
for row in img:
    print("  " + "".join(f"{v:4.2f}" for v in row))

# Operaciones de imagen
print("\\nOperaciones:")
print(f"  Min: {img.min():.2f}")
print(f"  Max: {img.max():.2f}")
print(f"  Media: {img.mean():.2f}")
print(f"  Desviación: {img.std():.2f}")

# Normalización
img_norm = (img - img.min()) / (img.max() - img.min())
print(f"\\nDespués de normalizar:")
print(f"  Min: {img_norm.min():.2f}")
print(f"  Max: {img_norm.max():.2f}")

# Umbralización (binarización)
threshold = 0.5
img_binary = (img > threshold).astype(int)
print(f"\\nBinarización (threshold={threshold}):")
for row in img_binary:
    print("  " + "".join(f"{v:2d}" for v in row))

# Filtro de promedio (blur 3x3)
def blur(image, size=3):
    result = np.zeros_like(image)
    pad = size // 2
    for i in range(pad, image.shape[0] - pad):
        for j in range(pad, image.shape[1] - pad):
            result[i, j] = np.mean(
                image[i-pad:i+pad+1, j-pad:j+pad+1]
            )
    return result

img_blurred = blur(img)
print(f"\\nDespués de blur 3x3 (centro):")
print(f"  Valor central: {img_blurred[8, 8]:.4f}")
print(f"  Valor original: {img[8, 8]:.4f}")
</code></pre>''', order=5)

CourseContent.objects.create(course=course5, section_type='demo', title='Demo: Detección de patrones con template matching', content='''<h3>Template matching: encontrar patrones en imágenes</h3>

<pre><code>import numpy as np

def template_match(image, template):
    """
    Template matching usando correlación normalizada.
    Encuentra la mejor posición del template en la imagen.
    """
    ih, iw = image.shape
    th, tw = template.shape
    oh = ih - th + 1
    ow = iw - tw + 1
    
    best_score = -1
    best_pos = (0, 0)
    
    for i in range(oh):
        for j in range(ow):
            patch = image[i:i+th, j:j+tw]
            # Correlación normalizada
            num = np.sum(patch * template)
            den = np.sqrt(np.sum(patch**2) * np.sum(template**2))
            score = num / den if den > 0 else 0
            if score > best_score:
                best_score = score
                best_pos = (i, j)
    
    return best_pos, best_score

# Crear imagen con patrón
image = np.zeros((10, 10))
# Dibujar una cruz en la imagen
image[3:7, 4:6] = 1
image[4:6, 2:8] = 1

# Template: la cruz que queremos encontrar
template = np.ones((5, 5))
template[0, :] = 0
template[4, :] = 0
template[:, 0] = 0
template[:, 4] = 0
template[2, 2] = 1

print("Imagen (10x10):")
for row in image:
    print("  " + "".join(f"{v:2.0f}" for v in row))

print("\\nTemplate (5x5):")
for row in template:
    print("  " + "".join(f"{v:2.0f}" for v in row))

# Encontrar el template
(pos_row, pos_col), score = template_match(image, template)
print(f"\\nMejor coincidencia:")
print(f"  Posición: fila={pos_row}, col={pos_col}")
print(f"  Score: {score:.4f}")

# Marcar la posición encontrada
result = image.copy()
result[pos_row:pos_row+5, pos_col:pos_col+5] = 0.5
print("\\nResultado (0.5 = posición encontrada):")
for row in result:
    print("  " + "".join(f"{v:4.1f}" for v in row))
</code></pre>''', order=6)

exam5 = Exam.objects.create(course=course5, title='Examen: Visión Computacional', description='Evaluación de CNNs, arquitecturas y detección de objetos', passing_score=70, time_limit_minutes=45)

q1 = Question.objects.create(exam=exam5, text='¿Qué operación matemática aplica un filtro sobre una imagen en una CNN?', order=1)
QuestionOption.objects.create(question=q1, text='Convolución', is_correct=True, order=1)
QuestionOption.objects.create(question=q1, text='Correlación cruzada', is_correct=False, order=2)
QuestionOption.objects.create(question=q1, text='Transformada de Fourier', is_correct=False, order=3)
QuestionOption.objects.create(question=q1, text='Multiplicación matricial', is_correct=False, order=4)

q2 = Question.objects.create(exam=exam5, text='¿Qué innovación introdujo ResNet que permite entrenar redes muy profundas?', order=2)
QuestionOption.objects.create(question=q2, text='Skip connections (conexiones residuales)', is_correct=True, order=1)
QuestionOption.objects.create(question=q2, text='Dropout', is_correct=False, order=2)
QuestionOption.objects.create(question=q2, text='Batch Normalization', is_correct=False, order=3)
QuestionOption.objects.create(question=q2, text='Data augmentation', is_correct=False, order=4)

q3 = Question.objects.create(exam=exam5, text='¿Cuál es la principal diferencia entre YOLO y Faster R-CNN?', order=3)
QuestionOption.objects.create(question=q3, text='YOLO es de una sola etapa (más rápido) y Faster R-CNN es de dos etapas (más preciso)', is_correct=True, order=1)
QuestionOption.objects.create(question=q3, text='YOLO solo detecta una clase y Faster R-CNN detecta múltiples', is_correct=False, order=2)
QuestionOption.objects.create(question=q3, text='Faster R-CNN es más rápido que YOLO', is_correct=False, order=3)
QuestionOption.objects.create(question=q3, text='No hay diferencia significativa', is_correct=False, order=4)

q4 = Question.objects.create(exam=exam5, text='¿Qué métrica mide la superposición entre una bounding box predicha y la ground truth?', order=4)
QuestionOption.objects.create(question=q4, text='IoU (Intersection over Union)', is_correct=True, order=1)
QuestionOption.objects.create(question=q4, text='Accuracy', is_correct=False, order=2)
QuestionOption.objects.create(question=q4, text='F1 Score', is_correct=False, order=3)
QuestionOption.objects.create(question=q4, text='MSE', is_correct=False, order=4)

q5 = Question.objects.create(exam=exam5, text='¿Qué ganó AlexNet en 2012 que revolucionó la visión computacional?', order=5)
QuestionOption.objects.create(question=q5, text='ImageNet Classification Challenge con 15.3% de error', is_correct=True, order=1)
QuestionOption.objects.create(question=q5, text='El premio Turing', is_correct=False, order=2)
QuestionOption.objects.create(question=q5, text='La competencia de detección de objetos COCO', is_correct=False, order=3)
QuestionOption.objects.create(question=q5, text='El premio Nobel de Física', is_correct=False, order=4)

print(f"Curso 5: {course5.title} - Contenido agregado")

# ============================================================
# CURSO 6: Proyecto Final
# ============================================================
course6 = Course.objects.get(id=6)

CourseContent.objects.create(course=course6, section_type='explicacion', title='Definición del problema y recolección de datos', content='''<h3>Fase 1: Definición del problema</h3>
<p>Todo proyecto de IA exitoso comienza con una definición clara del problema:</p>

<ol>
<li><strong>Identificar el problema de negocio:</strong> ¿Qué decisión o proceso queremos mejorar?</li>
<li><strong>Formular como problema de ML:</strong> Clasificación, regresión, clustering, generación, etc.</li>
<li><strong>Definir métricas de éxito:</strong> Accuracy, precision, recall, F1, ROI, etc.</li>
<li><strong>Evaluar viabilidad:</strong> ¿Hay datos disponibles? ¿Es factible técnicamente?</li>
</ol>

<h3>Fase 2: Recolección y preparación de datos</h3>

<h4>Fuentes de datos</h4>
<ul>
<li><strong>APIs públicas:</strong> Kaggle, UCI ML Repository, Hugging Face Datasets, Google Dataset Search.</li>
<li><strong>Web scraping:</strong> BeautifulSoup, Scrapy, Selenium (respetando robots.txt y términos de uso).</li>
<li><strong>Datos internos:</strong> Bases de datos de la organización (SQL, NoSQL).</li>
</ul>

<h4>Limpieza de datos</h4>
<ul>
<li>Manejo de valores faltantes: imputación (media, mediana, KNN) o eliminación.</li>
<li>Detección y tratamiento de outliers: IQR method, Z-score.</li>
<li>Balanceo de clases: SMOTE, undersampling, class weights.</li>
</ul>

<h4>Feature Engineering</h4>
<ul>
<li>Encoding de variables categóricas: one-hot, label encoding, target encoding.</li>
<li>Escalamiento: StandardScaler, MinMaxScaler, RobustScaler.</li>
<li>Creación de features: polinomiales, interacciones, agregaciones temporales.</li>
</ul>

<p>Referencia: <em>"Designing Machine Learning Systems"</em> de Chip Huyen (O\'Reilly, 2022).</p>''', order=1)

CourseContent.objects.create(course=course6, section_type='explicacion', title='Despliegue en producción con Docker y APIs REST', content='''<h3>Contenedores con Docker</h3>
<p>Docker empaqueta la aplicación con todas sus dependencias para garantizar consistencia entre entornos.</p>

<pre><code># Dockerfile ejemplo para modelo ML
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "http.server", "8000"]
</code></pre>

<p><em>Nota: Este Dockerfile es de referencia. En la terminal del curso puedes usar Python directamente sin Docker.</em></p>

<h3>API REST con Python estándar</h3>
<p>Python incluye el módulo <code>http.server</code> en su biblioteca estándar para crear servidores web sin dependencias externas:</p>

<pre><code>from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"status": "healthy"}
            self.wfile.write(json.dumps(response).encode())

server = HTTPServer("0.0.0.0", 8000, Handler)
print("Servidor en http://localhost:8000")
server.serve_forever()
</code></pre>

<h3>Alternativas populares</h3>
<ul>
<li><strong>FastAPI:</strong> Framework moderno con validación automática y documentación Swagger.</li>
<li><strong>Flask:</strong> Framework ligero y flexible para APIs simples.</li>
<li><strong>Django REST Framework:</strong> Ideal si ya usas Django.</li>
</ul>

<p>Referencia: <em>"Building Machine Learning Powered Applications"</em> de Emmanuel Ameisen (O\'Reilly, 2020).</p>''', order=2)

CourseContent.objects.create(course=course6, section_type='explicacion', title='Metodologías ágiles y documentación técnica', content='''<h3>Metodologías Ágiles para proyectos de IA</h3>

<h4>Scrum</h4>
<ul>
<li><strong>Sprints:</strong> Iteraciones de 2-4 semanas con entregables definidos.</li>
<li><strong>Daily standup:</strong> Reunión de 15 min: ¿Qué hice? ¿Qué haré? ¿Bloqueos?</li>
<li><strong>Sprint planning:</strong> Definir qué se entregará en el sprint.</li>
<li><strong>Sprint review:</strong> Demo del trabajo completado.</li>
<li><strong>Retrospectiva:</strong> ¿Qué funcionó? ¿Qué mejorar?</li>
</ul>

<h4>Kanban</h4>
<ul>
<li>Tablero visual con columnas: To Do → In Progress → Review → Done.</li>
<li>Limitar work-in-progress (WIP) para evitar sobrecarga.</li>
</ul>

<h3>Documentación técnica</h3>
<ul>
<li><strong>README.md:</strong> Descripción del proyecto, instalación, uso.</li>
<li><strong>Model Card (Mitchell et al., Google, 2018):</strong> Documenta el modelo: intención, datos de entrenamiento, métricas, limitaciones, consideraciones éticas.</li>
<li><strong>Datasheet for Datasets (Gebru et al., 2018):</strong> Documenta el dataset: motivación, composición, proceso de recolección, sesgos conocidos.</li>
<li><strong>API Documentation:</strong> Swagger/OpenAPI para APIs REST.</li>
</ul>

<h3>Presentación ejecutiva</h3>
<ol>
<li>Problema de negocio y oportunidad.</li>
<li>Solución propuesta y enfoque técnico.</li>
<li>Resultados y métricas clave.</li>
<li>Impacto esperado y ROI.</li>
<li>Próximos pasos y recomendaciones.</li>
</ol>''', order=3)

CourseContent.objects.create(course=course6, section_type='ejemplo', title='Ejemplo: Pipeline completo de ML con scikit-learn', content='''<h3>Pipeline end-to-end: desde datos hasta predicción</h3>

<pre><code>import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

# Crear dataset sintético
np.random.seed(42)
n_samples = 200

# Features: edad, ingresos, score
X = np.column_stack([
    np.random.randint(18, 65, n_samples),
    np.random.uniform(20000, 100000, n_samples),
    np.random.uniform(0, 100, n_samples),
])

# Target: 0 o 1 basado en una regla
y = (X[:, 0] > 30).astype(int) & (X[:, 1] > 50000).astype(int)
y = y.astype(int)

print(f"Dataset: {X.shape[0]} muestras, {X.shape[1]} features")
print(f"Distribución de clases: {np.bincount(y)}")

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Pipeline: escalar + clasificar
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(
        n_estimators=50, max_depth=5, random_state=42
    ))
])

# Entrenar
pipeline.fit(X_train, y_train)

# Evaluar
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred, target_names=["No compra", "Compra"]))

# Guardar modelo con pickle
with open("model.pkl", "wb") as f:
    pickle.dump(pipeline, f)
print("Modelo guardado en model.pkl")

# Cargar y predecir
with open("model.pkl", "rb") as f:
    loaded = pickle.load(f)

new_data = np.array([[35, 60000, 75]])
pred = loaded.predict(new_data)
print(f"\\nNueva predicción: {'Compra' if pred[0] else 'No compra'}")
</code></pre>''', order=4)

CourseContent.objects.create(course=course6, section_type='ejemplo', title='Ejemplo: Model Card para documentación de modelo', content='''<h3>Model Card template (formato Markdown)</h3>

<pre><code># Model Card: Clasificador de Spam en Español

## Model Details
- **Nombre:** spam-classifier-es-v1
- **Tipo:** Random Forest (scikit-learn)
- **Fecha:** 2026-01-15
- **Autores:** Equipo de IA

## Intended Use
- **Uso principal:** Clasificar emails como spam o no spam en español.
- **Uso fuera de alcance:** No usar para otros idiomas sin re-entrenamiento.

## Training Data
- **Fuente:** Dataset propio de 50,000 emails etiquetados.
- **Distribución:** 70% ham, 30% spam.
- **Periodo:** Emails recolectados entre 2024-2025.
- **Preprocesamiento:** Tokenización, TF-IDF, eliminación de stopwords.

## Metrics
| Métrica | Valor |
|---------|-------|
| Accuracy | 0.967 |
| Precision (spam) | 0.952 |
| Recall (spam) | 0.941 |
| F1 Score | 0.946 |
| AUC-ROC | 0.983 |

## Limitations
- Rendimiento reducido en emails con jerga muy específica.
- No detecta spam en imágenes (OCR no implementado).
- Sesgo potencial hacia dominios de email más comunes.

## Ethical Considerations
- Los emails fueron anonimizados antes del entrenamiento.
- Se implementó revisión humana para casos borderline.
- Los falsos positivos se revisan manualmente antes de acciones.
</code></pre>''', order=5)

CourseContent.objects.create(course=course6, section_type='demo', title='Demo: API REST simple con http.server de Python', content='''<h3>Servidor HTTP con modelo ML integrado</h3>

<pre><code>import json
import numpy as np
from http.server import HTTPServer, BaseHTTPRequestHandler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Entrenar modelo
np.random.seed(42)
X_train = np.random.randn(100, 3)
y_train = (X_train[:, 0] + X_train[:, 1] > 0).astype(int)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_scaled, y_train)

class MLHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/predict":
            content_length = int(self.headers["Content-Length"])
            body = json.loads(self.rfile.read(content_length))
            
            features = np.array([body["features"]])
            features_scaled = scaler.transform(features)
            pred = int(model.predict(features_scaled)[0])
            prob = float(model.predict_proba(features_scaled)[0].max())
            
            response = {"prediction": pred, "probability": prob}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == "/health":
            response = {"status": "healthy", "model": "loaded"}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        elif self.path == "/docs":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = """&lt;html&gt;&lt;body&gt;
            &lt;h1&gt;ML Prediction API&lt;/h1&gt;
            &lt;p&gt;POST /predict {"features": [1.0, 2.0, 3.0]}&lt;/p&gt;
            &lt;p&gt;GET /health&lt;/p&gt;
            &lt;/body&gt;&lt;/html&gt;"""
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Silenciar logs

print("Servidor corriendo en http://localhost:8000")
print("Endpoints:")
print("  GET  /health  - Estado del servicio")
print("  GET  /docs    - Documentación")
print("  POST /predict - Predicción")
print()

# Ejemplo de uso sin iniciar servidor
print("=== Demo sin servidor (simulación) ===")
test_features = [[1.0, 2.0, 3.0], [-1.0, -2.0, -3.0]]
for features in test_features:
    feat = np.array([features])
    feat_scaled = scaler.transform(feat)
    pred = int(model.predict(feat_scaled)[0])
    prob = float(model.predict_proba(feat_scaled)[0].max())
    print(f"  Input: {features}")
    print(f"  Predicción: {pred} (probabilidad: {prob:.4f})")
    print()
</code></pre>''', order=6)

exam6 = Exam.objects.create(course=course6, title='Examen: Proyecto Final de IA', description='Evaluación de conceptos de despliegue, metodologías y documentación', passing_score=70, time_limit_minutes=45)

q1 = Question.objects.create(exam=exam6, text='¿Cuál es el primer paso en todo proyecto de machine learning?', order=1)
QuestionOption.objects.create(question=q1, text='Definir claramente el problema de negocio', is_correct=True, order=1)
QuestionOption.objects.create(question=q1, text='Elegir el algoritmo más avanzado', is_correct=False, order=2)
QuestionOption.objects.create(question=q1, text='Recopilar la mayor cantidad de datos posible', is_correct=False, order=3)
QuestionOption.objects.create(question=q1, text='Entrenar un modelo deep learning', is_correct=False, order=4)

q2 = Question.objects.create(exam=exam6, text='¿Qué técnica se usa para manejar clases desbalanceadas en un dataset?', order=2)
QuestionOption.objects.create(question=q2, text='SMOTE (Synthetic Minority Over-sampling Technique)', is_correct=True, order=1)
QuestionOption.objects.create(question=q2, text='Batch Normalization', is_correct=False, order=2)
QuestionOption.objects.create(question=q2, text='Dropout', is_correct=False, order=3)
QuestionOption.objects.create(question=q2, text='Cross-validation', is_correct=False, order=4)

q3 = Question.objects.create(exam=exam6, text='¿Qué herramienta se usa para empaquetar una aplicación con todas sus dependencias?', order=3)
QuestionOption.objects.create(question=q3, text='Docker', is_correct=True, order=1)
QuestionOption.objects.create(question=q3, text='Git', is_correct=False, order=2)
QuestionOption.objects.create(question=q3, text='Jupyter', is_correct=False, order=3)
QuestionOption.objects.create(question=q3, text='TensorFlow', is_correct=False, order=4)

q4 = Question.objects.create(exam=exam6, text='¿Qué es una Model Card?', order=4)
QuestionOption.objects.create(question=q4, text='Un documento que describe la intención, datos, métricas, limitaciones y consideraciones éticas de un modelo', is_correct=True, order=1)
QuestionOption.objects.create(question=q4, text='Una tarjeta de presentación del equipo de desarrollo', is_correct=False, order=2)
QuestionOption.objects.create(question=q4, text='Un archivo de configuración del modelo', is_correct=False, order=3)
QuestionOption.objects.create(question=q4, text='Un tipo de red neuronal', is_correct=False, order=4)

q5 = Question.objects.create(exam=exam6, text='¿Qué framework de Python es recomendado para crear APIs REST rápidas con documentación automática?', order=5)
QuestionOption.objects.create(question=q5, text='FastAPI', is_correct=True, order=1)
QuestionOption.objects.create(question=q5, text='Django', is_correct=False, order=2)
QuestionOption.objects.create(question=q5, text='Flask', is_correct=False, order=3)
QuestionOption.objects.create(question=q5, text='Streamlit', is_correct=False, order=4)

q6 = Question.objects.create(exam=exam6, text='¿Qué metodología ágil usa sprints de 2-4 semanas con daily standups y retrospectivas?', order=6)
QuestionOption.objects.create(question=q6, text='Scrum', is_correct=True, order=1)
QuestionOption.objects.create(question=q6, text='Waterfall', is_correct=False, order=2)
QuestionOption.objects.create(question=q6, text='Kanban', is_correct=False, order=3)
QuestionOption.objects.create(question=q6, text='Six Sigma', is_correct=False, order=4)

print(f"Curso 6: {course6.title} - Contenido agregado")

print("\n" + "="*60)
print("TODOS LOS CURSOS HAN SIDO ACTUALIZADOS CON CONTENIDO")
print("="*60)
print("\nResumen:")
for i, course in enumerate([course1, course2, course3, course4, course5, course6], 1):
    contents = course.contents.count()
    exams = course.exams.count()
    questions = sum(e.questions.count() for e in course.exams.all())
    print(f"  Curso {i}: {course.title}")
    print(f"    - {contents} contenidos (explicaciones, ejemplos, demos)")
    print(f"    - {exams} examen(es) con {questions} preguntas")
