# -*- coding: utf-8 -*-
import random

try:
  from . crypt_hash import InformationHash, Dcrypt
except:
  pass

try:
  from crypt_hash import InformationHash, Dcrypt
except:
  pass


class InformationSecurity(InformationHash):
    """Information security class"""

    # put this some where safe! (the key),type is <class 'bytes'>
    crypt_key_32 = Dcrypt.generate_key()

    # this need complex implementation
    # crypt_key_64 = base64.urlsafe_b64encode(os.urandom(64))

    # calling Dcrypt class
    f_cls = Dcrypt(crypt_key_32)
    
    def __init__(self, crypt_key_32: bytes = crypt_key_32, f_cls = f_cls):
        self.crypt_key_32 = crypt_key_32
        self.f_cls = f_cls
        
    def encrypt_info(self, info_tion, info_f_cls):
        """encrypting information"""

        """encoding data from text to byte"""
        data_byte = info_tion.encode('utf-8')
        token_public = info_f_cls.encrypt(data_byte)
        return token_public # return type is <class 'bytes'>
    
    def decrypt_info(self, info_data, key):
        """for decryption"""
        t_base_ = Dcrypt(key)

        token_public = t_base_.decrypt(info_data)
        """decoding the token_publick from byte to text"""
        data_text = token_public.decode()
        return data_text # return type is <class 'str'>
    
    def the_key(self):
        """
        the (self.token_generate) is times by 3, (total length is 372),
        so that we will randomly select from it without any restriction,
        since we make the minimum length of the key to be 205 and the maximum to be 357,
        and also it will randomly select from that range of (205 - 357),
        with a stepping of (7)
        """
        the_pass = self.token_generate * 3
        the_list = list(the_pass)
        random.shuffle(the_list) # shuffling the list

        """
        salting our passcode with this class method

        By using the random sample method, where we make:
            population = the_list
            k = random.randrange(205, 357, 7)
        """
        rand_key = "".join(random.sample(the_list, random.randrange(205, 357, 7)))

        return rand_key # return type is str
    
    @property
    def fast_iteration(self):
        """

            *** WE WILL USE THREADING AND MULTIPROCESSING, IN ADVANCE ***

        Generating a random iteration. The iterations is not static,
        it is dynamic (every item's iteration is randomly choosen),
        by using the random method of randrange with:
            min of 111,
            max of 360, and 
            stepping of 7
        """
        itter = random.randrange(111, 360, 7)
        return itter # return type is integer
    
    def __str__(self):
        return f"Information encrypt and decrypt"
