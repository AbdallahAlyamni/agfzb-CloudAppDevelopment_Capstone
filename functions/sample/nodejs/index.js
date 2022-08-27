const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.CLOUDANT_URL);

    if (params.hasOwnProperty('state')) {
        return await getDocument(cloudant, params.state);
    }
    return await getDocuments(cloudant);
}

async function getDocuments(cloudant) {
    let docList = [];
    let response;
    try {
        response = await cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true,
        });
        response.result.rows.forEach(element => {
            docList.push(element.doc);
        });
        return { docList };
    } catch (error) {
        console.log(error.code);
        if (error.code == 404) {
            return { error: "404: The database is empty" }
        } else if (error.code == 500) {
            return { error: "500: Something went wrong on the server" }
        }
    }
}

async function getDocument(cloudant, state) {
    let docList = [];
    let response;
    try {
        response = await cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true,
        });
        response.result.rows.forEach(element => {
            if (element.doc.state == state) {
                docList.push(element.doc);
            }
        });
        return { docList };
    } catch (error) {
        console.log(error.code);
        if (error.code == 404) {
            return { error: "404: The database is empty" }
        } else if (error.code == 500) {
            return { error: "500: Something went wrong on the server" }
        }
    }
}

main({
    IAM_API_KEY: "kRx0m1bqr912khhbhyO950sN2ud1tdReqUE9M0WdanXQ",
    CLOUDANT_URL: "https://d460560b-a2f5-418c-9f2f-c567233b07bb-bluemix.cloudantnosqldb.appdomain.cloud",
    state: "Georgia"
}).then((res) => console.log(res));