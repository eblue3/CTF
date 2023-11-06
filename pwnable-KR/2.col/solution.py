from pwn import *

# check_password function add up 5 piece of int into the hash
# -> divide the password into 5, or 4 + remainder
payload = '\x01' * 96 + '\x04\xa0\x04\x08' + '\xea\x85\x04\x08'

r = ssh('col' ,'pwnable.kr' ,password='guest', port=2222)
p = r.process(executable='./col', argv=['col', payload])
flag = p.recv()
log.success(str(flag))

# python solution.py
# [x] Connecting to pwnable.kr on port 2222
# [+] Connecting to pwnable.kr on port 2222: Done
# [*] fd@pwnable.kr:        
#     Distro    Ubuntu 16.04
#     OS:       linux       
#     Arch:     amd64       
#     Version:  4.4.179     
#     ASLR:     Enabled     
# [x] Starting remote process bytearray(b'./col') on pwnable.kr
# [+] Starting remote process bytearray(b'./col') on pwnable.kr: pid 355959
# [+] b'daddy! I just managed to create a hash collision :)\n'