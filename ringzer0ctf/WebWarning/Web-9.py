import hashlib

hashres = "0e612198634316944013585621061115"
#salt = b"vunp"

for i in range (0,100000000000):
    keystr = str(i).encode('utf-8')
    hash = hashlib.md5(keystr).hexdigest()
    print("Hashing ", keystr)
    if hash == hashres:
        print("Result: ",keystr)
        break
