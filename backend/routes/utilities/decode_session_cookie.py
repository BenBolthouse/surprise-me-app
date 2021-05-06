from flask import current_app
from flask.sessions import TaggedJSONSerializer
from itsdangerous import URLSafeTimedSerializer
import hashlib


def decode_session_cookie(cookie_str):
    '''
    Decode a session object from an encoded session cookie.
    '''

    # Credit: https://gist.github.com/babldev/502364a3f7c9bafaa6db
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1,
    }
    key = current_app.config.get("SECRET_KEY")
    s = URLSafeTimedSerializer(key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.loads(cookie_str)
