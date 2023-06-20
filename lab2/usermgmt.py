import argparse
from getpass import getpass
import os

from functions import checkUser, addUser, changePassword, addFlag, deleteUser


# parse input
parser = argparse.ArgumentParser()
parser.add_argument('--init', type=str, default='')
parser.add_argument('--add', type=str, default='')
parser.add_argument('--changePass', type=str, default='')
parser.add_argument('--forcePass', type=str, default='')
parser.add_argument('--delete', type=str, default='')
args = parser.parse_args()

# inicijalizacija ciste nove baze --> obavezno prilikom prvog pokretanja programa
if (args.init):
    # stvori novu praznu bazu 
    open(os.path.abspath(os.getcwd()) + '/baza.txt', 'w')

# dodavanje novog usera 
elif (args.add):
    username = args.add

    password = getpass(prompt='Password: ')             
    repeatPass = getpass(prompt='Repeat Password: ')

    if (password != repeatPass):
        print('Adding user ' + username + ' failed. Password mismatch.')
    
    else:
        # min 10 znakova da se osiguramo od napada brute forceom (potrebno (126-33) na 10 = 93 na 10 mogucih kombinacija)
        if len(password) < 10:
            print('Password must contain at least 10 characters.')

        else:
            userExists = checkUser(username=username)
            if userExists:
                print('User ' + username + ' already exists.')

            else:
                addUser(username=username, password=password)
                print('User ' + username + ' successfully added.')

# admin mijenja korisniku password 
elif (args.changePass):
    username = args.changePass
    new_password = getpass(prompt='New password: ')
    repeatPass = getpass(prompt='Repeat password: ')

    if (new_password != repeatPass):
        print('Password change failed. Password mismatch.')

    else:
        changed = changePassword(username=username, new_password=new_password)
        if changed:
            print('Password changed successfully.')

        else:
            print('Password can not be changed because user does not exist in base.')

# admin trazi od korisnika da si sam promijeni pass pri sljedecem loginu (korinsika dobiva zastavicu 1 u redu u kojem je njegov username)
elif (args.forcePass):
    username = args.forcePass
    addedFlag = addFlag(username=username)
    if addedFlag:
        print('User ' + username + ' will be requested to change password on next login.')

    else:
        print('User ' + username + ' will not be requested to change password on next login beacuse he does not exist in base.')

elif (args.delete):
    username = args.delete
    deleted = deleteUser(username=username)
    if deleted:
        print('User ' + username + ' removed successfully.')

    else:
        print('User ' + username + ' can not be removed becouse he does not exist in base.')



# idea - ogranicenja za pass
# samo duljina jer je ona najbitnija
# kompleksnost ne toliko koliko duljina, ako imamo duljina 10+ kompleksnonst vise ne igra ulogu 
# rijecnici, kompromitirani pass, novi pass jednak kao stari -> dobro bi bilo provjeravat al nije nuzno (niti implementirano) za ovaj lab

# idea - spremanje u txt bazu
# zapis u obliku: 1 red 1 user, svaki red oblika username hashPass salt odvojeni ascii zankom 29
# nemozemo dobit pass ih poznatog hasha i salta jer koritimo PBKDF2 koji ima 1,000,000 iteracija (hashira se 1,000,00 puta prije nastajanja hash_passworda)