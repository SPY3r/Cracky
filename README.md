# Cracky
While doing a pentest of Active Directory, often we land our hands-on passwords. With legacy systems rarely found and Microsoft upgrading the encryption, it is rare to get a hands-on password in plain text. The password is either stored in LM or NetHash format. Of course, it takes minutes to crack the LM hash.  It takes a long time for an average computer to crack an NTLM hash. So to minimize the time to crack a dump of usernames and respective hashes, I wrote a script. 

This script first tries to crack the NTLM hash through rockyou.txt wordlist from a file containing usernames and respective hashes in the format:  &lt;username>:&lt;id>:&lt;LM>:&lt;NTLM>.  

Any success will output on the terminal and respective username will be removed from the list of remaining to be cracked.  

Further, the script will crack the LM hashes (ignoring the blank) and compute all possible combinations of the password. These combinations will be used to crack the NTLM hashes. 

Any success will output on the terminal and respective username will be removed from the list of remaining to be cracked. 

Finally, the script will use usernames and create combinations to crack the remaining NTLM hashes. 

Any success will output on the terminal and respective username will be removed from the list of remaining to be cracked.   How to improve the output of the script? Update the "append.txt" file and add the cracked passwords to the wordlist which can be used next time. 

OS: Linux
