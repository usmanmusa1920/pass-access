# -*- coding: utf-8 -*-
import json
# from itsdangerous import Serializer #(itsdangerous==2.1.2)
# from itsdangerous.serializer import Serializer #(itsdangerous==2.1.2)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #(itsdangerous==0.24)
from toolkit.base import PasscodeSecurity


with open('config.json') as config_file:
    config = json.load(config_file)


SECRET_KEY = config['SECRET_KEY']


def get_token(expires_sec=1):
    """Get toten function"""

    s = Serializer(SECRET_KEY, expires_sec * 60)
    # s = Serializer(SECRET_KEY) #(itsdangerous==2.1.2)
    mysecret = PasscodeSecurity().passcode_salt
    # return s.dumps([1,2,3,4])
    # return s.dumps('mysecret')
    return s.dumps(mysecret)


def verify_token(token):
    """Verify token function"""
    
    s = Serializer(SECRET_KEY)
    try:
        load_token = s.loads(token)
    except:
        return None
    return load_token

# from itsdangerous import TimestampSigner as ts
# s = ts('secretkey')
# string = s.sign('foo')
# s.unsign(string, max_age=5)
