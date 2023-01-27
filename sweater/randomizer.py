import string
import secrets
import random




def random_after_slash():
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(7))
    return crypt_rand_string