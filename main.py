from Hmac import SigninHMAC
from flask import Flask, request
app = Flask(__name__)


@app.route("/")
def main():
    return "Bem-vindo à página principal!"


@app.route("/auth/hmac", methods=["GET", "POST"])
def hmac():
    date_headers = request.headers
    method = request.method
    uri = f"{request.scheme}://{request.host}/auth/hmac"
    signature_header = date_headers.get("hyp-signature")
    headers = {
        "Authorization": date_headers.get("authorization"),
        "Hyp-Date": date_headers.get("hyp-date"),
        "Hyp-Content-Length": date_headers.get("hyp-content-length"),
        "Hyp-Content-Type": date_headers.get("hyp-content-type")
    }
    data = request.get_data().decode()
    signing_mac = SigninHMAC(method, uri, headers, data, query_string=None)
    secret = "eu8smp&!py1u4-9p77d9s6mra498&y2l292tpn0u96gi-mxa8"
    signature_hmac = signing_mac.sign(secret)

    if signature_hmac == signature_header:
        return {"status": "sucesso"}
    else:
        return {"message": "Unauthorized Access"}


if __name__ == "__main__":
    app.run(debug=True)


