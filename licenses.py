# import shortuuid
#
# def generate_short_key():
#     return shortuuid.ShortUUID().random(length=16)
#
#
# short_key = generate_short_key()
# print(short_key)

# import hashids
#
# hashids = hashids.Hashids(salt="your_salt", min_length=8)
# unique_id = hashids.encode(12345)
# print(unique_id)

import hashids
import string

hashids = hashids.Hashids(salt="ABCDEFGHJKLMNOBQRSTUVWXYZ", min_length=16, alphabet=string.ascii_uppercase + string.digits)
unique_id = hashids.encode(123456789, 123456789)
formatted_key = '-'.join(unique_id[i:i+4] for i in range(0, len(unique_id), 4))
print(formatted_key)




# DECODED_key = formatted_key.replace("-", "")


# decoded_id = hashids.decode(DECODED_key)
#
# print(decoded_id)


# import secrets
# import string
#
#
# def generate_secret_key(length=8):
#     characters = string.ascii_uppercase + string.digits
#     return ''.join(secrets.choice(characters) for _ in range(length))
#
#
# secret_key = generate_secret_key(16)
# print(secret_key)
