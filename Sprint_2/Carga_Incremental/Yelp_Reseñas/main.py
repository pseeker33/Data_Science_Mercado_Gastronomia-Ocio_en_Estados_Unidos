from bigquery_uploader import load_df_to_bigquery
from reviews import request_reviews_data
from schema import SCHEMA

def main(request):
    try:
        # PROJECT VARIABLES
        BIGQUERY_PROJECT_ID = 'aerial-resolver-237012'
        BIGQUERY_DATASET_ID = 'BQ_Yelp_Maps'
        BIGQUERY_TABLE_NAME = 'Yelp_reviews'
        PARTITION_FIELD = 'load_timestamp'
        APPEND_DATA_ON_BIGQUERY = True

        # Request reviews data
        reviews_data = request_reviews_data(api_key=)

        # Check if the created dataframe is not empty
        if reviews_data is None or len(reviews_data) == 0:
            print('No content, table has 0 rows')
            return ('No content, table has 0 rows', 204)

        # Save on Google Big Query
        print("Saving data into Google BigQuery....")
        http_status = load_df_to_bigquery(
            project_id=BIGQUERY_PROJECT_ID,
            dataset_id=BIGQUERY_DATASET_ID,
            table_name=BIGQUERY_TABLE_NAME,
            df=reviews_data,
            schema=SCHEMA,
            partition_field=PARTITION_FIELD,
            append=APPEND_DATA_ON_BIGQUERY
        )

        if http_status == 200:
            return ('Successful!', http_status)
        else:
            return ("Error. Please check the logging panel", http_status)

    except Exception as e:
        error_message = "Error uploading data: {}".format(e)
        print('[ERROR] ' + error_message)
        return (error_message, '400')

