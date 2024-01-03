from yelpapi import YelpAPI
import pandas as pd

def request_reviews_data(api_key):
    states = ['CA', 'FL', 'IL', 'PA', 'NJ', 'IN', 'TN', 'AZ']
    data_reviews_list = []

    with YelpAPI(api_key) as yelp_api:
        for state in states:
            business_response = yelp_api.search_query(term='restaurants', location=state, sort_by='rating', limit=1)
            businesses = business_response.get('businesses', [])
            for business in businesses:
                ide_biz = business.get('id')

                review_response = yelp_api.reviews_query(id=ide_biz)
                reviews = review_response.get('reviews', [])
                for review in reviews:
                    # Extraer campos específicos
                    reviews_data = {
                        'review_id': review.get('id'),
                        'business_id': business.get('id'),
                        'user_id': review.get('user', {}).get('id'),
                        'stars'	: review.get('rating'),
                        'text': review.get('text'),
                        'date': pd.to_datetime(review.get('time_created')),  # Convertir a datetime64
                    }
                    data_reviews_list.append(reviews_data)

    # Crear el DataFrame para los reviews
    df_reviews = pd.DataFrame(data_reviews_list)
    df_reviews['load_timestamp'] = pd.to_datetime('now')  # UTC

    return df_reviews


