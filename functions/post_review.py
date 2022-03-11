import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    authenticator = IAMAuthenticator("0lDnononoonnonnonononu01Omi")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://8fe0d9d3-9343-4175-8c7f-42e3660391fc-bluemix.cloudantnosqldb.appdomain.cloud")
    # response = service.post_find( db='reviews', selector={'dealership': {'$eq': int(dict["id"])}}, ).get_result()
    # print(response)
    review = {
        "id": dict["review"]["id"],
        "name": dict["review"]["name"],
        "dealership": dict["review"]["dealership"],
        "review": dict["review"]["review"],
        "purchase": dict["review"]["purchase"],
        # "another": dict["review"]["another"],
        "purchase_date": dict["review"]["purchase_date"],
        "car_make": dict["review"]["car_make"],
        "car_model": dict["review"]["car_model"],
        "car_year": dict["review"]["car_year"]
    }
    create_document_response = service.post_document(db="reviews", document=review ).get_result()
    return {
        'headers': {'Content-Type':'application/json'},
        'body': create_document_response
    }
        
        
        
        
