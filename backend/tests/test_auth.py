from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hash_roundtrip():
    hashed = hash_password("supersecret123")
    assert verify_password("supersecret123", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_roundtrip():
    token = create_access_token("11111111-2222-3333-4444-555555555555")
    assert decode_access_token(token) == "11111111-2222-3333-4444-555555555555"


def test_invalid_token_rejected():
    assert decode_access_token("not-a-token") is None
