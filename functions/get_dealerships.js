const Cloudant = require('@cloudant/cloudant');


async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL || "https://8fe0d9d3-9343-4175-8c7f-42e3660391fc-bluemix.cloudantnosqldb.appdomain.cloud",
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY || '0nononoonononononnonomi' } }
    });


    try {
        let state = params.state
        const headers = {'Content-Type':'application/json'};
        let dealerships = await cloudant.db.use("dealerships").list({ include_docs: true })
        if (state) {
            let onState = dealerships.rows
                    .map(el => el.doc)
                    .filter(dealer => dealer.st == state.toUpperCase())
            if (onState[0]) {
                return {
                    headers,
                    body: onState
                };
            } else {
        return {
            headers,
            error: "The requested resource could not be found.",
            code: 404,
            body: {} 
        }
            }
            return {
                headers,
                body: dealerships.rows
                    .map(el => el.doc)
                    .filter(dealer => dealer.st == state.toUpperCase())
            };
        } else {
            return {
                headers,
                body: dealerships.rows
                    .map(el => el.doc)
            };
        }
    } catch (error) {
        return { error: error.description };
    }
}
