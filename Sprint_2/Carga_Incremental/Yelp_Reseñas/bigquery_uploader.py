from google.cloud import bigquery

def load_df_to_bigquery(project_id, dataset_id, table_name,
                        df, schema, partition_field, append=True):
    try:
        # Init Big Query Client
        print('Initializing GBQ Client..')
        client = bigquery.Client(project=project_id)

        print(
            '\nUploading table {} to Google BigQuery.'.format(table_name)
        )

        # Get reference dataset
        dataset_ref = client.dataset(dataset_id)
        table_id = project_id + '.' + dataset_id + '.' + table_name
        try:
            # Check if table exists in reference dataset
            bq_table = client.get_table(table_id)
        except Exception:
            print("Table {} doesn't exist. Creating it..".format(table_id))
            # Create table reference
            table_ref = dataset_ref.table(table_name)
            # Set table schema
            table = bigquery.Table(table_ref, schema=schema)
            # Create partition by date
            table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field=partition_field,
            )
            # Create table
            created_table = client.create_table(table)
            print(
                "Created table {}, partitioned on column {}".format(
                    created_table.table_id,
                    created_table.time_partitioning.field
                )
            )
            # Get created table
            bq_table = client.get_table(table_id)

        # Load Job Config
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.PARQUET
        job_config.autodetect = True

        # Append or replace data
        if append is True:
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        else:
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

        # Load Pandas Dataframe to Bigquery
        job = client.load_table_from_dataframe(
            df,
            bq_table,
            job_config=job_config
        )

        # Waits for the job to complete.
        job.result()

        # show info
        print("Successful! Loaded {} rows into {}:{}.".format(
            job.output_rows,
            dataset_id,
            table_id)
        )
        return 200
    except Exception as e:
        print('[ERROR] {}'.format(e))
        return 400

