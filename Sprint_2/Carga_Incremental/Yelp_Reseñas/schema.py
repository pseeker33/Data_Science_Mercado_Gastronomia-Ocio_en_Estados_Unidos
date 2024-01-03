SCHEMA = [
    {
        "name": "review_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "business_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "user_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "stars",
        "type": "INTEGER",
        "mode": "NULLABLE",
    },
    {
        "name": "text",
        "type": "STRING",
        "mode": "NULLABLE",
    },
    {
        "name": "date",
        "type": "TIMESTAMP",
        "mode": "NULLABLE",
        "description": "date on which the review was created"
    },
    {
        "name": "load_timestamp",
        "type": "TIMESTAMP",
        "mode": "NULLABLE",
        "description": "date on which the data was requested"
    },
]
