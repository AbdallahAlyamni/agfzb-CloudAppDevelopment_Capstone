from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core import ApiException
import requests
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import time

def generateDocId():
    id = "00" + str(time.time()).replace(".","")
    return id

def main(dict):

    CLOUDANT_URL=dict["CLOUDANT_URL"]
    CLOUDANT_APIKEY=dict["IAM_API_KEY"]
    review = dict["review"]

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

    review_doc = Document(
        # id= review["id"],
        name=review["name"],
        dealership= review["dealership"],
        review=review["review"],
        purchase= review["purchase"],
        another= review["another"],
        purchase_date= review["purchase_date"],
        car_make= review["car_make"],
        car_model= review["car_model"],
        car_year= review["car_year"]
    )

    response = client.post_document(db='reviews', document=review_doc)
    return response.result


res = main({
    "IAM_API_KEY":"kRx0m1bqr912khhbhyO950sN2ud1tdReqUE9M0WdanXQ",
    "CLOUDANT_URL":"https://d460560b-a2f5-418c-9f2f-c567233b07bb-bluemix.cloudantnosqldb.appdomain.cloud",
    "review": 
    {
        "id": 1114,
        "name": "Upkar Lidder",
        "dealership": 15,
        "review": "Great service!",
        "purchase": False,
        "another": "field",
        "purchase_date": "02/16/2021",
        "car_make": "Audi",
        "car_model": "Car",
        "car_year": 2021
    }
})



print(res.result)
# print(generateDocId())