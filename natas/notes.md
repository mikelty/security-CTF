### overthewire - natas (cybersecurity CTF)
this post tries to focus on methods and implementations as passwords / flags change frequently<br />
getting burp set up with firefox and some basic math & programming experience are kinda required in order to follow this guide<br />
when in doubt, read the provided source code and google the rest

0. view source
1. view source
2. directory traversal
    * tracker image hint in source code
    * simple file tree (http://natas2.natas.labs.overthewire.org/files/users.txt)
3. robots.txt hack
    * first, go to http://natas3.natas.labs.overthewire.org/robots.txt
    * then go to http://natas3.natas.labs.overthewire.org/s3cr3t/users.txt
4. request forgery
    * follow instructions on the page and change referer in burp
5. request forgery
    * similar to 4, change loggedin to 1 in burp
6. directory traversal
    * go to http://natas6.natas.labs.overthewire.org/includes/secret.inc and submit the secret
7. directory traversal with php
    * web projects tend to rest a couple levels beneath the root
    * php routers are kinda naive compared to modern frameworks
    * http://natas7.natas.labs.overthewire.org/index.php?page=../../../../../../../etc/natas_webpass/natas8
8. baby cryptography
    * reverse php processing
    * ```f(g(x))=y <=> g'(f'(y))=x```, g' and f' are inverses of g and f.
    * [implementation](./eight.php)
9. grep exploit
    * > ```.* /etc/natas_webpass/natas<next>```
    * reason: dot (.) matches for all single characters, while star (*) matches for all lengths. together they mean 'match anything and everything'. so grep becomes cat here.
10. same as 9
11. elementary cryptography
    * similar to 8. but one more trick:
        * ```a xor a = 0```, and thus:
        * ```a xor b = c => c xor b = a xor b xor b = a```
        * ```plaintext xor key = ciphertext```, and thus:
        * ```ciphertext xor plaintext = key```
    * this is done in [here](./eleven_key.php)
    * once we get the key the rest is the same as 8
    * this is done in [here](./eleven_attack.php)
12. file upload exploit
    * the first two bytes of a jpg image tells php that it is a jpg image. so grab those two bytes along with the shell code.
    * [file to upload](./twelve.php)
    * upload the file and change filename to something.php (like a.php) using burp, so the server parses it
13. same as 12.
14. elementary sql injection
    * > ```" or 1=1#```
    * reasons:
        * the quotation mark breaks out of the username context
        * ```or```is executed after ```and``` in general (although not used here)
        * 1 is always equal to 1, so ```1=1``` means True
        * as a result, the expression will always evaluate to true, bypassing password
15. normal sql injection
    * leak password one character at a time using the ```LIKE``` function in MySQL
    * if ```LIKE(<known-password><new-char>%)``` returns true, then the user exists.
    * [implementation](./fifteen.py), perhaps it's easier to understand watching it run
16. grep leak (similar to 15)
    * the logic behind this attack is basically the same as the last level
    * > ```$(grep -E ^<known-password><new-char>.* /etc/natas_webpass/natas17)```
    * ```$(<expr>)``` evaluates ```<expr>``` and let the rest of the shell code treat its result as instruction
    * in this example, ```<expr>``` yields password if ```<new-char>``` is a valid guess
    * ```-E``` flag allows one to use an expression
    * ```^``` is start of string, to force our guess to start at the first char of the actual password, but not other slices of it.
    * [implementation](./sixteen.py)
17. blind sql injection - timing attack
    * this one can take a while to think and to execute
        * MySQL has this function called ```SLEEP```, putting the query engine to sleep for specified time
        * MySQL also short-circuit logical evaluations, so if A is false, MySQL does not evaluate B when evaluating ```A and B```
    * together, they form the following solution:
        * ```" and password like <known-password><new-char> and sleep(<some-time>)```
        * the time to sleep is safer above two seconds
        * one need to wrap this query around a rather accurate timer
    * [implementation](./seventeen.py)
18. session impersonation
    * one key observation is one of the session id is admin's and has more priviledge
    * this observation along with a low number of possible session ids suggest a brute-force attack
    * [implementation](./eighteen.py)
19. session impersonation, elementary encryption
    * through observation or experience one determines that session-id is the hex value of ```<numerical-id>-<username>```, where ```<numerical-id>``` is the same as the last level
    * observation of the flow of information or experience with cryptography is important in a later level of natas (28)
    * [implementation](./nineteen.py)
20. ```explode``` function in php
    * through rather careful thinking, an associated array with ```admin => 1``` as an entry is the goal
    * observe that we can put a new line between the name variable's value and the injected pair (admin, 1) to fool ```explode``` and the several lines after it
    * > http://natas20.natas.labs.overthewire.org/index.php?debug&name=%0Aadmin%201
        * refresh the page to see flag, as the server is able to read the admin element upon the second request, which was written by the first request
21. colocation
    * colocated machines share hardware resources
    * session variable shared across requests
    * ```session_start``` can also resume an ongoing session, according to manual
    * implementation:
        * navigate to the [experimenter server](http://natas21-experimenter.natas.labs.overthewire.org/)
        * clear all cookies starting with natas21
        * use burp to append ```admin=1``` at the end of the variable list
        * navigate to the original page
22. redirection
    * ```header``` redirects user to its parameter, a single slash means home page
    * most browsers can stop redirection for configured sites
    * in python, use ```requests.get``` and set ```allow_redirection=False```
    * [implementation](./twentytwo.py)
23. php numeric comparison
    * apparently php treats strings as partial numbers when it can interpret strings as such.
    * > 100iloveyou
24. ```strcmp``` exploit
    * there are many loopholes to ```strcmp``` in php
    * one is particularly bad, that an array would be treated as equal to string
    * shorthand of specifying array (at least in URL) is ```<variable>[]```
    * > http://natas24.natas.labs.overthewire.org/index.php?passwd[]=0
25. mature cyber attack
    * this is when the natas levels first show its teeth (this level is quite hard)
