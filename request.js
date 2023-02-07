//The Script below must be pasted in the Postman tool in the pre script tab
let crypto =require("crypto-js");
const uri = pm.environment.get("HOST_HMAC") + '/auth/hmac';
const encodedUri = uri;
const key = pm.environment.get("X-API-KEY");
const secret = pm.environment.get("CLIENT_SECRET");
const method = pm.request.method;
let headerString = ''
let headers = {};
headers['authorization'] = `x-api-key ${key}`;
headers['hyp-content-length'] = request.data.length;
pm.environment.set("LENGTH_CONTENT",headers['hyp-content-length']);
headers['hyp-content-type'] = pm.request.getHeaders()['hyp-content-type'];
headers['hyp-date'] = (new Date()).toUTCString();
pm.environment.set("DATE_NOW",headers['hyp-date']);
bodyData = ""
if (pm.request.body.raw != undefined){
    bodyData = pm.request.body.raw
}

console.log("body-: ",bodyData)
const headerKeys = Object.keys(headers);

for (const [index, key] of headerKeys.entries()) {
    let value = headers[key];

    if (typeof value !== 'string') {
        value = `${value}`;
    }

    headerString += `${key}:${value.trim()}`


    if (index !== headerKeys.length - 1) {
        headerString += '\n';
    }
}

const body = crypto.enc.Hex.stringify(crypto.SHA256(bodyData));
let canonicalString = '';
canonicalString = `${method}\n`;
canonicalString += `${encodedUri}\n\n`;
canonicalString += `${headerString}\n`;
if (bodyData !==""){
    console.log("body-data:",bodyData)
    canonicalString += `${body}`;
}

console.log("canonical: ",canonicalString);

const signHmac = CryptoJS.enc.Hex.stringify(
    CryptoJS.HmacSHA256(canonicalString, secret)
);
tests["signHmac: " + signHmac] = 1 === 1;

pm.environment.set("HMAC_SIGNATURE", signHmac);