#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core import ApiException
import requests
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(dict):
    # databaseName = "dealerships"
    CLOUDANT_URL=dict["CLOUDANT_URL"]
    CLOUDANT_APIKEY=dict["IAM_API_KEY"]
    authenticator = IAMAuthenticator(CLOUDANT_APIKEY)

    service = CloudantV1(authenticator=authenticator)

    service.set_service_url(CLOUDANT_URL)


    try:
        client = service
        # print("Databases: {0}".format(client.get_all_dbs()))
    except ApiException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print(err)
        return {"error": err}

    return {"dbs": client.get_all_dbs().result}

res = main({
    "COUCH_USERNAME":"d460560b-a2f5-418c-9f2f-c567233b07bb-bluemix",
    "IAM_API_KEY":"kRx0m1bqr912khhbhyO950sN2ud1tdReqUE9M0WdanXQ",
    "CLOUDANT_URL":"https://d460560b-a2f5-418c-9f2f-c567233b07bb-bluemix.cloudantnosqldb.appdomain.cloud"
})["dbs"]

print((res))
