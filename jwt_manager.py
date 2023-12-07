from jwt import encode, decode

def create_token(data: dict):
    # Payload = content to transform into a token.
    token: str = encode(payload=data, key="password secured", algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    data: str = decode(token, key="password secured", algorithms=["HS256"])
    return data

