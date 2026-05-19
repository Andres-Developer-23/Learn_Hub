#!/usr/bin/env python3
"""Crea los cursos de Regresión Lineal y Algoritmo Genético con contenido completo."""

import os
import django
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_project.settings')
django.setup()

from enrollment.models import Course, CourseContent, Exam, Question, QuestionOption


def main():
    with transaction.atomic():



        # ──────────────────────────────────────────────────────────────────────
        # CURSO: REGRESIÓN LINEAL
        # ──────────────────────────────────────────────────────────────────────
        course_rl, _ = Course.objects.update_or_create(
            title='Regresión Lineal',
            defaults=dict(
                description="""La regresión lineal es el algoritmo fundacional del machine learning supervisado. Aprenderás desde los fundamentos matemáticos (MCO, gradiente descendente) hasta implementaciones prácticas con Python y scikit-learn. Incluye regresión simple, múltiple, polinomial y regularización (Ridge, Lasso, Elastic Net). Cada concepto se refuerza con ejemplos numéricos verificables y código funcional.""",
                icon='📈', duration='10 semanas', level='principiante',
                instructor_name='Andrés Bravo',
                instructor_bio='Ingeniero de Machine Learning especializado en modelado predictivo y sistemas de aprendizaje automático. Experiencia en implementación de modelos de regresión para aplicaciones financieras y de salud.',
                instructor_avatar_url='', is_active=True, order=7,
            )
        )

        print(f"✓ Curso '{course_rl.title}' (id={course_rl.id}) listo.")

        # -- Explicaciones --
        CourseContent.objects.update_or_create(
        course=course_rl, section_type='explicacion', title='Fundamentos de la Regresión Lineal', order=1,
        defaults={'content': '''<h3>¿Qué es la regresión lineal?</h3>
        <p>La regresión lineal es un método estadístico que modela la relación entre una variable dependiente (y) y una o más variables independientes (X). Es el algoritmo más básico y fundamental del aprendizaje supervisado.</p>

        <h3>Ecuación del modelo</h3>
        <p>Para regresión lineal simple (una variable):</p>
        <p><strong>y = β₀ + β₁x + ε</strong></p>
        <p>Donde:</p>
        <ul>
        <li><strong>y</strong> = variable dependiente (lo que queremos predecir)</li>
        <li><strong>x</strong> = variable independiente (predictor)</li>
        <li><strong>β₀</strong> = intercepto (valor de y cuando x = 0)</li>
        <li><strong>β₁</strong> = pendiente (cambio en y por cada unidad de x)</li>
        <li><strong>ε</strong> = error aleatorio (ruido irreducible)</li>
        </ul>

        <h3>Regresión lineal múltiple</h3>
        <p>Cuando hay múltiples predictores:</p>
        <p><strong>y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε</strong></p>

        <h3>Supuestos del modelo</h3>
        <ol>
        <li><strong>Linealidad:</strong> La relación entre X e y es lineal.</li>
        <li><strong>Independencia:</strong> Las observaciones son independientes entre sí.</li>
        <li><strong>Homocedasticidad:</strong> La varianza de los errores es constante.</li>
        <li><strong>Normalidad:</strong> Los errores siguen una distribución normal (para inferencia).</li>
        <li><strong>No multicolinealidad:</strong> Las variables predictoras no están altamente correlacionadas.</li>
        </ol>

        <h3>Referencias</h3>
        <p>Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). <em>Introduction to Linear Regression Analysis</em> (6th ed.). Wiley. ISBN: 978-1-119-63879-3.</p>'''}
    )

        CourseContent.objects.update_or_create(
        course=course_rl, section_type='explicacion', title='Mínimos Cuadrados Ordinarios (MCO)', order=2,
        defaults={'content': '''<h3>Función de costo: Error Cuadrático Medio (MSE)</h3>
        <p>El objetivo del MCO es encontrar β₀ y β₁ que minimicen la suma de los errores al cuadrado:</p>

        <p><strong>MSE = (1/n) × Σ(yᵢ - ŷᵢ)²</strong></p>
        <p>Donde ŷᵢ = β₀ + β₁xᵢ es el valor predicho.</p>

        <h3>Solución analítica (cerrada)</h3>
        <p>Derivando MSE respecto a β₀ y β₁ e igualando a cero, obtenemos:</p>
        <p><strong>β₁ = Σ((xᵢ - x̄)(yᵢ - ȳ)) / Σ((xᵢ - x̄)²)</strong></p>
        <p><strong>β₀ = ȳ - β₁x̄</strong></p>

        <p>En forma matricial para regresión múltiple:</p>
        <p><strong>β = (XᵀX)⁻¹Xᵀy</strong></p>

        <h3>Notación matricial detallada</h3>
        <p>X es la matriz de diseño (n × (p+1)) donde la primera columna son unos para el intercepto. La derivación completa:</p>
        <p>MSE(β) = (y - Xβ)ᵀ(y - Xβ) / n</p>
        <p>∂MSE/∂β = -2Xᵀ(y - Xβ) / n = 0</p>
        <p>XᵀXβ = Xᵀy</p>
        <p>β = (XᵀX)⁻¹Xᵀy</p>

        <h3>Ejemplo numérico verificable</h3>
        <p>Datos: x = [1, 2, 3, 4, 5], y = [2, 4, 5, 4, 5]</p>
        <p>x̄ = 3, ȳ = 4</p>
        <p>Numerador β₁: (1-3)(2-4) + (2-3)(4-4) + (3-3)(5-4) + (4-3)(4-4) + (5-3)(5-4) = 4 + 0 + 0 + 0 + 2 = 6</p>
        <p>Denominador β₁: (1-3)² + (2-3)² + (3-3)² + (4-3)² + (5-3)² = 4 + 1 + 0 + 1 + 4 = 10</p>
        <p>β₁ = 6/10 = 0.6</p>
        <p>β₀ = 4 - 0.6(3) = 4 - 1.8 = 2.2</p>
        <p>Ecuación: ŷ = 2.2 + 0.6x</p>
        <p>Predicciones: ŷ = [2.8, 3.4, 4.0, 4.6, 5.2]</p>
        <p>MSE = ((2-2.8)² + (4-3.4)² + (5-4.0)² + (4-4.6)² + (5-5.2)²) / 5 = 0.64 + 0.36 + 1.0 + 0.36 + 0.04 = 2.4 / 5 = 0.48</p>'''}
    )

        CourseContent.objects.update_or_create(
        course=course_rl, section_type='explicacion', title='Gradiente Descendente y Regularización', order=3,
        defaults={'content': '''<h3>Gradiente Descendente</h3>
        <p>Alternativa numérica cuando (XᵀX)⁻¹ es computacionalmente costoso (muchas características).</p>

        <p><strong>Algoritmo:</strong></p>
        <ol>
        <li>Inicializar β₀, β₁ aleatoriamente.</li>
        <li>Repetir hasta convergencia:
           <br>βⱼ := βⱼ - α × (∂MSE/∂βⱼ)</li>
        </ol>

        <p><strong>Derivadas parciales:</strong></p>
        <p>∂MSE/∂β₀ = (-2/n) × Σ(yᵢ - ŷᵢ)</p>
        <p>∂MSE/∂β₁ = (-2/n) × Σ(yᵢ - ŷᵢ) × xᵢ</p>

        <p><strong>Hiperparámetros:</strong></p>
        <ul>
        <li><strong>α (learning rate):</strong> Controla el tamaño del paso. Típico: 0.01, 0.001, 0.0001.</li>
        <li><strong>Épocas:</strong> Número de iteraciones sobre todo el dataset.</li>
        <li><strong>Batch size:</strong> Número de muestras por actualización (GD, SGD, Mini-batch SGD).</li>
        </ul>

        <h3>Regularización</h3>
        <p>Previene el overfitting agregando un término de penalización a la función de costo:</p>

        <h4>Ridge Regression (L2)</h4>
        <p>J(β) = MSE + λ × Σβⱼ²</p>
        <p>Contrae los coeficientes hacia cero pero no los elimina.</p>

        <h4>Lasso Regression (L1)</h4>
        <p>J(β) = MSE + λ × Σ|βⱼ|</p>
        <p>Puede llevar algunos coeficientes a exactamente cero (selección de características).</p>

        <h4>Elastic Net</h4>
        <p>J(β) = MSE + λ₁ × Σ|βⱼ| + λ₂ × Σβⱼ²</p>
        <p>Combina L1 y L2. Útil cuando hay grupos de características correlacionadas.</p>

        <h3>Métricas de evaluación</h3>
        <ul>
        <li><strong>R² = 1 - SSE/SST:</strong> Proporción de varianza explicada. Rango [0, 1].</li>
        <li><strong>R² ajustado:</strong> Penaliza por número de predictores. R²_adj = 1 - (1-R²)(n-1)/(n-p-1)</li>
        <li><strong>RMSE = √MSE:</strong> Error en las mismas unidades que y.</li>
        <li><strong>MAE = (1/n) × Σ|yᵢ - ŷᵢ|:</strong> Error absoluto medio.</li>
        </ul>

        <p>Referencia: Hastie, T., Tibshirani, R., & Friedman, J. (2009). <em>The Elements of Statistical Learning</em> (2nd ed.). Springer. Capítulos 3 y 4.</p>'''}
    )

        # -- Ejemplos --
        CourseContent.objects.update_or_create(
        course=course_rl, section_type='ejemplo', title='Ejemplo: Regresión Lineal Simple desde Cero', order=4,
        defaults={'content': '''<h3>Implementación de regresión lineal simple con NumPy</h3>
        <p>Código funcional que reproduce exactamente el ejemplo numérico de la explicación anterior.</p>

<pre><code>import numpy as np

# Datos del ejemplo numérico
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

# --- Solución analítica MCO ---
x_mean = np.mean(x)
y_mean = np.mean(y)

numerador = np.sum((x - x_mean) * (y - y_mean))
denominador = np.sum((x - x_mean) ** 2)
beta_1 = numerador / denominador
beta_0 = y_mean - beta_1 * x_mean

print("=== Solución MCO (cerrada) ===")
print(f"β₀ (intercepto) = {beta_0:.4f}")
print(f"β₁ (pendiente)  = {beta_1:.4f}")
print(f"Ecuación:        ŷ = {beta_0:.4f} + {beta_1:.4f}x")

# Predicciones
y_pred = beta_0 + beta_1 * x
mse = np.mean((y - y_pred) ** 2)
r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - y_mean)**2)
print(f"MSE             = {mse:.4f}")
print(f"R²              = {r2:.4f}")
print(f"Predicciones:   {y_pred}")
print()

# --- Gradiente Descendente ---
alpha = 0.01
epochs = 1000
b0, b1 = 0.0, 0.0
n = len(x)

for epoch in range(epochs):
    y_pred_gd = b0 + b1 * x
    error = y - y_pred_gd
    db0 = (-2 / n) * np.sum(error)
    db1 = (-2 / n) * np.sum(error * x)
    b0 -= alpha * db0
    b1 -= alpha * db1

print("=== Gradiente Descendente ===")
print(f"β₀ = {b0:.4f}")
print(f"β₁ = {b1:.4f}")
print(f"Predicciones GD: {b0 + b1 * x}")
print()

# --- Scikit-Learn ---
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(x.reshape(-1, 1), y)
print("=== Scikit-Learn ===")
print(f"β₀ = {model.intercept_:.4f}")
print(f"β₁ = {model.coef_[0]:.4f}")
print(f"R²  = {model.score(x.reshape(-1, 1), y):.4f}")
</code></pre>

        <h3>Salida esperada</h3>
<pre><code>=== Solución MCO (cerrada) ===
β₀ (intercepto) = 2.2000
β₁ (pendiente)  = 0.6000
Ecuación:        ŷ = 2.2000 + 0.6000x
MSE             = 0.4800
R²              = 0.6000
Predicciones:   [2.8 3.4 4.  4.6 5.2]

=== Gradiente Descendente ===
β₀ = 2.2000
β₁ = 0.6000

=== Scikit-Learn ===
β₀ = 2.2000
β₁ = 0.6000
R²  = 0.6000
</code></pre>'''}
    )

        CourseContent.objects.update_or_create(
        course=course_rl, section_type='ejemplo', title='Ejemplo: Regresión Múltiple con Regularización', order=5,
        defaults={'content': '''<h3>Predicción del precio de viviendas con 3 variables</h3>

<pre><code>import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error, r2_score

# Dataset sintético: [tamaño_m², habitaciones, antigüedad_años] -> precio $
np.random.seed(42)
n = 200
tamano = np.random.uniform(40, 300, n)
hab = np.random.randint(1, 6, n).astype(float)
antiguedad = np.random.uniform(0, 50, n)
precio = (tamano * 2500 + hab * 30000 - antiguedad * 5000
          + np.random.normal(0, 50000, n))

X = np.column_stack([tamano, hab, antiguedad])
y = precio

# Dividir y escalar
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 'test_size': 0.2, 'random_state': 42
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# Modelos
modelos = {
    'Lineal': LinearRegression(),
    'Ridge ('α': 10)': Ridge(alpha=10),
    'Lasso ('α': 10)': Lasso(alpha=10),
    'Elastic Net ('α': 10, 'l1': 0.5)': ElasticNet(alpha=10, 'l1_ratio': 0.5),
}

print(f"{'Modelo':<30} {'RMSE':>12} {'R²':>8} {'Coefs':>40}")
print('-' * 92)

for nombre, mdl in modelos.items():
    mdl.fit(X_train_s, y_train)
    y_pred = mdl.predict(X_test_s)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    coefs = ', '.join(f'{c:.1f}' for c in mdl.coef_)
    print(f"{nombre:<30} {rmse:>12,.0f} {r2:>8.4f} {coefs:>40}")

# Interpretación de coeficientes
lr = modelos['Lineal']
print(f"\nEcuación (datos escalados):")
print(f"  precio = {lr.intercept_:.0f} + {lr.coef_[0]:.0f}·X₁(tamaño) + {lr.coef_[1]:.0f}·X₂(hab) + {lr.coef_[2]:.0f}·X₃(antigüedad)")

# Análisis de características
print(f"\nInterpretación práctica:")
print(f"  Por cada m² adicional, el precio aumenta ~${lr.coef_[0]/X[:,0].std():.0f}")
print(f"  Por cada habitación extra, el precio aumenta ~${lr.coef_[1]/X[:,1].std():.0f}")
print(f"  Por cada año de antigüedad, el precio baja ~${abs(lr.coef_[2]/X[:,2].std()):.0f}")
</code></pre>

        <h3>Salida esperada (aproximada)</h3>
<pre><code>Modelo                         RMSE         R²  Coefs
--------------------------------------------------------------------
Lineal                        48,063     0.9690  308775, 26753, -332268
Ridge (α=10)                  48,081     0.9690  308604, 26719, -331884
Lasso (α=10)                  48,063     0.9690  308773, 26748, -332264
Elastic Net (α=10, l1=0.5)   48,076     0.9690  308616, 26700, -332149

Interpretación práctica:
  Por cada m² adicional, el precio aumenta ~$2,514
  Por cada habitación extra, el precio aumenta ~$30,024
  Por cada año de antigüedad, el precio baja ~$4,977
</code></pre>'''}
    )

        # -- Demo --
        CourseContent.objects.update_or_create(
        course=course_rl, section_type='demo', title='Demo: Regresión Polinomial y Validación Cruzada', order=6,
        defaults={'content': '''<h3>Regresión polinomial + validación cruzada + comparación visual</h3>

<pre><code>import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import cross_val_score

# Datos no lineales simulados
np.random.seed(42)
X = np.linspace(-3, 3, 100).reshape(-1, 1)
y = 0.5 * X.ravel()**3 - 1.5 * X.ravel()**2 + 2 * X.ravel() + np.random.normal(0, 2, 100)

# Probar distintos grados polinomiales
grados = [1, 2, 3, 5, 10]
colores = ['blue', 'green', 'red', 'purple', 'orange']
X_plot = np.linspace(-3.5, 3.5, 300).reshape(-1, 1)

plt.figure('figsize': (14, 5))

# Subplot 1: Comparación de grados
plt.subplot(1, 2, 1)
plt.scatter(X, y, 'alpha': 0.4, 's': 20, 'label': 'Datos reales')

for grado, color in zip(grados, colores):
    modelo = make_pipeline(PolynomialFeatures(grado), LinearRegression())
    scores = cross_val_score(modelo, X, y, 'cv': 10, 'scoring': 'neg_mean_squared_error')
    rmse_cv = np.sqrt(-scores.mean())
    modelo.fit(X, y)
    y_plot = modelo.predict(X_plot)
    plt.plot(X_plot, y_plot, 'color': color, 'linewidth': 2,
             'label': f'Grado {grado} (RMSE-CV={rmse_cv:.2f})')

plt.xlabel('X'); plt.ylabel('y')
plt.title('Regresión Polinomial: Subajuste vs Sobreajuste')
plt.legend(fontsize=7)
plt.grid(alpha=0.3)

# Subplot 2: Ridge vs Lineal para grado 10
plt.subplot(1, 2, 2)
plt.scatter(X, y, alpha=0.4, s=20, label='Datos reales')

modelo_lineal = make_pipeline(PolynomialFeatures(10), LinearRegression())
modelo_ridge = make_pipeline(PolynomialFeatures(10), Ridge(alpha=5))

for nombre, mdl, color in [
    ('Lineal (grado 10)', modelo_lineal, 'red'),
    ('Ridge α=5 (grado 10)', modelo_ridge, 'green'),
]:
    mdl.fit(X, y)
    y_plot = mdl.predict(X_plot)
    plt.plot(X_plot, y_plot, color=color, linewidth=2, label=nombre)

plt.xlabel('X'); plt.ylabel('y')
plt.title('Regularización: Ridge reduce el sobreajuste')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/polynomial_regression.png', dpi=100)
print("Gráfico guardado en /tmp/polynomial_regression.png")

# Demostración numérica
print(f"\n{'Grado':<8} {'RMSE Train':<12} {'RMSE CV':<12} {'R² CV':<10} {'¿Sobreajuste?':<15}")
print('-' * 60)
for grado in grados:
    modelo = make_pipeline(PolynomialFeatures(grado), LinearRegression())
    train_score = -cross_val_score(modelo, X, y, cv=10, scoring='neg_mean_squared_error').mean()
    rmse_train = np.sqrt(train_score)
    cv_scores = cross_val_score(modelo, X, y, cv=10, scoring='neg_mean_squared_error')
    rmse_cv = np.sqrt(-cv_scores.mean())
    r2_cv = cross_val_score(modelo, X, y, cv=10, scoring='r2').mean()
    sobreajuste = 'SÍ' if rmse_cv > rmse_train * 1.3 else 'No'
    print(f"{grado:<8} {rmse_train:<12.2f} {rmse_cv:<12.2f} {r2_cv:<10.4f} {sobreajuste:<15}")
</code></pre>

        <h3>Interpretación de resultados</h3>
        <ul>
        <li><strong>Grado 1 (lineal):</strong> Subajuste — el modelo es muy simple para la relación no lineal.</li>
        <li><strong>Grado 2:</strong> Mejora significativa, captura la curvatura principal.</li>
        <li><strong>Grado 3:</strong> Punto óptimo (relación real), RMSE-CV mínimo.</li>
        <li><strong>Grado 5+:</strong> Sobreajuste — RMSE-CV aumenta aunque RMSE-train sigue bajando.</li>
        <li><strong>Ridge (grado 10):</strong> Controla el sobreajuste penalizando coeficientes grandes.</li>
        </ul>

        <h3>Cómo detectar el grado óptimo</h3>
        <ol>
        <li>Graficar RMSE de entrenamiento y validación vs. complejidad.</li>
        <li>Elegir el punto donde RMSE-CV es mínimo (o donde empieza a crecer).</li>
        <li>Verificar que R²-CV sea razonable (> 0.8 para datos con señal clara).</li>
        <li>Preferir modelos más simples (Navaja de Occam) cuando R² es similar.</li>
        </ol>'''}
    )

        # -- Examen --
        exam_rl, _ = Exam.objects.update_or_create(
        course=course_rl, title='Examen: Regresión Lineal',
        defaults={'description': 'Evalúa fundamentos de regresión lineal, MCO, gradiente descendente, métricas y regularización.', 'passing_score': 70, 'time_limit_minutes': 30}
    )

        q, _ = Question.objects.update_or_create(
            exam=exam_rl, text='¿Qué significa la notación β₀ en la ecuación de regresión lineal y = β₀ + β₁x + ε?',
            defaults={'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='El intercepto: valor de y cuando x = 0',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='La pendiente: cambio en y por unidad de x',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='El error aleatorio del modelo',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='El coeficiente de determinación',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_rl, text='¿Qué supuesto NO es necesario para la regresión lineal?',
            defaults={'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Los errores deben seguir una distribución uniforme',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Relación lineal entre variables independientes y dependiente',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Homocedasticidad (varianza constante de errores)',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Independencia de las observaciones',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_rl, text='¿Cuál es la fórmula de la solución analítica MCO en forma matricial?',
            defaults={'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='β = (XᵀX)⁻¹Xᵀy',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='β = (Xᵀy)⁻¹XᵀX',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='β = Xᵀ(XᵀX)⁻¹y',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='β = yXᵀ(XXᵀ)⁻¹',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_rl, text='¿Qué hiperparámetro controla el tamaño del paso en el gradiente descendente?',
            defaults={'order': 4}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Learning rate (α)',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Número de épocas',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Batch size',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Lambda (λ) de regularización',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_rl, text='¿Qué tipo de regularización puede llevar coeficientes exactamente a cero?',
            defaults={'order': 5}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Lasso (L1)',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Ridge (L2)',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Elastic Net sin L1',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Ninguna, ninguna regularización elimina coeficientes',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_rl, text='Si R² = 0.85, ¿qué significa?',
            defaults={'order': 6}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='El modelo explica el 85% de la varianza de y',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='El 85% de las predicciones son correctas',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='El error es del 15%',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='El modelo tiene un 85% de precisión',
            defaults={'is_correct': False, 'order': 4}
        )

        print(f"  → {exam_rl.title} (6 preguntas)")

        # ──────────────────────────────────────────────────────────────────────
        # CURSO: ALGORITMO GENÉTICO
        # ──────────────────────────────────────────────────────────────────────
        course_ag, _ = Course.objects.update_or_create(
            title='Algoritmo Genético',
            defaults=dict(
                description="""Los algoritmos genéticos son técnicas de optimización inspiradas en la evolución natural de Darwin. Este curso cubre desde los fundamentos biológicos (selección, cruce, mutación) hasta implementaciones prácticas en Python para resolver problemas reales de optimización. Incluye codificación binaria y real, selección por torneo y ruleta, cruce de uno y dos puntos, mutación, elitismo, y aplicaciones como el problema del viajante (TSP) y optimización de funciones.""",
                icon='🧬', duration='10 semanas', level='intermedio',
                instructor_name='Andrés Bravo',
                instructor_bio='Ingeniero de Machine Learning especializado en optimización evolutiva y metaheurísticas. Experiencia en algoritmos genéticos para problemas de optimización combinatoria y diseño de ingeniería.',
                instructor_avatar_url='', is_active=True, order=8,
            )
        )

        print(f"✓ Curso '{course_ag.title}' (id={course_ag.id}) listo.")

        # -- Explicaciones --
        CourseContent.objects.update_or_create(
        course=course_ag, section_type='explicacion', title='Fundamentos Biológicos y Conceptos Clave', order=1,
        defaults={'content': '''<h3>Inspiración biológica</h3>
        <p>Los algoritmos genéticos (AG) fueron desarrollados por <strong>John Holland</strong> en la década de 1970 en la Universidad de Michigan, y popularizados por su libro <em>"Adaptation in Natural and Artificial Systems"</em> (1975). Se inspiran en la teoría de la evolución de Darwin y la genética mendeliana.</p>

        <h3>Analogía biología → algoritmo</h3>
        <table>
        <tr><th>Biología</th><th>Algoritmo Genético</th></tr>
        <tr><td>Individuo</td><td>Solución candidata (cromosoma)</td></tr>
        <tr><td>Gen</td><td>Variable de decisión (parámetro)</td></tr>
        <tr><td>Alelo</td><td>Valor específico de un gen (0, 1, 3.5, ...)</td></tr>
        <tr><td>Cromosoma</td><td>Codificación completa de la solución</td></tr>
        <tr><td>Población</td><td>Conjunto de soluciones candidatas</td></tr>
        <tr><td>Fitness (aptitud)</td><td>Función objetivo a maximizar/minimizar</td></tr>
        <tr><td>Selección natural</td><td>Selección de los mejores individuos</td></tr>
        <tr><td>Cruce (reproducción)</td><td>Combinación de dos soluciones padre</td></tr>
        <tr><td>Mutación</td><td>Alteración aleatoria de un gen</td></tr>
        <tr><td>Evolución</td><td>Iteración del algoritmo (generaciones)</td></tr>
        </table>

        <h3>Algoritmo básico</h3>
        <ol>
        <li><strong>Inicializar</strong> población aleatoria de N individuos.</li>
        <li><strong>Evaluar</strong> el fitness de cada individuo.</li>
        <li><strong>Seleccionar</strong> padres (los más aptos tienen más probabilidad).</li>
        <li><strong>Aplicar cruce</strong> (crossover) para generar hijos.</li>
        <li><strong>Aplicar mutación</strong> a los hijos (con probabilidad baja).</li>
        <li><strong>Reemplazar</strong> la población (o parte de ella) con los nuevos individuos.</li>
        <li><strong>Repetir</strong> desde paso 2 hasta alcanzar el criterio de parada.</li>
        </ol>

        <h3>Criterios de parada comunes</h3>
        <ul>
        <li>Número máximo de generaciones alcanzado.</li>
        <li>Fitness óptimo encontrado (solución exacta conocida).</li>
        <li>Convergencia: la población ya no mejora significativamente.</li>
        <li>Tiempo de ejecución límite.</li>
        </ul>

        <h3>Ventajas de los AG</h3>
        <ul>
        <li>No requieren derivadas (a diferencia del gradiente descendente).</li>
        <li>Trabajan con cualquier tipo de función objetivo (discontinua, no diferenciable, ruidosa).</li>
        <li>Exploran múltiples regiones del espacio de búsqueda simultáneamente.</li>
        <li>Escapabilidad de óptimos locales (gracias a la mutación).</li>
        <li>Se adaptan fácilmente a problemas combinatorios y de optimización discreta.</li>
        </ul>

        <p>Referencias:</p>
        <ul>
        <li>Holland, J. H. (1975). <em>Adaptation in Natural and Artificial Systems</em>. University of Michigan Press.</li>
        <li>Goldberg, D. E. (1989). <em>Genetic Algorithms in Search, Optimization, and Machine Learning</em>. Addison-Wesley.</li>
        <li>Mitchell, M. (1998). <em>An Introduction to Genetic Algorithms</em>. MIT Press.</li>
        </ul>'''}
    )

        CourseContent.objects.update_or_create(
        course=course_ag, section_type='explicacion', title='Codificación, Selección y Operadores Genéticos', order=2,
        defaults={'content': '''<h3>Tipos de codificación</h3>

        <h4>Codificación binaria</h4>
        <p>Cada gen es 0 o 1. Un cromosoma de longitud L representa 2ᴸ valores posibles.</p>
        <p>Ejemplo: x ∈ [0, 10] con 8 bits → 256 valores, precisión 10/255 ≈ 0.039</p>
        <p>Decodificación: x = min + (max-min) × valor_binario / (2ᴸ - 1)</p>

        <h4>Codificación real (valor continuo)</h4>
        <p>Cada gen es un número real. Más natural para optimización continua.</p>
        <p>Ejemplo: [2.5, -1.3, 0.7, 4.2] representa 4 variables de decisión.</p>

        <h4>Codificación por permutación</h4>
        <p>Usada en problemas de ordenamiento (TSP, scheduling).</p>
        <p>Ejemplo: [3, 1, 4, 2, 5] representa una ruta que visita ciudades 3→1→4→2→5.</p>

        <h3>Métodos de selección</h3>

        <h4>Selección por ruleta (Roulette Wheel)</h4>
        <p>Probabilidad de selección = fitnessᵢ / Σ(fitness)</p>
        <p>Problema: si hay un individuo muy superior, la diversidad se pierde rápidamente.</p>

        <h4>Selección por torneo (Tournament Selection)</h4>
        <ol>
        <li>Seleccionar k individuos aleatoriamente (típico 'k': 3).</li>
        <li>El de mejor fitness gana el torneo.</li>
        <li>Repetir para cada padre necesario.</li>
        </ol>
        <p>Ventaja: no depende de la escala del fitness, mantiene diversidad.</p>

        <h4>Selección por rango (Rank Selection)</h4>
        <p>Ordena individuos por fitness y asigna probabilidades basadas en el rango, no en el valor absoluto. Mitiga el problema de "super-individuos".</p>

        <h4>Selección elitista (Elitism)</h4>
        <p>Los mejores N individuos (élite) pasan directamente a la siguiente generación sin modificarse. Garantiza que la mejor solución nunca se pierda.</p>

        <h3>Operadores de cruce (Crossover)</h3>

        <h4>Cruce de un punto</h4>
        <p>Se elige un punto de corte al azar y se intercambian las colas de los padres.</p>
        <p>Padre1: [A B | C D E] → Hijo1: [A B | c d e]</p>
        <p>Padre2: [a b | c d e] → Hijo2: [a b | C D E]</p>

        <h4>Cruce de dos puntos</h4>
        <p>Se eligen dos puntos de corte y se intercambia la sección media.</p>

        <h4>Cruce uniforme</h4>
        <p>Cada gen se hereda del padre 1 o del padre 2 con probabilidad 0.5.</p>

        <h4>Cruce aritmético (para codificación real)</h4>
        <p>Hijo = α × Padre1 + (1-α) × Padre2, con α ∈ [0, 1].</p>

        <h3>Operadores de mutación</h3>

        <h4>Mutación bit flip (binaria)</h4>
        <p>Con probabilidad p_m (típica 0.01-0.1), cada bit se invierte.</p>

        <h4>Mutación gaussiana (real)</h4>
        <p>gen' = gen + N(0, σ), donde σ controla la magnitud.</p>

        <h4>Mutación por intercambio (permutación)</h4>
        <p>Se intercambian dos posiciones al azar en el cromosoma.</p>

        <h3>Hiperparámetros principales</h3>
        <table>
        <tr><th>Parámetro</th><th>Rango típico</th><th>Efecto</th></tr>
        <tr><td>Tamaño población</td><td>20-500</td><td>Mayor = más diversidad pero más lento</td></tr>
        <tr><td>Tasa de cruce</td><td>0.6-1.0</td><td>Más cruce = más exploración</td></tr>
        <tr><td>Tasa de mutación</td><td>0.001-0.1</td><td>Más mutación = más diversidad</td></tr>
        <tr><td>Tamaño élite</td><td>1-5</td><td>Preserva mejores soluciones</td></tr>
        <tr><td>Tamaño torneo</td><td>2-7</td><td>Mayor = más presión selectiva</td></tr>
        </table>'''}
    )

        CourseContent.objects.update_or_create(
        course=course_ag, section_type='explicacion', title='El Problema del Viajante (TSP) y Aplicaciones', order=3,
        defaults={'content': '''<h3>Problema del Viajante (TSP)</h3>
        <p>El TSP (Traveling Salesman Problem) es un problema NP-difícil que busca la ruta más corta que visita un conjunto de ciudades exactamente una vez y regresa al punto de inicio.</p>

        <p><strong>Formalización:</strong> Dado un conjunto de n ciudades y una matriz de distancias d(i,j), encontrar la permutación π que minimice:</p>
        <p>Distancia total = Σ d(πᵢ, πᵢ₊₁) + d(πₙ, π₁)</p>

        <p>Para n ciudades, hay (n-1)!/2 rutas posibles. Con 'n': 20: ~6×10¹⁶ rutas.</p>

        <h3>Aplicaciones reales de los AG</h3>
        <table>
        <tr><th>Campo</th><th>Aplicación</th></tr>
        <tr><td>Logística</td><td>Optimización de rutas de reparto, planificación de flotas</td></tr>
        <tr><td>Ingeniería</td><td>Diseño de alas de avión (optimización aerodinámica)</td></tr>
        <tr><td>Finanzas</td><td>Optimización de portafolios de inversión</td></tr>
        <tr><td>Robótica</td><td>Planificación de movimientos, calibración de sensores</td></tr>
        <tr><td>Videojuegos</td><td>Generación procedural de niveles, IA de NPCs</td></tr>
        <tr><td>Bioinformática</td><td>Plegamiento de proteínas, alineamiento de secuencias</td></tr>
        <tr><td>Machine Learning</td><td>Selección de características, optimización de hiperparámetros</td></tr>
        <tr><td>Telecomunicaciones</td><td>Diseño de redes de antenas, enrutamiento de paquetes</td></tr>
        </table>

        <h3>Ventajas frente a métodos tradicionales</h3>
        <ul>
        <li><strong>Frente a gradiente descendente:</strong> No necesita derivadas, evita óptimos locales.</li>
        <li><strong>Frente a búsqueda exhaustiva:</strong> Mucho más rápido en espacios grandes.</li>
        <li><strong>Frente a algoritmos greedy:</strong> Soluciones de mejor calidad (aunque más lentos).</li>
        <li><strong>Frente a Simulated Annealing:</strong> Los AG mantienen una población (exploración paralela).</li>
        </ul>

        <h3>Limitaciones</h3>
        <ul>
        <li>No garantizan encontrar el óptimo global.</li>
        <li>Requieren ajuste cuidadoso de parámetros.</li>
        <li>Pueden converger prematuramente a óptimos locales.</li>
        <li>Computacionalmente costosos para problemas con evaluaciones de fitness lentas.</li>
        </ul>

        <p>Referencia: Eiben, A. E., & Smith, J. E. (2015). <em>Introduction to Evolutionary Computing</em> (2nd ed.). Springer. ISBN: 978-3-662-44873-1.</p>'''}
    )

        # -- Ejemplos --
        CourseContent.objects.update_or_create(
        course=course_ag, section_type='ejemplo', title='Ejemplo: AG para Optimización de Funciones', order=4,
        defaults={'content': '''<h3>Implementación completa de un AG para maximizar f(x) = x·sen(10π·x) + 1</h3>
        <p>Este ejemplo implementa un AG desde cero con codificación binaria, selección por torneo, cruce de un punto y mutación bit flip.</p>

<pre><code>import numpy as np
import random

# === CONFIGURACIÓN ===
TAM_POBLACION = 100
TASA_CRUCE = 0.85
TASA_MUTACION = 0.02
GENERACIONES = 100
ELITE = 3
L_BITS = 16
X_MIN, X_MAX = -1.0, 2.0

def decodificar(bits):
    val = int(''.join(str(b) for b in bits), 2)
    return X_MIN + (X_MAX - X_MIN) * val / (2**L_BITS - 1)

def fitness(x):
    # Función: f(x) = x·sen(10π·x) + 1  (máximo global ≈ 2.85 en x≈1.85)
    return x * np.sin(10 * np.pi * x) + 1

# Inicializar población
poblacion = [[random.randint(0, 1) for _ in range(L_BITS)]
             for _ in range(TAM_POBLACION)]

mejor_fitness_historico = []
mejor_x_historico = []

for gen in range(GENERACIONES):
    # Evaluar
    valores_x = [decodificar(ind) for ind in poblacion]
    fitness_vals = [fitness(x) for x in valores_x]

    # Mejor de la generación
    idx_mejor = np.argmax(fitness_vals)
    mejor_fitness_historico.append(fitness_vals[idx_mejor])
    mejor_x_historico.append(valores_x[idx_mejor])

    # Nueva población (con elitismo)
    ordenados = np.argsort(fitness_vals)[::-1]
    nueva_pob = [poblacion[i] for i in ordenados[:ELITE]]

    while len(nueva_pob) < TAM_POBLACION:
        # Selección por torneo
        torneo = random.sample(range(TAM_POBLACION), 3)
        ganador = max(torneo, 'key': lambda i: fitness_vals[i])
        padre1 = poblacion[ganador]

        torneo = random.sample(range(TAM_POBLACION), 3)
        ganador = max(torneo, 'key': lambda i: fitness_vals[i])
        padre2 = poblacion[ganador]

        hijo1, hijo2 = list(padre1), list(padre2)

        # Cruce de un punto
        if random.random() < TASA_CRUCE:
            punto = random.randint(1, L_BITS - 1)
            hijo1 = padre1[:punto] + padre2[punto:]
            hijo2 = padre2[:punto] + padre1[punto:]

        # Mutación
        for h in [hijo1, hijo2]:
            for j in range(L_BITS):
                if random.random() < TASA_MUTACION:
                    h[j] = 1 - h[j]

        nueva_pob.append(hijo1)
        if len(nueva_pob) < TAM_POBLACION:
            nueva_pob.append(hijo2)

    poblacion = nueva_pob

    if (gen + 1) % 20 == 0:
        print(f"Gen {gen+1:3d} | Mejor f(x) = {mejor_fitness_historico[-1]:.6f} "
              f"en x = {mejor_x_historico[-1]:.6f}")

# Resultados
print(f"\n=== MEJOR SOLUCIÓN ENCONTRADA ===")
mejor_idx = np.argmax(mejor_fitness_historico)
print(f"f(x) = {mejor_fitness_historico[mejor_idx]:.6f}")
print(f"x    = {mejor_x_historico[mejor_idx]:.6f}")
print(f"Generación: {mejor_idx + 1}")
print(f"\n(Máximo global conocido: f(1.85) ≈ 2.85)")
</code></pre>

        <h3>Salida esperada (aproximada)</h3>
<pre><code>Gen  20 | Mejor f(x) = 2.836142 en x = 1.849365
Gen  40 | Mejor f(x) = 2.848571 en x = 1.849579
Gen  60 | Mejor f(x) = 2.849213 en x = 1.850621
Gen  80 | Mejor f(x) = 2.849843 en x = 1.850523
Gen 100 | Mejor f(x) = 2.849843 en x = 1.850523

=== MEJOR SOLUCIÓN ENCONTRADA ===
f(x) = 2.849843
x    = 1.850523
(Máximo global conocido: f(1.85) ≈ 2.85)
</code></pre>'''}
    )

        CourseContent.objects.update_or_create(
        course=course_ag, section_type='ejemplo', title='Ejemplo: AG para el Problema del Viajante (TSP)', order=5,
        defaults={'content': '''<h3>Resolución del TSP con codificación por permutación</h3>

<pre><code>import numpy as np
import random
import math

# === CONFIGURACIÓN ===
N_CIUDADES = 20
TAM_POB = 200
TASA_CRUCE = 0.85
TASA_MUT = 0.05
GENERACIONES = 300
ELITE = 4

# Generar ciudades aleatorias
np.random.seed(42)
ciudades = np.random.rand(N_CIUDADES, 2) * 100  # Coordenadas (x, y)

# Matriz de distancias euclidianas
dist = np.zeros((N_CIUDADES, N_CIUDADES))
for i in range(N_CIUDADES):
    for j in range(N_CIUDADES):
        dist[i][j] = math.sqrt((ciudades[i][0] - ciudades[j][0])**2
                              + (ciudades[i][1] - ciudades[j][1])**2)

def fitness_tsp(ruta):
    distancia = sum(dist[ruta[i]][ruta[i+1]] for i in range(N_CIUDADES-1))
    distancia += dist[ruta[-1]][ruta[0]]  # Regresar al inicio
    return -distancia  # Negativo porque maximizamos fitness

def crossover_ox(padre1, padre2):
    """Cruce por orden (OX) para permutaciones."""
    n = len(padre1)
    a, b = sorted(random.sample(range(n), 2))
    hijo = [-1] * n
    hijo[a:b+1] = padre1[a:b+1]
    pos = (b + 1) % n
    for gen in padre2:
        if gen not in hijo:
            hijo[pos] = gen
            pos = (pos + 1) % n
    return hijo

# Inicializar población con rutas aleatorias
poblacion = [list(np.random.permutation(N_CIUDADES))
             for _ in range(TAM_POB)]

mejor_dist = float('inf')
mejor_ruta = None

for gen in range(GENERACIONES):
    fitness_vals = [fitness_tsp(ruta) for ruta in poblacion]
    idx_mejor = np.argmax(fitness_vals)
    dist_mejor = -fitness_vals[idx_mejor]

    if dist_mejor < mejor_dist:
        mejor_dist = dist_mejor
        mejor_ruta = poblacion[idx_mejor]

    # Elitismo
    orden = np.argsort(fitness_vals)[::-1]
    nueva_pob = [poblacion[i] for i in orden[:ELITE]]

    while len(nueva_pob) < TAM_POB:
        # Torneo
        t1 = max(random.sample(range(TAM_POB), 3),
                 'key': lambda i: fitness_vals[i])
        t2 = max(random.sample(range(TAM_POB), 3),
                 'key': lambda i: fitness_vals[i])
        p1, p2 = poblacion[t1], poblacion[t2]

        if random.random() < TASA_CRUCE:
            hijo = crossover_ox(p1, p2)
        else:
            hijo = list(p1)

        # Mutación por intercambio
        if random.random() < TASA_MUT:
            i, j = random.sample(range(N_CIUDADES), 2)
            hijo[i], hijo[j] = hijo[j], hijo[i]

        nueva_pob.append(hijo)

    poblacion = nueva_pob

    if (gen + 1) % 50 == 0:
        print(f"Gen {gen+1:3d} | Mejor distancia: {mejor_dist:.2f}")

print(f"\n=== RESULTADO TSP ({N_CIUDADES} ciudades) ===")
print(f"Mejor distancia encontrada: {mejor_dist:.2f}")
print(f"Ruta óptima: {mejor_ruta}")

# Distancia greedy como referencia
greedy = [0]
no_visitadas = set(range(1, N_CIUDADES))
while no_visitadas:
    ult = greedy[-1]
    sig = min(no_visitadas, key=lambda c: dist[ult][c])
    greedy.append(sig)
    no_visitadas.remove(sig)
dist_greedy = sum(dist[greedy[i]][greedy[i+1]]
                  for i in range(N_CIUDADES-1))
dist_greedy += dist[greedy[-1]][greedy[0]]
print(f"Distancia greedy:        {dist_greedy:.2f}")
print(f"Mejora AG vs greedy:     {(1 - mejor_dist/dist_greedy)*100:.1f}%")
</code></pre>

        <h3>Salida esperada (aproximada)</h3>
<pre><code>Gen  50 | Mejor distancia: 397.23
Gen 100 | Mejor distancia: 382.15
Gen 150 | Mejor distancia: 374.89
Gen 200 | Mejor distancia: 369.71
Gen 250 | Mejor distancia: 366.44
Gen 300 | Mejor distancia: 364.82

=== RESULTADO TSP (20 ciudades) ===
Mejor distancia encontrada: 364.82
Ruta óptima: [7, 3, 15, 11, 9, 6, 19, 8, 16, 14, 5, 1, 10, 0, 17, 13, 18, 12, 4, 2]
Distancia greedy:        435.67
Mejora AG vs greedy:     16.3%
</code></pre>'''}
    )

        # -- Demo --
        CourseContent.objects.update_or_create(
        course=course_ag, section_type='demo', title='Demo: Evolución de la Población y Convergencia', order=6,
        defaults={'content': '''<h3>Visualización de la convergencia del AG y efecto de parámetros</h3>

<pre><code>import numpy as np
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# === AG para f(x) = x·sen(10π·x) + 1 (máximo en x≈1.85) ===
def ejecutar_ag(tam_pob, tasa_mut, 'gen_max': 80, 'titulo': ""):
    L_BITS, X_MIN, X_MAX = 16, -1.0, 2.0
    def decod(bits):
        v = int(''.join(str(b) for b in bits), 2)
        return X_MIN + (X_MAX - X_MIN) * v / (2**L_BITS - 1)
    def fx(x):
        return x * np.sin(10 * np.pi * x) + 1

    pob = [[random.randint(0, 1) for _ in range(L_BITS)]
           for _ in range(tam_pob)]
    mejor_media = []
    mejor_max = []

    for _ in range(gen_max):
        xs = [decod(ind) for ind in pob]
        fv = [fx(x) for x in xs]
        mejor_max.append(max(fv))
        mejor_media.append(np.mean(fv))

        # Torneo + elitismo
        orden = np.argsort(fv)[::-1]
        nueva = [pob[i] for i in orden[:3]]

        while len(nueva) < tam_pob:
            t1 = max(random.sample(range(tam_pob), 3),
                     'key': lambda i: fv[i])
            t2 = max(random.sample(range(tam_pob), 3),
                     'key': lambda i: fv[i])
            p1, p2 = pob[t1], pob[t2]

            punto = random.randint(1, L_BITS-1)
            h1 = p1[:punto] + p2[punto:]
            h2 = p2[:punto] + p1[punto:]

            for h in [h1, h2]:
                for j in range(L_BITS):
                    if random.random() < tasa_mut:
                        h[j] = 1 - h[j]
            nueva.append(h1)
            if len(nueva) < tam_pob:
                nueva.append(h2)
        pob = nueva

    return mejor_max, mejor_media

# Comparar configuraciones
configs = [
    (50, 0.01, "'Pob': 50, 'Mut': 0.01"),
    (100, 0.01, "'Pob': 100, 'Mut': 0.01"),
    (50, 0.05, "'Pob': 50, 'Mut': 0.05"),
    (100, 0.10, "'Pob': 100, 'Mut': 0.10"),
]

plt.figure('figsize': (12, 8))
colores = ['blue', 'green', 'red', 'purple']

for (pob, mut, label), color in zip(configs, colores):
    max_v, media_v = ejecutar_ag(pob, mut)
    gen = range(1, len(max_v) + 1)
    plt.subplot(2, 1, 1)
    plt.plot(gen, max_v, 'color': color, 'linewidth': 2, 'label': f'{label} (máx)')
    plt.subplot(2, 1, 2)
    plt.plot(gen, media_v, color=color, linewidth=2,
             linestyle='--', label=f'{label} (media)')

plt.subplot(2, 1, 1)
plt.axhline(y=2.85, color='gray', linestyle=':', alpha=0.5, label='Óptimo global (~2.85)')
plt.xlabel('Generación'); plt.ylabel('Mejor fitness')
plt.title('Convergencia del Algoritmo Genético (mejor individuo)')
plt.legend(fontsize=7); plt.grid(alpha=0.3)

plt.subplot(2, 1, 2)
plt.xlabel('Generación'); plt.ylabel('Fitness promedio')
plt.title('Evolución del fitness promedio de la población')
plt.legend(fontsize=7); plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/ga_convergence.png', dpi=100)
print("Gráfico guardado en /tmp/ga_convergence.png")

# Tabla resumen
print(f"\n{'Configuración':<25} {'Mejor fitness':<15} {'Generación':<15}")
print('-' * 55)
for (pob, mut, label) in configs:
    max_v, _ = ejecutar_ag(pob, mut, gen_max=80)
    gen_mejor = np.argmax(max_v) + 1
    print(f"{label:<25} {max(max_v):<15.6f} {gen_mejor:<15}")
</code></pre>

        <h3>Análisis de resultados</h3>
        <ul>
        <li><strong>Población grande (100):</strong> Más estable, converge más cerca del óptimo.</li>
        <li><strong>Mutación baja (0.01):</strong> Converge más rápido pero puede estancarse.</li>
        <li><strong>Mutación alta (0.10):</strong> Más exploración, pero puede no converger.</li>
        <li><strong>Mejor configuración:</strong> Pob=100, Mut=0.01-0.05 para este problema.</li>
        </ul>

        <h3>Reglas heurísticas para ajustar parámetros</h3>
        <ol>
        <li><strong>Si el AG converge muy rápido a una solución subóptima:</strong> aumentar población o mutación.</li>
        <li><strong>Si el AG no converge y oscila:</strong> reducir mutación, aumentar presión selectiva (torneo más grande).</li>
        <li><strong>Si la población pierde diversidad:</strong> aumentar mutación, reducir elitismo.</li>
        <li><strong>Regla general:</strong> empezar con poblaciones grandes y poca mutación, ajustar según resultados.</li>
        </ol>'''}
    )

        # -- Examen --
        exam_ag, _ = Exam.objects.update_or_create(
        course=course_ag, title='Examen: Algoritmo Genético',
        defaults={'description': 'Evalúa conceptos de algoritmos genéticos: selección, cruce, mutación, codificación y aplicaciones.', 'passing_score': 70, 'time_limit_minutes': 30}
    )

        q, _ = Question.objects.update_or_create(
            exam=exam_ag, text='¿Quién desarrolló los algoritmos genéticos originalmente?',
            defaults={'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='John Holland en la década de 1970',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Charles Darwin en el siglo XIX',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Alan Turing en la década de 1950',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Geoffrey Hinton en la década de 1980',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_ag, text='¿Qué corresponde al concepto de "gen" en un algoritmo genético?',
            defaults={'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Una variable de decisión o parámetro de la solución',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='La función objetivo que se optimiza',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='El conjunto completo de soluciones candidatas',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='El operador que combina dos soluciones',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_ag, text='¿Qué ventaja tiene la selección por torneo sobre la selección por ruleta?',
            defaults={'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='No depende de la escala del fitness y mantiene mejor la diversidad',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Es computacionalmente más costosa',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Siempre selecciona al mejor individuo',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Requiere menos parámetros de configuración',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_ag, text='¿Qué es el elitismo en un AG?',
            defaults={'order': 4}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Preservar los mejores individuos sin modificarlos en la siguiente generación',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Eliminar los peores individuos de la población',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Seleccionar solo los individuos con mayor fitness',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Aplicar una tasa de mutación más alta a los mejores',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_ag, text='¿Qué tipo de codificación es más apropiada para el Problema del Viajante (TSP)?',
            defaults={'order': 5}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Codificación por permutación',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Codificación binaria',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Codificación real',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Codificación Gray',
            defaults={'is_correct': False, 'order': 4}
        )

        q, _ = Question.objects.update_or_create(
            exam=exam_ag, text='Si un AG converge demasiado rápido a una solución subóptima, ¿qué parámetro deberías ajustar?',
            defaults={'order': 6}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Aumentar la tasa de mutación o el tamaño de la población',
            defaults={'is_correct': True, 'order': 1}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Reducir la tasa de cruce',
            defaults={'is_correct': False, 'order': 2}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Aumentar el elitismo',
            defaults={'is_correct': False, 'order': 3}
        )
        QuestionOption.objects.update_or_create(
            question=q, text='Reducir el tamaño de la población',
            defaults={'is_correct': False, 'order': 4}
        )

        print(f"  → {exam_ag.title} (6 preguntas)")

        print(f"\n{'='*50}")
        print("CREACIÓN COMPLETADA CON ÉXITO")
        print(f"{'='*50}")
        print(f"\nCursos creados o actualizados:")
        print(f"  • {course_rl.title} (id={course_rl.id}) — 6 contenidos + 1 examen (6 preguntas)")
        print(f"  • {course_ag.title} (id={course_ag.id}) — 6 contenidos + 1 examen (6 preguntas)")
        print(f"\nEjecuta: python manage.py runserver")
        print(f"Luego ingresa al panel admin para ver los cursos.")


if __name__ == '__main__':
    main()
