import googlemaps
import pandas as pd
import requests
from datetime import datetime
import time
import numpy as np

def obtener_resenas_usuarios(api_key, place_id, max_resenas=5):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    parametros = {
        'place_id': place_id,
        'fields': 'reviews',
        'key': api_key
    }

    try:
        # Realiza la solicitud a la API de Places para obtener detalles, incluyendo reseñas de usuarios
        respuesta = requests.get(url, params=parametros)
        datos = respuesta.json()

        # Verifica si la solicitud fue exitosa y si hay reseñas disponibles
        if respuesta.status_code == 200 and 'reviews' in datos['result']:
            reseñas = datos['result']['reviews'][:max_resenas]

            # Obtén información de cada reseña de usuario
            detalles_resenas = []
            for reseña in reseñas:
                # Utiliza el formato 'yyyy-mm-dd' para la fecha
                fecha_reseña = datetime.utcfromtimestamp(reseña['time']).strftime('%Y-%m-%d')
                detalles_resena = {
                    'autor': reseña['author_name'],
                    'rating': reseña['rating'],
                    'texto': reseña['text'],
                    'fecha': fecha_reseña,
                    'place_id': place_id
                }
                detalles_resenas.append(detalles_resena)

            # Crear un DataFrame con la información de reseñas de usuarios
            df_resenas_usuarios = pd.DataFrame(detalles_resenas)
            return df_resenas_usuarios

        else:
            print(f'Error en la obtención de reseñas: {datos.get("status", "No hay reseñas disponibles")}')
            return pd.DataFrame()

    except Exception as e:
        print(f'Error en la obtención de reseñas: {str(e)}')
        return pd.DataFrame()

def obtener_y_guardar_lugares(coordenadas, api_key, radio=100, tipo='restaurant', max_resenas=5):
    gmaps = googlemaps.Client(key=api_key)

    lugares_totales = []
    reseñas_totales = []

    for estado, ciudades in coordenadas.items():
        for ciudad, coord in ciudades.items():
            pag_token = None

            while True:
                try:
                    resultados = gmaps.places_nearby(location=coord, radius=radio, type=tipo, page_token=pag_token)

                    for resultado in resultados['results']:
                        # Verificar la existencia de los campos 'rating' y 'user_ratings_total'
                        rating = resultado.get('rating', None)
                        num_reviews = resultado.get('user_ratings_total', None)
                        precio = resultado.get('price_level')
                        precio = int(precio) if precio is not None else None

                        lugar = {
                            'nombre': resultado['name'],
                            'direccion': resultado.get('vicinity', 'No disponible'),
                            'ciudad': ciudad,
                            'estado': estado,
                            'rating': rating,
                            'categoria': resultado.get('types', 'No disponible'),
                            'place_id': resultado['place_id'],
                            'num_reviews': num_reviews,
                            'precio': precio,
                            'load_timestamp': pd.to_datetime('now')  # Agregar la columna load_timestamp
                        }

                        # Obtener reseñas de usuarios para cada lugar
                        df_resenas_usuarios = obtener_resenas_usuarios(api_key, resultado['place_id'], max_resenas)
                        reseñas_totales.append(df_resenas_usuarios)

                        lugares_totales.append(lugar)

                    pag_token = resultados.get('next_page_token')
                    if not pag_token:
                        break
                    time.sleep(2)
                except Exception as e:
                    print(f"Error al obtener lugares: {e}")
                    break

    # Crear un DataFrame con la información total de lugares
    df_lugares_totales = pd.DataFrame(lugares_totales)

    # Reemplazar valores no finitos en la columna num_reviews con 0
    df_lugares_totales['num_reviews'] = df_lugares_totales['num_reviews'].replace([np.inf, -np.inf, np.nan], 0)

    # Convertir la columna num_reviews a tipo int64
    df_lugares_totales['num_reviews'] = df_lugares_totales['num_reviews'].astype('int64')

    # Crear un DataFrame con la información total de reseñas de usuarios
    df_resenas_totales = pd.concat(reseñas_totales, ignore_index=True)

    return df_resenas_totales




