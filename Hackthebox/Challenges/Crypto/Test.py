import codecs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from binascii import unhexlify
data = input("Hex: ")
data = unhexlify(data)
print(data)
print(data[4])
data = chr(ord(data[4])^1)
print(data)
