# -*- coding: utf-8 -*-
import random

"""PasscodeSecurity is imported for use in the secureapp views, as well as InformationSecurity too"""
from . contrib import PasscodeSecurity
from . crypt_info import InformationSecurity


class MixinTrick:
    def _instance_item_data(INS_iteration, INS_hash, INS_salt, INS_private):
        """
        a method for instantiating item information joining (concatenating) it according to our algorithm
        """

        # convert iteration from string to integer, and then multiply it by 2
        iteration_times = int(INS_iteration) * 2

        # [(itter * 2) - random.randint(1, 10, 2)] + gen_salt + key + hash
        d_1_graph = iteration_times - random.randrange(1, 10, 2)
        data_1 = str(d_1_graph) + INS_salt + INS_private.decode() + INS_hash

        # [(itter * 2) + random.randint(1, 9)] + hash + (itter * 2) + "".join(random.sample(select_from_me, 1))
        select_from_me = "internetcommunicationsecurity"
        d_2_graph = iteration_times + random.randint(1, 9)
        data_2 = str(d_2_graph) + INS_hash + str(iteration_times) + "".join(random.sample(select_from_me, 1))

        # [(itter - random.randint(1, 10)) * 2] + private + hash + gen_salt
        d_3_graph = int(INS_iteration) - random.randint(1, 10)
        d_3_graph_2 = d_3_graph * 2
        data_3 = str(d_3_graph_2) + INS_private.decode() + INS_hash + INS_salt

        # [(itter - 13) * 2] + key + hash + [(itter * 2) - random.randint(3, 8)]
        d_4_graph = int(INS_iteration) - 13
        d_4_1_graph = d_4_graph * 2
        d_4_2_graph = iteration_times - random.randint(3, 8)
        data_4 = str(d_4_1_graph) + INS_private.decode() + INS_hash + str(d_4_2_graph)

        return [data_1, data_2, data_3, data_4]
        # the return are: (the_key, the_hash, the_private, ingredient) respectively
        

    def _3_to_3(add_the_key, add_the_hash, add_the_private, add_ingredient):
        """
        a method for getting item information unveil (splitting) it according to our algorithm
        """

        itter_1 = add_the_hash[-4:] # negating the last four character
        itter_2 = itter_1[:-1] # negating the last character of (itter_1)

        # converting iteration to integer, and divide it by 2, also making sure it is in integer (without any decimal point)
        real_iteration = int(int(itter_2) / 2)

        hash_1 = add_the_hash[:-4] # negating the last four character
        real_hash = hash_1[3:] # negating the first three digit of (hash_1)


        key_1 = add_ingredient[3:-3] # negating the first three digit, and the last three
        real_key = key_1[:-len(real_hash)] # negating the hash, (leaving only the key)

        salt_1 = add_the_key[:-len(real_hash)] # removing the second hash
        salt_2 = salt_1[:-len(real_key)] # removing the key
        real_gen_salt = salt_2[3:] # negating the first three digit

        p1 = add_the_private[len(str(int(real_iteration) * 2)):] # negating the first three digit
        p2 = len(real_hash) + len(real_gen_salt) # adding length of hash and length of gen_hash
        real_private_key = p1[:-p2]

        return [real_gen_salt, real_iteration, real_hash, real_private_key]
    

# __all__ = [
#   "PasscodeSecurity",
#   "InformationSecurity",
#   "MixinTrick",
#   ]
