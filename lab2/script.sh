#!/bin/bash

# pokretanje shell scripte iz terminala: 
    # chmod +x script.sh
    # ./script.sh 


# usermgmt.py
echo "Base initialization"
python3 usermgmt.py --init baza
echo " "


echo "Try adding user iva"
python3 usermgmt.py --add iva
echo " "

echo "Try adding user marko"
python3 usermgmt.py --add marko
echo " "

echo "Try adding user ante"
python3 usermgmt.py --add ante
echo " "

echo "Try adding user ana with password length less than 10 characters"
python3 usermgmt.py --add ana
echo " "
# greska -> prekratak pass

echo "Try adding user ana with password != repeat password"
python3 usermgmt.py --add ana
echo " "
# greska -> password mismatch


echo "Change password for user iva"
python3 usermgmt.py --changePass iva
echo " "

echo "Request user marko to change password on next login."
python3 usermgmt.py --forcePass marko
echo " "


echo "Remove user ante."
python3 usermgmt.py --delete ante
echo " "


# login.py
echo "Try log in as user iva"
python3 login.py iva
echo " "

echo "Try log in as user marija which is not in base"
python3 login.py marija
echo " "
# greska -> krivi username / password

echo "Try log in as user iva with wrong password"
python3 login.py iva
echo " "
# greska -> krivi username / password

echo "Try log in as user marko"
python3 login.py marko
echo " "
# trazit ce ga da promijeni password