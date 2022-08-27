from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core import ApiException
import requests
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(dict):

    CLOUDANT_URL=dict["CLOUDANT_URL"]
    CLOUDANT_APIKEY=dict["IAM_API_KEY"]
    dealerId = dict["dealerId"]

    authenticator = IAMAuthenticator(CLOUDANT_APIKEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(CLOUDANT_URL)

    try:
        client = service
    except ApiException as ce:
        print("unable to connect")
        return {"error": "500: Something went wrong on the server"}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print(err)
        return {"error": "500: Something went wrong on the server"}

    response = client.post_all_docs(db='reviews', include_docs=True).get_result()
    reviews = []
    for record in response['rows']:
        doc = record["doc"]
        if(doc["dealership"] == dealerId):
            reviews.append(doc)
        
    if(len(reviews) == 0):
        return {"error":"404: dealerId does not exist"}
    else:
        return {"reviews":reviews}


res = main({
    "IAM_API_KEY":"kRx0m1bqr912khhbhyO950sN2ud1tdReqUE9M0WdanXQ",
    "CLOUDANT_URL":"https://d460560b-a2f5-418c-9f2f-c567233b07bb-bluemix.cloudantnosqldb.appdomain.cloud",
    "dealerId":15
})

print((res))
