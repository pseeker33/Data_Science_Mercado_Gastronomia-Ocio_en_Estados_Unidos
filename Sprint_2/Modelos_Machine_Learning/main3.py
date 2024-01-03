import pandas as pd
from pandas import json_normalize
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer
from textblob import TextBlob
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from sklearn.preprocessing import MinMaxScaler


# Especifica la ruta del archivo Parquet
ruta_parquet = "restaurants_limpio.parquet"

# Lee el archivo Parquet en un DataFrame
df = pd.read_parquet(ruta_parquet)

# Define una función para manejar casos nulos y convertir atributos numéricos
def safe_eval(attr):
    try:
        if pd.notna(attr) and isinstance(attr, str):
            return eval(attr)
        else:
            return {}
    except:
        return {}

# Normaliza 'attributes' usando la función safe_eval
df_attributes = pd.json_normalize(df['attributes'].apply(safe_eval))

# Configura pandas para mostrar todas las columnas
pd.set_option('display.max_columns', None)
# Convierte columnas numéricas a tipo numérico
numeric_columns = ['stars', 'review_count', 'is_open']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Elimina columnas específicas y filas con valores NaN
df.drop(['address', 'postal_code'], axis=1, inplace=True)
df.dropna(inplace=True)

df.drop(['business_id', 'latitude', 'longitude', 'hours'], axis=1, inplace=True)

# Restaura la configuración original de pandas después de imprimir
pd.reset_option('display.max_columns')

# Muestra las primeras filas del DataFrame después de las correcciones
print(df)
print(df.columns)

################################################################

# Se utiliza LabelEncoder para convertir las etiquetas de la columna 'stars_review_interaction' en números enteros. +
# Esto es comúnmente necesario para que los algoritmos de aprendizaje automático trabajen con variables categóricas.

#Se eliminan las filas que contienen al menos un valor nulo en cualquier columna. }
# Esto se hace para asegurarse de que el conjunto de datos no contenga valores faltantes antes de entrenar el modelo.

#Se divide el conjunto de datos en características (X) y etiquetas (y).
#Luego, se divide el conjunto de datos en conjuntos de entrenamiento (X_train, y_train) y prueba (X_test, y_test). 
# El 80% se usa para entrenar el modelo y el 20% para evaluar su rendimiento.

#Se utiliza un modelo de tubería (make_pipeline) que incluye un preprocesamiento específico para ciertas columnas utilizando SimpleImputer para manejar los valores faltantes ('mean' indica que se rellenarán con la media) y un clasificador RandomForest.
#El modelo se entrena con los datos de entrenamiento (X_train, y_train).}
# Preprocesamiento: Codificar variables categóricas y manejar valores nulos
le = LabelEncoder()
df['stars_review_interaction'] = le.fit_transform(df['stars_review_interaction'])

# Filtrar solo las instancias de la clase '1'
df_model = df[df['is_open'] == 1]

X = df_model.drop('is_open', axis=1)
y = df_model['is_open']

# Dividir datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo
model = make_pipeline(
    make_column_transformer(
        (SimpleImputer(strategy='mean'), ['stars', 'review_count', 'stars_review_interaction'])
    ),
    RandomForestClassifier(random_state=42)
)
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print(classification_report(y_test, y_pred))
print(df_model)
print(df_model.columns)

#############################################################
#Accuracy (Precisión): Es la proporción de instancias correctamente clasificadas entre el total de instancias. 
# En tu caso, un valor de 1.0 significa que todas las instancias se clasificaron correctamente.

#Precision (Precisión): Representa la proporción de instancias positivas correctamente clasificadas 
# entre todas las instancias que se predijeron como positivas. Un valor de 1.0 significa que no hay falsos positivos; 
# todas las predicciones positivas son correctas.

#Recall (Exhaustividad): Representa la proporción de instancias positivas correctamente clasificadas entre todas las 
# instancias que son realmente positivas. Un valor de 1.0 significa que no hay falsos negativos; todas las instancias positivas 
# se identificaron correctamente.

#F1-Score: Es la media armónica de la precisión y la exhaustividad. Es útil cuando hay un desequilibrio entre las clases. 
# Un valor de 1.0 significa un equilibrio perfecto entre precisión y exhaustividad.

#Macro avg (Promedio Macro): Calcula las métricas promedio por clase y luego toma la media de esas métricas. 
# En tu caso, dado que solo hay una clase ('1'), este valor es igual a las métricas de la clase '1'.

#Weighted avg (Promedio Ponderado): Calcula las métricas promedio por clase, pero pondera esas métricas por el número 
# de instancias en cada clase. En este caso, dado que solo hay una clase ('1'), este valor es igual a las métricas de la clase '1'.

# Especifica la ruta del archivo Parquet
ruta_parquet = "restaurants_limpio.parquet"

# Lee el archivo Parquet en un DataFrame
df = pd.read_parquet(ruta_parquet)

# Define una función para manejar casos nulos y convertir atributos numéricos
def safe_eval(attr):
    try:
        if pd.notna(attr) and isinstance(attr, str):
            return eval(attr)
        else:
            return {}
    except:
        return {}

# Normaliza 'attributes' usando la función safe_eval y convierte el diccionario a cadena
df['reviews'] = df['attributes'].apply(lambda x: str(safe_eval(x)))

# Crea una función para analizar el sentimiento de una reseña
def analyze_sentiment(review):
    analysis = TextBlob(str(review))
    return analysis.sentiment.polarity

# Aplica el análisis de sentimiento a todas las reseñas y crea una nueva columna 'sentiment'
df['sentiment'] = df['reviews'].apply(analyze_sentiment)

# Preprocesamiento: Codificar variables categóricas y manejar valores nulos
le = LabelEncoder()
df['stars_review_interaction'] = le.fit_transform(df['stars_review_interaction'])
# Filtrar solo las instancias de la clase '1'
df_model = df[df['is_open'] == 1]

# Dividir datos en conjunto de entrenamiento y prueba
X = df_model.drop(['is_open', 'reviews'], axis=1)
X['sentiment'] = df_model['sentiment']
y = df_model['is_open']

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo
model = make_pipeline(
    make_column_transformer(
        (SimpleImputer(strategy='mean'), ['stars', 'review_count', 'stars_review_interaction', 'sentiment'])
    ),
    RandomForestClassifier(random_state=42)
)
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print(classification_report(y_test, y_pred))


########################################################
# Especifica la ruta del archivo Parquet
ruta_parquet = "restaurants_limpio.parquet"

# Lee el archivo Parquet en un DataFrame
df = pd.read_parquet(ruta_parquet)

# Define una función para manejar casos nulos y convertir atributos numéricos
def safe_eval(attr):
    try:
        if pd.notna(attr) and isinstance(attr, str):
            return eval(attr)
        else:
            return {}
    except:
        return {}

# Normaliza 'attributes' usando la función safe_eval y convierte el diccionario a cadena
df['reviews'] = df['attributes'].apply(lambda x: str(safe_eval(x)))

# Preprocesamiento: Codificar variables categóricas y manejar valores nulos
le = LabelEncoder()
df['stars_review_interaction'] = le.fit_transform(df['stars_review_interaction'])

# Filtrar solo las instancias de la clase '1'
df_model = df[df['is_open'] == 1]

# Dividir datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    df_model[['stars', 'review_count', 'stars_review_interaction']],
    df_model['is_open'],
    test_size=0.2,
    random_state=42)

# Crear y entrenar el modelo
model = make_pipeline(
    make_column_transformer(
        (SimpleImputer(strategy='mean'), ['stars', 'review_count', 'stars_review_interaction'])
    ),
    RandomForestClassifier(random_state=42)
)
model.fit(X_train, y_train)

#########################################################

app = FastAPI()

# Endpoint para obtener recomendaciones de restaurantes por ciudad
@app.get("/recommendations/")
async def get_recommendations(city: str = Query(..., title="City Name", description="Enter the city name to get restaurant recommendations")):
    # Filtra el DataFrame por la ciudad dada
    city_data = df[df['city'].str.lower() == city.lower()]

    if city_data.empty:
        raise HTTPException(status_code=404, detail=f"No restaurants found in {city}")

    # Selecciona las columnas deseadas y convierte el DataFrame a una lista de diccionarios
    results = city_data[['name', 'stars', 'categories']].to_dict(orient='records')

    # Devuelve la información deseada en formato de lista de diccionarios
    return results


from fastapi import Query

@app.get("/growth-decline/")
async def get_growth_decline(
    analysis_type: str = Query(..., title="Analysis Type", description="Enter 'growth' or 'decline'"),
    states: list = Query(..., title="States", description="Enter the names of States (comma-separated)")
):
    # Filtra el DataFrame por los estados dados
    state_data = [df[df['state'].str.lower() == state.lower()] for state in states]

    if any(data.empty for data in state_data):
        raise HTTPException(status_code=404, detail="One or more states not found in the dataset")

    # Calcula el crecimiento o decrecimiento en porcentaje para cada estado
    def calculate_percentage_change(data):
        initial_stars, initial_review_count = data[['stars', 'review_count']].iloc[0]
        latest_stars, latest_review_count = data[['stars', 'review_count']].iloc[-1]

        if analysis_type == 'growth':
            percentage_change = abs(((latest_stars - initial_stars) / initial_stars) * 100)
        elif analysis_type == 'decline':
            percentage_change = -abs(((latest_review_count - initial_review_count) / initial_review_count) * 100)
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type. Use 'growth' or 'decline'.")

        return percentage_change

    # Devuelve la información de crecimiento o decrecimiento
    result_data = [
        {
            'state': state,
            'percentage_change': calculate_percentage_change(data),
            'restaurants': data[['name', 'categories']].to_dict(orient='records')
        }
        for state, data in zip(states, state_data)
    ]

    # Devuelve la información de crecimiento o decrecimiento
    return result_data




