# -*- coding: utf-8 -*-
import hashlib
import base64

try:
  from . contrib import PasscodeSecurity, BcipherTXT
except:
  pass

try:
  from contrib import PasscodeSecurity, BcipherTXT
except:
  pass

class InformationHash(PasscodeSecurity):
    """
    Information hash class for hashing user public and private key,
    also for generating iteratiion number and the salting, along side with second hash
    """
    
    def get_hash(self, salt, itter, passwd):
        """
        generating our key using this class method, and also
        the return type of the key is bytes
        """
        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            passwd, # Our password (public key) is already in bytes type
            salt.encode('utf-8'), # Convert the salt to bytes
            itter, # iteration type is integer
            dklen=128 # Get a 128 byte key
        )

        """
        Base64 encoding convert the binary data (sequence of byte) into text format,
        to avoid data corruption when transfer via only text channel.
        It is Privacy enhanced Electronic Mail (PEM).

        We use ascii to encode the (key)
        """
        # encodeing the key, type is string
        b64_encode = base64.b64encode(key).decode("ascii").strip()
        # hashing our b64_encode (the second hash), type is string
        hash_result = hashlib.sha256(str.encode(str(b64_encode))).hexdigest()
        # salt + iteration + hash_result, type is string
        secure_ingredient = '%s%d%s' % (salt, itter, hash_result)
        
        print("\nThe salt is:  ", salt, sep='')
        print("The itteration is:  ", itter, sep='')
        print("This is the hashlib:  ", hash_result, sep='')
        print("\nThis is the key:\n", key, "\n", sep='')
        
        return [hash_result, secure_ingredient] # return types of the list is string all
    
    def __str__(self):
        return f"Information hash class"
    

class Dcrypt(BcipherTXT):
    pass


# a = InformationHash()
# sl = a.passcode_salt
# it = a.passcode_iteration
# print(a.get_hash(sl, it, b'my secure password'))
