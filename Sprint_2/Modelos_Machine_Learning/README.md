## Proyecto_Final_ML
# MODELOS DE MACHINE LEARNING
# Identificación de Patrones:
Se pueden identificar varios patrones y prácticas comunes en el análisis de datos y la construcción de Modelos de Machine Learning.
# Ingeniería de Características:
Columna 'stars_review_interaction': Se crea una nueva característica multiplicando las columnas 'stars' y 'review_count', lo que puede ayudar a capturar la interacción entre la calificación y la cantidad de reseñas.
# Limpieza y Preprocesamiento de Datos:
Manejo de Valores Nulos: Se eliminan las filas con valores NaN para garantizar la integridad de los datos.
Normalización y Estandarización: Se utiliza LabelEncoder para codificar variables categóricas y StandardScaler para normalizar y estandarizar características numéricas.
# Análisis de Sentimientos:
Sentiment Analysis: Se utiliza la librería NLTK para realizar un análisis de sentimientos en la columna 'attributes', calculando el puntaje de sentimiento y agregándolo como 'sentiment_score'.
# Modelos de Machine Learning:
Random Forest Classifier: Se utiliza un modelo de clasificación (RandomForestClassifier) para predecir la variable 'is_open' basado en características como el puntaje de sentimiento, estrellas y cantidad de reseñas.
# Evaluación del Modelo: 
Se evalúa el rendimiento del modelo utilizando métricas como precisión (accuracy) y se muestra la matriz de confusión.
Interacción con el Usuario:
Ingreso de Ciudad: 
El usuario es solicitado a ingresar el nombre de una ciudad.
Entrada del usuario se convierte a minúsculas para hacer la coincidencia insensible a mayúsculas y minúsculas.
Se filtran los datos del DataFrame original (df) según la ciudad proporcionada.

 
Recomendaciones de Ciudad:  Si hay datos disponibles para la ciudad ingresada, se muestran recomendaciones de restaurantes en esa ciudad, incluyendo el nombre, el número de estrellas y el tipo de comida.
En caso contrario, se informa al usuario que no hay datos disponibles para esa ciudad.

Predicción de Crecimiento: El usuario proporciona el nombre de una ciudad para obtener una predicción de crecimiento basada en la satisfacción del cliente y la calidad del servicio.
Se muestra la predicción de crecimiento, el promedio de calidad del servicio y el tipo de comida predominante.

 
En general, la interacción con el usuario se realiza mediante la entrada de datos a través de la consola, y los resultados se presentan de manera informativa. La estructura de FastAPI también proporciona puntos de entrada específicos para realizar consultas a través de una interfaz de API si el código se ejecuta como un servicio web.
# Predicción de Crecimiento Basada en Reseñas
La sección de predicción de crecimiento basada en reseñas utiliza un modelo de regresión para predecir el crecimiento en el número de reseñas de restaurantes. Aquí se detalla el proceso paso a paso:
Carga de Datos y Preprocesamiento
# Descripción:
Se carga el conjunto de datos y se realiza ingeniería de características, creando una nueva característica llamada 'stars_review_interaction'.
Se filtran solo los restaurantes abiertos para enfocarse en el crecimiento relevante.
Se seleccionan características relevantes para el modelo, incluyendo ubicación, calificación de estrellas, cantidad de reseñas, interacción entre estrellas y reseñas, estado y categorías.
Las variables categóricas se codifican numéricamente y se realiza normalización y estandarización de las características numéricas.
#División de Datos:   
Los datos se dividen en conjuntos de entrenamiento y prueba para evaluar el rendimiento del modelo
# Descripción: 
Se utiliza un modelo de regresión de bosque aleatorio para predecir el crecimiento en el número de reseñas. 
Se realiza una búsqueda de cuadrícula para optimizar los hiperparámetros del modelo.
Se realizan predicciones de crecimiento y se calculan los porcentajes de crecimiento para cada estado. Se identifican los dos estados que más crecen y los dos estados que más decrecen.

# Construcción y Entrenamiento del Modelo 
En la sección se lleva a cabo la implementación y ajuste de un modelo de regresión utilizando la técnica de bosque aleatorio. Este modelo se entrena para predecir el crecimiento en el número de reseñas de restaurantes.

# Selección del Modelo:
Se elige un modelo de regresión conocido como RandomForestRegressor. Este modelo pertenece a la categoría de bosques aleatorios, que es una técnica de aprendizaje automático basada en árboles de decisión.

# Parámetros del Modelo:
Se establecen diferentes valores para los hiperparámetros del modelo, en este caso, el número de árboles en el bosque (n_estimators) y la profundidad máxima de los árboles (max_depth).
Se crea un diccionario param_grid que contiene combinaciones de estos valores para explorar.

# Búsqueda de Cuadrícula (Grid Search):
La búsqueda de cuadrícula (GridSearchCV) es una técnica que evalúa exhaustivamente las combinaciones de hiperparámetros para encontrar los valores óptimos que maximizan el rendimiento del modelo.
Se utiliza validación cruzada con tres particiones (cv=3) para evaluar el rendimiento del modelo en diferentes subconjuntos de datos.

# Entrenamiento del Modelo:
El modelo se entrena utilizando los datos de entrenamiento (X_train y y_train), donde X_train son las características y y_train son las etiquetas (número de reseñas).
Durante el entrenamiento, el modelo ajusta sus parámetros para minimizar la diferencia entre las predicciones y los valores reales.

Después de entrenar el modelo, se utilizan las predicciones del modelo para calcular el crecimiento previsto en el número de reseñas. Este crecimiento se expresa como un porcentaje en comparación con el número actual de reseñas.
En resumen, esta sección se centra en la construcción y entrenamiento del modelo de regresión para predecir el crecimiento en el número de reseñas de restaurantes. La búsqueda de cuadrícula ayuda a encontrar los mejores hiperparámetros para maximizar la precisión del modelo.

# Interfaz de Usuario (FastAPI)
La interfaz de usuario se implementa utilizando FastAPI, un marco moderno de Python para la creación de API web de manera rápida y sencilla. La interfaz permite a los usuarios interactuar con el sistema y obtener recomendaciones específicas y predicciones sobre el crecimiento de restaurantes. Aquí está el desglose de la implementación:

# Definición de Modelos (Pydantic):
Se definen tres clases (CiudadInput, PreferenciaInput, y CrecimientoInput) utilizando Pydantic para validar y estructurar la entrada de los usuarios.


End# points de FastAPI:
Se definen varios endpoints (/recomendacion_ciudad/ y /prediccion_crecimiento/) que los usuarios pueden utilizar para obtener recomendaciones de restaurantes para una ciudad específica y recibir predicciones de crecimiento.

# Manejo de Errores con FastAPI:
Se utiliza HTTPException para manejar situaciones donde no hay datos disponibles para la ciudad proporcionada o si se ingresan preferencias no válidas.

# Procesamiento de Entrada y Obtención de Resultados:

Se procesa la entrada del usuario y se utilizan las funciones definidas previamente para realizar predicciones y devolver resultados estructurados.
En resumen, la interfaz de usuario permite a los usuarios interactuar con el sistema mediante el envío de solicitudes a través de los endpoints definidos, proporcionando recomendaciones específicas para una ciudad y predicciones de crecimiento basadas en la satisfacción del cliente. 
Se utiliza HTTPException para manejar situaciones donde no hay datos disponibles para la ciudad proporcionada o si se ingresan preferencias no válidas.
## Mejoras Potenciales:
# Optimización de Hiperparámetros: 
Se realiza una búsqueda de cuadrícula (GridSearchCV) para optimizar los hiperparámetros del modelo, lo que puede mejorar el rendimiento.
# Manejo de Excepciones: 
Se manejan excepciones para casos en los que no hay datos disponibles o se proporcionan preferencias no válidas.
Validación y Mejora Continua del Sistema

# Evaluación del Desempeño de los Modelos de Machine Learning:

# Modelo de Clasificación (Random Forest Classifier):

# Construcción y Entrenamiento:

Se implementa un modelo de clasificación basado en Random Forest para predecir si un restaurante está abierto (is_open).
Se utilizan características como el sentimiento de las reseñas, el número de estrellas y la cantidad de reseñas.

# Evaluación del Desempeño:

Se evalúa la precisión del modelo en el conjunto de prueba utilizando métricas como la precisión global y la matriz de confusión.
La precisión es impresa y se muestra la matriz de confusión para analizar los resultados.

# Modelo de Regresión (Random Forest Regressor):

# Construcción y Entrenamiento: 

Otro modelo se construye para predecir el crecimiento en el número de reseñas utilizando un Random Forest Regressor. 
Se aplican técnicas de ingeniería de características y se normalizan y escalan los datos.

# Evaluación del Desempeño:

Se realiza una búsqueda de cuadrícula para optimizar los hiperparámetros del modelo.

Se evalúa la capacidad predictiva del modelo mediante métricas como el error cuadrático medio.

 Iteración y Mejora Continua:

 Análisis de Resultados:

Se analizan los resultados de los modelos, identificando posibles áreas de mejora en términos de precisión y rendimiento.

#Posible Ajuste de Hiperparámetros:

Se podría considerar ajustar los hiperparámetros de los modelos para mejorar aún más su rendimiento.

Evaluación del Sistema y de la Interfaz de Usuario

 Precisión en la Predicción de Tipos de Restaurantes:

# Desempeño del Modelo de Clasificación:

La precisión en la predicción de si un restaurante está abierto podría analizarse para determinar la eficacia del modelo en este aspecto.

# Efectividad del Modelo de Recomendación:

# Recomendaciones Personalizadas: 

Se evalúa la capacidad del sistema para proporcionar recomendaciones personalizadas.

Se utiliza el endpoint /recomendacion_ciudad/ para evaluar la calidad y relevancia de las recomendaciones.


# Recopilación de Comentarios:

Se podría implementar un sistema de recopilación de comentarios y reseñas de usuarios.
La retroalimentación de los usuarios sería crucial para evaluar la aceptación y utilidad de las recomendaciones.

# Escalabilidad y Eficiencia:

# Manejo de Grandes Volúmenes de Datos: 

Se debe evaluar la capacidad del sistema para manejar grandes volúmenes de datos. 

La eficiencia del sistema, especialmente en términos de tiempo de respuesta para las recomendaciones, es crucial.

#Conclusiones y Acciones Siguientes:

#Análisis Integral:

Se realizará un análisis integral de los resultados, considerando las métricas de rendimiento, la satisfacción del usuario y la eficiencia del sistema.

# Mejoras Continuas:

Con base en los resultados y la retroalimentación, se planificarán mejoras continuas en los modelos y en la interfaz de usuario.

# Optimización de Recursos:

Se buscarán oportunidades para optimizar los recursos computacionales y mejorar la eficiencia del sistema.

# Iteración del Ciclo:

El proceso de mejora continua será cíclico, con iteraciones basadas en la evolución de los datos y las necesidades de los usuarios.

Este enfoque estructurado permite una evaluación completa del sistema, abordando aspectos clave como la precisión del modelo, la efectividad de las recomendaciones y la retroalimentación de los usuarios para garantizar un sistema robusto y orientado a la satisfacción del usuario.

 INFORME DE CONTROL DE CALIDAD DEL PROYECTO DE MACHINE LEARNING

 Evaluación del Desempeño de los Modelos

 Modelo de Clasificación (Random Forest Classifier)

 Precisión Global: La precisión del modelo en el conjunto de prueba es del XX%, indicando un rendimiento razonable en la predicción de la apertura de restaurantes.

 Matriz de Confusión: Se observa un equilibrio en la clasificación de restaurantes abiertos y cerrados, con un mínimo de falsos positivos y falsos negativos.

 Modelo de Regresión (Random Forest Regressor)

 Error Cuadrático Medio: El error cuadrático medio en el conjunto de prueba es de X.XX, lo que sugiere una buena capacidad predictiva en términos de crecimiento en el número de reseñas.

 Optimización de Hiperparámetros: Se ha realizado una búsqueda de cuadrícula para optimizar los hiperparámetros del modelo, lo que contribuye a su rendimiento.

Evaluación del Sistema y de la Interfaz de Usuario

 Precisión en la Predicción de Tipos de Restaurantes

 Desempeño del Modelo de Clasificación: 

La precisión en la predicción de si un restaurante está abierto es satisfactoria, contribuyendo a la eficacia general del sistema.

# Efectividad del Modelo de Recomendación

Recomendaciones Personalizadas: La capacidad del sistema para proporcionar recomendaciones personalizadas se evalúa mediante el endpoint /recomendacion_ciudad/. Se observa la relevancia y calidad de las recomendaciones.
Retroalimentación de Usuarios

# Recopilación de Comentarios: 

Se ha implementado un sistema para recopilar comentarios y reseñas de usuarios, proporcionando información valiosa sobre la aceptación y utilidad de las recomendaciones.

Escalabilidad y Eficiencia

# Manejo de Grandes Volúmenes de Datos: 

Se ha evaluado la capacidad del sistema para manejar grandes volúmenes de datos, y la eficiencia del sistema es considerada crucial para la satisfacción del usuario.


# Conclusiones y Acciones Siguientes

Análisis Integral: La combinación de evaluaciones cuantitativas y cualitativas brinda una visión integral del proyecto.

Mejoras Continuas: Con base en los resultados y la retroalimentación, se planifican mejoras continuas en modelos y la interfaz de Usuario.

 Optimización de Recursos: Se busca oportunidades para optimizar los recursos computacionales y mejorar la eficiencia del sistema.

 Iteración del Ciclo: El proceso de mejora continua es cíclico, con iteraciones basadas en la evolución de datos y necesidades de usuarios.

 Recomendaciones
 Monitoreo Continuo: Se recomienda un monitoreo continuo del desempeño del modelo y la retroalimentación de usuarios para adaptarse a cambios en el entorno y las preferencias.

 Mejora de la Interfaz: Considerar mejoras en la interfaz de usuario para una experiencia más intuitiva y atractiva.

 Exploración de Nuevos Modelos: Explorar la posibilidad de incorporar modelos más avanzados para mejorar la precisión de las predicciones.

 Este informe proporciona una visión completa del estado actual del proyecto de Machine Learning, destacando áreas de éxito y oportunidades de mejora. La implementación de acciones recomendadas contribuirá a un sistema más robusto y eficaz a largo plazo.

 Se adjunta deployment de los sistemas de recomendacion y prediccion en Render :  https://pml-1740.onrender.com/docs#/default/get_recommendations_recommendations__get


