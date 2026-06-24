import string

BASE62 = string.digits + string.ascii_letters


def encode_base62(num):
    if num == 0:
        return "0"

    result = ""

    while num:
        result = BASE62[num % 62] + result
        num //= 62

    return result
