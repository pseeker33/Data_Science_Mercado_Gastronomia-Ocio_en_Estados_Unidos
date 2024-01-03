from bigquery_uploader import load_df_to_bigquery
from restaurantes import obtener_y_guardar_lugares
from schema import SCHEMA

def main(request):
    try:
        # PROJECT VARIABLES
        BIGQUERY_PROJECT_ID = 'tu-proyecto-id'
        BIGQUERY_DATASET_ID = 'tu-dataset-id'
        BIGQUERY_TABLE_NAME = 'restaurantes_data'
        PARTITION_FIELD = 'load_timestamp'
        APPEND_DATA_ON_BIGQUERY = True

        # Coordenadas y API Key
        coordenadas = {
    'California': {
        'Los Angeles': '34.0522,-118.2437',
        'San Francisco': '37.7749,-122.4194',
        'San Diego': '32.7157,-117.1611',
        'San Jose': '37.3382,-121.8863',
        'Fresno': '36.7373,-119.7871'
    },
    'Florida': {
        'Miami': '25.7617,-80.1918',
        'Orlando': '28.5383,-81.3792',
        'Tampa': '27.9506,-82.4572',
        'Jacksonville': '30.3322,-81.6557',
        'St. Petersburg': '27.7676,-82.6403'
    },
    'Tennessee':{
        'Nashville': '36.1627,-86.7816',
        'Memphis': '35.1495,-90.0490',
        'Knoxville': '35.9606,-83.9207',
        'Chattanooga': '35.0456,-85.3097',
        'Clarksville': '36.5298,-87.3595'
    },
    'Illinois':{
        'Chicago': '41.8781,-87.6298',
        'Aurora': '41.7606,-88.3201',
        'Joliet': '41.5250,-88.0817',
        'Rockford': '42.2711,-89.0937',
        'Naperville': '41.7508,-88.1535'
    },
    'Pennsylvania':{
        'Philadelphia': '39.9526,-75.1652',
        'Pittsburgh': '40.4406,-79.9959',
        'Reading': '40.3356,-75.9272',
        'Allentown': '40.6084,-75.4902',
        'Erie': '42.1292,-80.0851'
    },
    'New Jersey':{
        'Newark': '40.7357,-74.1724',
        'Jersey City': '40.7282,-74.0776',
        'Trenton': '40.2206,-74.7597',
        'Elizabeth': '40.6639,-74.2107',
        'Paterson': '40.9168,-74.1718'
    },
    'Indiana':{
        'Indianapolis': '39.7684,-86.1581',
        'Fort Wayne': '41.0793,-85.1394',
        'Evansville': '37.9716,-87.5711',
        'South Bend': '41.6764,-86.2520',
        'Carmel': '39.9784,-86.1180'
    },
    'Arizona':{
        'Phoenix': '33.4484,-112.0740',
        'Tucson': '32.2226,-110.9747',
        'Mesa': '33.4152,-111.8315',
        'Chandler': '33.3062,-111.8413',
        'Scottsdale': '33.4942,-111.9261'
    }
}
        api_key = 'tu-api-key'

        # Obtener datos de lugares y reseñas
        df_lugares, df_resenas_usuarios = obtener_y_guardar_lugares(coordenadas, api_key)

        # Verificar si el DataFrame de lugares no está vacío
        if df_lugares is None or len(df_lugares) == 0:
            print('No hay contenido, el DataFrame de lugares está vacío')
            return ('No hay contenido, el DataFrame de lugares está vacío', 204)

        # Guardar en Google Big Query
        print("Guardando datos en Google Big Query....")
        http_status = load_df_to_bigquery(
            project_id=BIGQUERY_PROJECT_ID,
            dataset_id=BIGQUERY_DATASET_ID,
            table_name=BIGQUERY_TABLE_NAME,
            df=df_lugares,
            schema=SCHEMA,
            partition_field=PARTITION_FIELD,
            append=APPEND_DATA_ON_BIGQUERY
        )

        # Verificar el estado HTTP de la operación
        if http_status == 200:
            return ('¡Éxito!', http_status)
        else:
            return ("Error. Por favor, revisa el panel de registro", http_status)

    except Exception as e:
        error_message = "Error al cargar datos: {}".format(e)
        print('[ERROR] ' + error_message)
        return (error_message, '400')


