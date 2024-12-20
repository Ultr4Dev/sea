import random
import string


def random_string(n=8, prefix=""):

    return prefix + "".join(random.choices(string.ascii_letters + string.digits, k=n))
