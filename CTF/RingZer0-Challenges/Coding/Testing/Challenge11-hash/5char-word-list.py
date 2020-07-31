import string

first = list(string.ascii_lowercase)+list(string.digits)
second = list(string.ascii_lowercase)+list(string.digits)
third = list(string.ascii_lowercase)+list(string.digits)
fourth = list(string.ascii_lowercase)+list(string.digits)
fifth = list(string.ascii_lowercase)+list(string.digits)
sixth = list(string.ascii_lowercase)+list(string.digits)
word = ['','','','','','']

hashfile = open('5char.txt', 'a')

# Loop add
for a in first:
    word[0] = a
    for b in second:
        word[1] = b
        for c in third:
            word[2] = c
            for d in fourth:
                word[3] = d
                for e in fifth:
                    word[4] = e
                    for f in sixth:
                        word[5] = f
                        res = str("".join(word))
                        hashfile.write(res + ('\n'))

hashfile.close()
