import uuid
import hashlib
import hmac
import base64
from hacaton.settings import SECRET_KEY, ACCESS_TOKEN_LIFETIME
import datetime
import json


def encode_base64(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def decode_base64(data):
    return base64.b64decode(data).decode('utf-8')


def gen_uuid():
    return str(uuid.uuid4())


def gen_fingerprint():
    return encode_base64(gen_uuid())


def gen_sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def gen_hs256(key, data):
    return hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()


def gen_access_token(user_id, fingerprint):
    header = {"alg": "HS256", "typ": "JWT"}
    fingerprint_hash = gen_sha256(data=fingerprint)
    payload = {"user_id": user_id,
               "exp": int((datetime.datetime.now() + ACCESS_TOKEN_LIFETIME).timestamp()),
               "fingerprint": fingerprint_hash}

    base64_header = encode_base64(json.dumps(header))
    base64_payload = encode_base64(json.dumps(payload))

    base64_sign = encode_base64(gen_hs256(SECRET_KEY, base64_header + '.' + base64_payload))
    token = base64_header + '.' + base64_payload + '.' + base64_sign
    return token


def decode_jwt(at):
    base64_parts = at.split('.')
    try:
        decoded_parts = [decode_base64(part) for part in base64_parts]
        json_parts = [json.loads(part) for part in decoded_parts[:2]]
    except:
        return None
    return json_parts[0], json_parts[1], decoded_parts[2]


def gen_refresh_token():
    return encode_base64(gen_uuid())


def check_at_exp(at):
    try:
        _, payload, _ = decode_jwt(at)
    except:
        return False
    return int(datetime.datetime.now().timestamp()) <= payload['exp']


def check_at_sign(at):
    base64_parts = at.split('.')
    if len(base64_parts) != 3:
        return False
    base64_sign_check = encode_base64(gen_hs256(SECRET_KEY, base64_parts[0] + '.' + base64_parts[1]))
    return base64_sign_check == base64_parts[2]


def check_at_fingerprint(at, fingerprint):
    try:
        _, payload, _ = decode_jwt(at)
    except:
        return False
    fingerprint_hash_check = gen_sha256(data=fingerprint)
    return fingerprint_hash_check == payload['fingerprint']


if __name__ == '__main__':
    fp = gen_fingerprint()
    print('FINGERPRINT: ', fp)
    token = gen_access_token(12, fp)
    decoded = decode_jwt(token)
    print('AT', decoded)
    print('RT', gen_refresh_token())
    print('IS LIFE: ', check_at_exp(token))
    print('CHECK SIGN: ', check_at_sign(token))
    print('CHECK FP: ', check_at_fingerprint(token, fp))


