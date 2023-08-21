# -*- coding: utf-8 -*-
import os
import json
# from itsdangerous import Serializer #(itsdangerous==2.1.2)
# from itsdangerous.serializer import Serializer #(itsdangerous==2.1.2)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #(itsdangerous==0.24)


with open('config.json') as config_file:
    config = json.load(config_file)


# SECRET_KEY = config['SECRET_KEY']
SECRET_KEY = os.environ.get('SECRET_KEY')


def get_token(expires_sec=30):
    # default `expires_in` = 3600 (1 hour)
    #                        1800 (30 minutes)
    s = Serializer(SECRET_KEY, expires_sec)
    # s = Serializer(SECRET_KEY) #(itsdangerous==2.1.2)
    return s.dumps('mysecret')
    # return s.dumps([1,2,3,4])


def verify_token(token):
    s = Serializer(SECRET_KEY)
    try:
        load_token = s.loads(token)
    except:
        return None
    return load_token


# st = get_token()
# sv = verify_token(st)
# print('token', st)
# print('verify', sv)

# from itsdangerous import TimestampSigner as ts
# s = ts('secretkey')
# string = s.sign('foo')
# s.unsign(string, max_age=5)
