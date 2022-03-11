import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    response = ""
    try:
        if api_key:
            print(api_key)
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    print(response)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    
    response = requests.post(url, params=kwargs,  headers={'Content-Type': 'application/json', 'X-Debug-Mode':'true'}, json=json_payload)
    print(json.dumps(json_payload, indent = 4))
    print(response)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, False)
    if json_result:
        # Get the row list in JSON as dealers
        print(json_result)
        dealers = json_result#["rows"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, False)
    if json_result:
        for doc in json_result:
            senti = analyze_review_sentiments(doc["review"])
            print(senti)
            dealer_obj = DealerReview(dealership=doc["dealership"], name=doc["name"], purchase=doc["purchase"], review=doc["review"], purchase_date=doc["purchase_date"], car_make=doc["car_make"], car_model=doc["car_model"], car_year=doc["car_year"], sentiment=senti, id=doc["id"])
                                   
 
            results.append(dealer_obj)

    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(txt):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/29322f3c-8d3f-4a7c-af59-bcc6416ee201"
    api_key = "noooooooooooooooooooooooooooooooooooooooo"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=txt,
        language= "en",
        features=Features(sentiment=SentimentOptions())
        ).get_result()
    sentiment = response["sentiment"]["document"]["label"]
    # print(sentiment)
    return sentiment
