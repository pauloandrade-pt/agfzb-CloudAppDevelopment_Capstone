import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    authenticator = IAMAuthenticator("0lnononononononononnoOmi")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://8fe0d9d3-9343-4175-8c7f-42e3660391fc-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_find( db='reviews', selector={'dealership': {'$eq': int(dict["id"])}}, ).get_result()
    print(response)
    return {
        'headers': {'Content-Type':'application/json'},
        'body': response["docs"]
        }
