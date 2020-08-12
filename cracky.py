import sys
import subprocess
import itertools

#argument 1: hash file name
#Note: will remove hashcat.potfile
#Note: next version--> append before the username
#----------------Hash file of format username:id:lmhash:nthash-------------------------

#----------------Creating duplicate ntds file and file with only NTLM Hash-------------------------------------------
command="cp " + sys.argv[1]+" duplicatentds.txt"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

file1=open("duplicatentds.txt","r")
file2=open("only_ntlmhash.txt","w")
r=file1.readline()
while(len(r)!=0):
	r=r.split(":")
	file2.write(r[3])
	r=file1.readline()
file1.close()
file2.close()

#-----------------Running rockyou.txt file----------------------------------------------
command="rm /root/.hashcat/hashcat.potfile"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

command="hashcat -m 1000 only_ntlmhash.txt /usr/share/wordlists/rockyou.txt --force"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

verify_crack={}
hashcrack=open("/root/.hashcat/hashcat.potfile","r")
r=hashcrack.readlines()
for i in r:
	i=i.split(":")
	i[1]=i[1].replace("\n","")
	verify_crack[i[0]]=i[1]
hashcrack.close()
duplicatefile=open("duplicatentds.txt","r")
tempfile=open("tempfile.txt","w")
r=duplicatefile.readline()
while(len(r)!=0):
	flag=0
	for hashes, passwd in verify_crack.items():
		if hashes in r:
			r=r.split(":")
			print r[0]+":"+passwd
			flag=1
	if(flag==0):
		tempfile.write(r)
	r=duplicatefile.readline()
tempfile.close()
duplicatefile.close()

#---------------Clearing the temp file-------------------------------------
command="rm duplicatentds.txt only_ntlmhash.txt"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

command="mv tempfile.txt duplicatentds.txt"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


#----------------Creating only LMHash file----------------------------------------------
only_lmhash=open("only_lmhash.txt","w")
lmhash_verify=open("verify_lmcrack.txt","w")
mainfile=open("duplicatentds.txt","r")

r=mainfile.readline()
while(len(r)!=0):
	r=r.split(":")
	m=r[3]#NTLM Hash	
	r=r[2]#LM Hash	
	if(r!="aad3b435b51404eeaad3b435b51404ee"):#LM hash for empty
		only_lmhash.write(r)
		only_lmhash.write("\n")
		lmhash_verify.write(m)	
	r=mainfile.readline()
only_lmhash.close()
mainfile.close()
lmhash_verify.close()

#----------------Cracking LMHash if any------------------------------------------------
command="rm /root/.hashcat/hashcat.potfile"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

command="hashcat -m 3000 only_lmhash.txt /usr/share/wordlists/rockyou.txt --force"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

lm_crack_dict={}
hashcrack=open("/root/.hashcat/hashcat.potfile","r")
r=hashcrack.readlines()
for i in r:
	i=i.split(":")
	i[1]=i[1].replace("\n","")
	lm_crack_dict[i[0]]=i[1]
	r=hashcrack.readline
hashcrack.close()
#print(lm_crack_dict)
lm_hash=open("only_lmhash.txt","r")
lmhash=open("lmhash_crack.txt","w")
filedata=lm_hash.read()
for hashes, passwd in lm_crack_dict.items():
	filedata=filedata.replace(hashes,passwd)
lmhash.write(filedata)
lmhash.close()
lm_hash.close()


#----------------Creating password list from cracked lm password-------------------------------------
lmhash=open("lmhash_crack.txt","r")
final=open("final.txt","w")

r=lmhash.readline()
while(len(r)!=0):
	chars=r
	results = list(map(''.join, itertools.product(*zip(chars.upper(), chars.lower()))))
	r=lmhash.readline()
	for i in results:
		final.write(i)	
lmhash.close()
final.close()



#----------------LM cracked, verifing with ntlm hash--------------------------------------------
command="rm /root/.hashcat/hashcat.potfile"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

command="hashcat -m 1000 verify_lmcrack.txt final.txt --force"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

#---------------print username and password---------------------------------------------------
verify_lmcrack={}
hashcrack=open("/root/.hashcat/hashcat.potfile","r")
r=hashcrack.readlines()
for i in r:
	i=i.split(":")
	i[1]=i[1].replace("\n","")
	verify_lmcrack[i[0]]=i[1]
	r=hashcrack.readline
hashcrack.close()
duplicatefile=open("duplicatentds.txt","r")
tempfile=open("tempfile.txt","w")
r=duplicatefile.readline()
while(len(r)!=0):
	flag=0
	for hashes, passwd in verify_lmcrack.items():
		if hashes in r:
			r=r.split(":")
			print r[0]+":"+passwd
			flag=1
	if(flag==0):
		tempfile.write(r)
	r=duplicatefile.readline()
tempfile.close()
duplicatefile.close()

#--------------------Clearing the temp file-------------------------
command="rm duplicatentds.txt only_lmhash.txt lmhash_crack.txt final.txt verify_lmcrack.txt"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

command="mv tempfile.txt duplicatentds.txt"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
#-------------------------------------------------END OF PASSWORD CRACK FROM LMHASH-------------------------
#-------------------------------------------------Creating password list using user name--------------------
#----------------Creating only username:NTHash file----------------------------------------------
mainfile=open("duplicatentds.txt","r")
username={}
r=mainfile.readline()
while(len(r)!=0):
	r=r.split(":")
	username[r[0]]=r[3]
	r=mainfile.readline()
mainfile.close()
#-------------------------removing hashcat.pofile-----------------------------------
command="rm /root/.hashcat/hashcat.potfile"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
for user,hashes in username.items():
	wordlist=open("temp.txt","w")
	user=user.replace(".","")
	wordlist.write(user)
	wordlist.write("\n")
	results = list(map(''.join, itertools.product(*zip(user.upper(), user.lower()))))
	for i in results:
		wordlist.write(i)
		wordlist.write("\n")
	wordlist.close()
	wordlist=open("temp.txt","a+")
	filedata=wordlist.read()
	filedata=filedata.replace("a","@")
	filedata=filedata.replace("o","0")
	filedata=filedata.replace("s","5")
	wordlist.write(filedata)
	wordlist.close
	wordlist=open("temp.txt","a+")
	r=wordlist.readline()
	to_added=[]
	while(len(r)!=0):
		append=open("appendfile.txt","r")
		string=append.readline()
		r=r.replace("\n","")
		while(len(string)!=0):
			to_added.append(r+string)
			string=append.readline()
		append.close()
		r=wordlist.readline()	
	for i in to_added:
		wordlist.write(i)
	wordlist.close()
	ntlm=open("ntlmhash.txt","w")
	ntlm.write(hashes)
	ntlm.close()
	#--------------Running hashcat for user and corresponding wordlist

	command="hashcat -m 1000 ntlmhash.txt temp.txt --force"
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

#---------------print username and password---------------------------------------------------
verify_ntlmcrack={}
hashcrack=open("/root/.hashcat/hashcat.potfile","r")
r=hashcrack.readlines()
for i in r:
	i=i.split(":")
	i[1]=i[1].replace("\n","")
	verify_ntlmcrack[i[0]]=i[1]
	r=hashcrack.readline
hashcrack.close()
duplicatefile=open("duplicatentds.txt","r")
tempfile=open("tempfile.txt","w")
r=duplicatefile.readline()
while(len(r)!=0):
	flag=0
	for hashes, passwd in verify_ntlmcrack.items():
		if hashes in r:
			r=r.split(":")
			print r[0]+":"+passwd
			flag=1
	if(flag==0):
		tempfile.write(r)
	r=duplicatefile.readline()
tempfile.close()
duplicatefile.close()

