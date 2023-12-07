from jwt import encode

def create_token(data: dict):
    # Payload = content to transform into a token.
    token: str = encode(payload=data, key="password secured", algorithm="HS256")
    return token