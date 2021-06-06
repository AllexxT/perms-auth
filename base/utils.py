import string
import random


def random_password(length_=10):
    ran = ''.join(random.choices(string.ascii_letters + string.digits, k=length_))
    return str(ran)
