### Mindgames 1336 1337 1338 challenge

- use libc.so.6 for calculating offsets

Get help from here about byapssing vuln function calling logic =  https://ctftime.org/writeup/23789

- Imports necessary modules such as re, datetime, ctypes, and pwn.
- Sets up the binary and context, specifying architecture, log level, terminal, etc.
- Establishes a connection with the remote target mindgames.secenv on port 1336, 1337, 1338
- Receives a date and time string from the server, extracts the timestamp, and uses it as a seed for the random number generator.
- Utilizes the rand() function from libc.so.6 to generate random numbers.
- Extracts the first random value and calculates the highscore.
- Sends commands and random values to the server based on the game's logic.
- Exploits a buffer overflow vulnerability to leak addresses from the server's memory.
- Calculates the base address of the binary and the libc library.
- Constructs a ROP (Return-Oriented Programming) chain to bypass NX (No eXecute) bit protection.
- Uses gadgets from the libc library to build the ROP chain.
- Constructs a payload containing the ROP chain to execute arbitrary commands.
- Sends the final payload to the server to exploit the vulnerability.
- After successful exploitation, gains an interactive shell to interact with the server.

In this exploit, the attacker establishes remote connections with targets named 1336, 1337, and 1338, extracting date and time information from the initial connection to use as a seed for the random number generator. By manipulating specific menu options, they bypass random validation checks, enabling further exploitation.

The attacker's strategy evolves as they progress through different challenges. In the first challenge, they bypass ASLR mitigation by leaking the binary's base address through overwriting the new_name pointer address. They then update the base address accordingly. In the next challenge, where Position Independent Executable (PIE) is enabled, they leak the pointer new_name's address to find the binary's base address.

Subsequently, they target libc, crafting payloads to leak libc function addresses and calculate the libc base address. With this information, they execute return-to-libc attacks, utilizing system functions and pop gadgets to spawn a shell with `/bin/sh`.

As challenges intensify with stack canaries implemented, the attacker crafts payloads to leak the canary's address by leveraging libc's `environ` variable and printing addresses to extract the canary value. Finally, they bypass NX (No-Execute) bit protection using Return-Oriented Programming (ROP) techniques, constructing a payload to execute a shell with system function, thus gaining interactive access. Through meticulous exploitation and bypassing of security mitigations, the attacker achieves their objective of gaining control over the target system.
