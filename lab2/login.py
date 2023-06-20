from base64 import b64encode
from getpass import getpass
import sys
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512

from functions import changePassword


args = sys.argv
username = args[1]

password = getpass(prompt='Password: ')

file = open('baza.txt', 'r')
data = file.read()
file.close()

dataList = data.split('\n')

nasli = False
for red in dataList:
    red = red.split(chr(29)) # splitaj po group separatoru da dobijemo red = [username, hash_pass, salt]

    if red[0] == username:
        nasli = True 

        # admin je dodao useru flag da mora sam promijenit pass 
        if (red[-1] == '1'):
            password = bytes(password, 'UTF-8')

            hash_password_check = PBKDF2(password, red[2], 32, count=1000000, hmac_hash_module=SHA512)
            hash_password_check = b64encode(hash_password_check).decode('utf-8')
            
            # uspored hasheve
            if (red[1] == hash_password_check):
                new_password = getpass(prompt='New password: ')
                repeat_new_password = getpass(prompt='Repeat password: ')

                if (new_password != repeat_new_password):
                    print('Changing password failed. Password mismatch.')

                else:
                    if len(password) < 10: 
                        print('Password must contain at least 10 characters.')

                    else:
                        changed = changePassword(username=username, new_password=new_password)
                        if changed:
                            print('Login successful.')

                        else:
                            print('Username or password incorrect.')

            # nije unesen ispravan (stari) password 
            else:
                print('Username or password incorrect.')

        # admin nije dodao useru flag da mora sam promijenit pass 
        else:
            password = bytes(password, 'UTF-8')

            hash_password_check = PBKDF2(password, red[2], 32, count=1000000, hmac_hash_module=SHA512)
            hash_password_check = b64encode(hash_password_check).decode('utf-8')
            
            # provjeri hasheve
            if (red[1] == hash_password_check):
                print('Login successful.')
            else:
                print('Username or password incorrect.')

# nema usera u bazi s tim usernameom
if not nasli:
    print('Username or password incorrect.')