from google.cloud import bigquery

def load_df_to_bigquery(project_id, dataset_id, table_name,
                        df, schema, partition_field, append=False):
    try:
        # Inicializar el cliente de Big Query
        print('Inicializando cliente de GBQ..')
        client = bigquery.Client(project=project_id)

        print(
            '\nSubiendo tabla {} a Google BigQuery.'.format(table_name)
        )

        # Obtener referencia del conjunto de datos
        dataset_ref = client.dataset(dataset_id)
        table_id = project_id+'.'+dataset_id+'.'+table_name
        try:
            # Verificar si la tabla existe en el conjunto de datos de referencia
            bq_table = client.get_table(table_id)
        except Exception:
            print("La tabla {} no existe. Creándola..".format(table_id))
            # Crear referencia de la tabla
            table_ref = dataset_ref.table(table_name)
            # Establecer el esquema de la tabla
            table = bigquery.Table(table_ref, schema=schema)
            # Crear partición por fecha
            table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field=partition_field,
            )
            # Crear tabla
            created_table = client.create_table(table)
            print(
                "Tabla creada {}, particionada en la columna {}".format(
                    created_table.table_id,
                    created_table.time_partitioning.field
                )
            )
            # Obtener la tabla creada
            bq_table = client.get_table(table_id)

        # Configuración del trabajo de carga
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.PARQUET
        job_config.autodetect = True

        # Anexar o reemplazar datos
        if append is True:
            job_config.write_disposition = bigquery.\
                                           WriteDisposition.\
                                           WRITE_APPEND
        else:
            job_config.write_disposition = bigquery.\
                                           WriteDisposition.\
                                           WRITE_TRUNCATE

        # Cargar DataFrame de Pandas a Bigquery
        job = client.load_table_from_dataframe(
            df,
            bq_table,
            job_config=job_config
        )

        # Esperar a que el trabajo se complete.
        job.result()

        # Mostrar información
        print("¡Exitoso! Se cargaron {} filas en {}:{}.".format(
            job.output_rows,
            dataset_id,
            table_id)
        )
        return 200
    except Exception as e:
        print('[ERROR] {}'.format(e))
        return 400

