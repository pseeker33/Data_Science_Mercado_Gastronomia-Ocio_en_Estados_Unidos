from yelpapi import YelpAPI
import pandas as pd

def request_business_data(api_key):
    states = ['CA', 'FL', 'IL', 'PA', 'NJ', 'IN', 'TN', 'AZ']
    data_businesses_list = []

    with YelpAPI(api_key) as yelp_api:
        for state in states:
            business_response = yelp_api.search_query(term='restaurants', location=state, sort_by='rating', limit=50)
            businesses = business_response.get('businesses', [])
            for business in businesses:
                business_data = {
                    'business_id': business.get('id'),
                    'name': business.get('name'),
                    'address': business.get('location', {}).get('address1'),
                    'city': business.get('location', {}).get('city'),
                    'state': business.get('location', {}).get('state'),
                    'latitude': business.get('coordinates', {}).get('latitude'),
                    'longitude': business.get('coordinates', {}).get('longitude'),
                    'stars': business.get('rating'),
                    'review_count': business.get('review_count'),
                    'categories': ', '.join([category.get('title') for category in business.get('categories', [])]),
                }
                data_businesses_list.append(business_data)

    # Create a DataFrame from the results
    df_businesses = pd.DataFrame(data_businesses_list)
    df_businesses['load_timestamp'] = pd.to_datetime('now')  # UTC

    return df_businesses
