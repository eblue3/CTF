from pwn import *
import os

# Stage 1
args = ['A']*100
args[65] = '\x00'
args[66] = '\x20\x0a\x0d'
args[67] = '4444'

# Stage 2
r1, w1 = os.pipe()
r2, w2 = os.pipe()
os.write(w1, '\x00\x0a\x00\xff')
os.write(w2, '\x00\x0a\x02\xff')

# Stage 4
with open('\x0a', 'w') as f:
	f.write('\x00\x00\x00\x00')

# Stage 3
p = process(executable='/home/input2/input', 
	    argv=args, 
	    stdin=r1, stderr=r2, 
	    env={'\xde\xad\xbe\xef' :'\xca\xfe\xba\xbe'})

# Stage 5
conn = remote('localhost', 4444)
conn.sendline('\xde\xad\xbe\xef')

p.interactive()