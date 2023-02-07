import hashlib
import hmac

class SigninHMAC:
    def __init__(self, method, uri, headers, data, query_string=None):
        self.method = method.upper()
        self.uri = uri
        self.header_string = "\n".join(
            [f"{k.lower()}:{v}" for k, v in sorted(headers.items()) if k.lower() in ["authorization", "hyp-date", "hyp-content-length", "hyp-content-type"]]
        )
        self.query_string = query_string if query_string else ""
        self.data = self.byte_to_hex_string(self.hash_content(data))

    def hash_content(self, content):
        plain_content = content
        if not plain_content:
            return None

        input_hash = plain_content.encode()
        sha_256 = hashlib.sha256()
        sha_256.update(input_hash)

        return sha_256.digest()

    def byte_to_hex_string(self, bytes ):

        if not bytes:
            return ""
        return "".join([format(b, "02x") for b in bytes])

    def sign(self, secret) -> object:
        secret_byte = secret.encode()
        canonical = f"{self.method}\n{self.uri}\n{self.query_string}\n{self.header_string}\n{self.data}"
        print("canonical:", canonical)
        canonical_byte = canonical.encode()
        hmac_result = hmac.new(secret_byte, canonical_byte, digestmod=hashlib.sha256).hexdigest()
        return hmac_result
