# -*- coding: utf-8 -*-
import base64
import random
import hashlib
from cryptography.fernet import Fernet


class PasscodeSecurity:
    """
    Passcode class for generating iteration number, salting, and creating secure passcode for every user along side with second hash.
    
    A reqular expression that matches any character that
    should never appear in base 64 encodings would be:
    [^A-Za-z0-9+/=]

    we follow the base64 pattern of [^A-Za-z0-9+/=] that should never appear in base64, (in regex)

    NOTE: usage:
        >>> pass_cls = PasscodeSecurity()
        >>> pass_salt = pass_cls.passcode_salt
        >>> pass_itter = pass_cls.passcode_iteration
        >>> print(pass_salt)
        >>> print(pass_cls.get_hash(pass_salt, pass_itter, 'my secure password'))
    """

    token_sm_alpha = 'abcdefghijklmnopqrstuvwxyz'
    token_cap_alpha = token_sm_alpha.upper()
    token_num = '0123456789'
    token_char = '/+='
    token_sum = token_sm_alpha + token_cap_alpha + token_num

    # We times the above variable (token_sum) by 2 (total length is 124),
    # so that we will randomly select from it without any restriction,
    # since we make the minimum length of the salt to be 32 and the maximum to be 64,
    # and also it will randomly select from that range of (32 - 64)

    token_times = token_sum * 2
    token_list = list(token_times)
    random.shuffle(token_list) # shuffling the above list
    token_generate = ''.join(token_list)
    
    def __init__(self, token_generate = token_generate):
        self.token_generate = ''.join(token_generate)
        
    @property
    def passcode_salt(self):
        """
        Salting our passcode with this class method

        By using the random sample method, where we make:
            population = self.token_generate
            k = random.randint(32, 64)
        """

        salt = ''.join(random.sample(self.token_generate, random.randint(32, 64)))
        return salt # return type is string
    
    @property
    def passcode_iteration(self):
        """
        Generating a random iteration. The iterations is not static,
        it is dynamic (every user's iteration is randomly choosen),
        by using the random method of randrange with:
            min of 260000,
            max of 400000, and 
            stepping of 20
        """
        
        # itter = random.randrange(2048, 4048, 20)
        itter = random.randrange(260000, 400000, 20)
        return itter # return type is integer
    
    def get_hash(self, salt: str, itter: int, passwd: str) -> str:
        """
        Generating our key using this class method, and also the return type of the key is bytes
        """

        if type(passwd) == str:
            # for hashing user passcode
            key = hashlib.pbkdf2_hmac(
                'sha256', # The hash digest algorithm for HMAC
                passwd.encode('utf-8'), # Convert the password to bytes
                salt.encode('utf-8'), # Convert the salt to bytes
                itter, # iteration type is integer
                dklen=128 # Get a 128 byte key
            )
        elif type(passwd) == bytes:
            # for hashing user public and private key
            key = hashlib.pbkdf2_hmac(
                'sha256', # The hash digest algorithm for HMAC
                passwd, # Our password (public key) is already in bytes type
                salt.encode('utf-8'), # Convert the salt to bytes
                itter, # iteration type is integer
                dklen=128 # Get a 128 byte key
            )
        else:
            raise TypeError
        
        # Base64 encoding convert the binary data (sequence of byte) into text format,
        # to avoid data corruption when transfer via only text channel.
        # It is Privacy enhanced Electronic Mail (PEM).
        
        # We use ascii to encode the (key)
        
        # encodeing the key, type is string
        b64_encode = base64.b64encode(key).decode('ascii').strip()
        # hashing our b64_encode (the second hash), type is string
        hash_result = hashlib.sha256(str.encode(str(b64_encode))).hexdigest()
        # salt + iteration + hash_result, type is string
        secure_ingredient = '%s%d%s' % (salt, itter, hash_result)
        
        # return types of the list is string all, access it by print(self.get_hash.__annotations__)
        return [hash_result, secure_ingredient]
    
    def __str__(self):
        return f'Passcode security class'
    

class InformationSecurity(PasscodeSecurity):
    """
    Information security class

    NOTE: fernet usage:
        >>> # put this some where safe!
        >>> key = Fernet.generate_key()
        >>> f = Fernet(key)

        >>> token_public = f.encrypt(b'My secret message here!')
        >>> token_private = f.decrypt(token_public)

        >>> print(key)
        >>> print(token_public)
        >>> print(token_private.decode())
    """

    # put this some where safe! (the key),type is <class 'bytes'>
    crypt_key_32 = Fernet.generate_key()

    # this need complex implementation
    # crypt_key_64 = base64.urlsafe_b64encode(os.urandom(64))

    # calling Fernet class
    f_cls = Fernet(crypt_key_32)
    
    def __init__(self, crypt_key_32: bytes = crypt_key_32, f_cls = f_cls):
        self.crypt_key_32 = crypt_key_32
        self.f_cls = f_cls
        
    def encrypt_info(self, info_tion, info_f_cls):
        """Encrypting information"""

        # encoding data from text to byte
        data_byte = info_tion.encode('utf-8')
        token_public = info_f_cls.encrypt(data_byte)
        return token_public # return type is <class 'bytes'>
    
    def decrypt_info(self, info_data, key):
        """For decryption"""

        t_base_ = Fernet(key)

        token_public = t_base_.decrypt(info_data)
        # decoding the token_public from byte to text
        data_text = token_public.decode()
        return data_text # return type is <class 'str'>
    
    def the_key(self):
        """
        The (self.token_generate) is times by 3, (total length is 372),
        so that we will randomly select from it without any restriction,
        since we make the minimum length of the key to be 205 and the maximum to be 357,
        and also it will randomly select from that range of (205 - 357),
        with a stepping of (7)
        """

        the_pass = self.token_generate * 3
        the_list = list(the_pass)
        random.shuffle(the_list) # shuffling the list

        # """
        # salting our passcode with this class method

        # By using the random sample method, where we make:
        #     population = the_list
        #     k = random.randrange(205, 357, 7)
        # """
        rand_key = ''.join(random.sample(the_list, random.randrange(205, 357, 7)))
        return rand_key # return type is str
    
    @property
    def fast_iteration(self):
        """
        We will use threading and multiprocessing in advance

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
        return f'Information encrypt and decrypt'
    

class MixinTrick:
    def sign_mix(sign_iteration, sign_hash, sign_salt, sign_private):
        """Method for instantiating item information joining (concatenating)"""

        # convert iteration from string to integer, and then multiply it by 2
        iteration_times = int(sign_iteration) * 2

        # [(itter * 2) - random.randint(1, 10, 2)] + gen_salt + key + hash
        d_1_graph = iteration_times - random.randrange(1, 10, 2)
        data_1 = str(d_1_graph) + sign_salt + sign_private.decode() + sign_hash

        # [(itter * 2) + random.randint(1, 9)] + hash + (itter * 2) + ''.join(random.sample(select_from_me, 1))
        select_from_me = 'internetcommunicationsecurity'
        d_2_graph = iteration_times + random.randint(1, 9)
        data_2 = str(d_2_graph) + sign_hash + str(iteration_times) + ''.join(random.sample(select_from_me, 1))

        # [(itter - random.randint(1, 10)) * 2] + private + hash + gen_salt
        d_3_graph = int(sign_iteration) - random.randint(1, 10)
        d_3_graph_2 = d_3_graph * 2
        data_3 = str(d_3_graph_2) + sign_private.decode() + sign_hash + sign_salt

        # [(itter - 13) * 2] + key + hash + [(itter * 2) - random.randint(3, 8)]
        d_4_graph = int(sign_iteration) - 13
        d_4_1_graph = d_4_graph * 2
        d_4_2_graph = iteration_times - random.randint(3, 8)
        data_4 = str(d_4_1_graph) + sign_private.decode() + sign_hash + str(d_4_2_graph)

        return [data_1, data_2, data_3, data_4]
        # the return are: (the_key, the_hash, the_private, ingredient) respectively
        

    def unsign_mix(add_key, add_hash, add_private, add_ingredient):
        """Method for getting item information unveil (splitting)"""

        itter_1 = add_hash[-4:] # negating the last four character
        itter_2 = itter_1[:-1] # negating the last character of (itter_1)

        # converting iteration to integer, and divide it by 2, also making sure it is in integer (without any decimal point)
        real_iteration = int(int(itter_2) / 2)

        hash_1 = add_hash[:-4] # negating the last four character
        real_hash = hash_1[3:] # negating the first three digit of (hash_1)


        key_1 = add_ingredient[3:-3] # negating the first three digit, and the last three
        real_key = key_1[:-len(real_hash)] # negating the hash, (leaving only the key)

        salt_1 = add_key[:-len(real_hash)] # removing the second hash
        salt_2 = salt_1[:-len(real_key)] # removing the key
        real_gen_salt = salt_2[3:] # negating the first three digit

        p1 = add_private[len(str(int(real_iteration) * 2)):] # negating the first three digit
        p2 = len(real_hash) + len(real_gen_salt) # adding length of hash and length of gen_hash
        real_private_key = p1[:-p2]

        return [real_gen_salt, real_iteration, real_hash, real_private_key]
    

class SliceDetector:
    """It slice old pass"""

    def __init__(self, request):
        self.request = request

        # """ingredient (salt + iteration + second hash) respectively"""
        old_ingredient = request.user.passcode.passcode_ingredient
        
        # """(second hash) from custome user model"""
        self.real_hash = request.user.passcode_hash
        # """(second hash) slicing it from old_ingredient"""
        self.slice_hash = old_ingredient[-len(self.real_hash):]
        
        # """
        # slicing ingredient from old_ingredient, starting from index zero to the actual length of the (real_hash) above
        # """
        self.slice_ingre = old_ingredient[: -len(self.slice_hash)]
        
        # """slicing iteration from the (slice_ingre) above from index -6 to the end"""
        self.slice_iter = self.slice_ingre[-6:]
        
        # """slicing salt from the first index of the (slice_ingre) to index -6"""
        self.slice_salt = self.slice_ingre[: -6]
        
    @property
    def _hash(self):
        """Hash value"""

        return self.slice_hash
    
    @property
    def _ingre(self):
        """Ingredient value"""

        return self.slice_ingre
    
    @property
    def _salt(self):
        """Salt value"""

        return self.slice_salt
    
    @property
    def _iter(self):
        """Iteration value"""

        return self.slice_iter
