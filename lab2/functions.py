from base64 import b64encode
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import os
from Crypto.Random import get_random_bytes

# povjeri jel user postoji u bazi 
def checkUser(username):
    file = open('baza.txt', 'r')
    data = file.read()
    dataList = data.split('\n')

    useri = []
    for red in dataList:
        red = red.split(chr(29))
        useri.append(red[0])

    if username in useri:
        return True # prodi po cijeloj bazi i ako ima usera vrati True

    return False    # ako nema usera u bazi vrati False

# dodaj u bazu usera, hash_pass, salt
def addUser(username, password):
    password = bytes(password, 'UTF-8')
    salt = get_random_bytes(16)
    salt = b64encode(salt).decode('utf-8') # bytes -> str
    
    hash_password = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    hash_password = b64encode(hash_password).decode('utf-8') # bytes -> str

    noviUnos = []
    noviUnos.append(username)
    noviUnos.append(hash_password)
    noviUnos.append(salt)
    redak = chr(29).join(noviUnos)

    file = open('baza.txt', 'r')
    data = file.read()
    file.close()

    data = data + '\n' + redak

    file = open('baza.txt', 'w')
    file.write(data)
    file.close()

    return 

# promijeni pass useru -> izbrisi tog usera i dodaj istog tog usera s novim pass
def changePassword(username, new_password):
    deleted = deleteUser(username=username)

    if (deleted):
        addUser(username=username, password=new_password)
        return True

    else:
        return False

# dodaj 1 kao flag na kraju red u kojem je user od kojeg se trazi da promijeni pass
def addFlag(username):
    file = open('baza.txt', 'r')
    data = file.read()
    file.close()

    dataList = data.split('\n')

    promijeni = ''   
    for red in dataList:
        red = red.split(chr(29))
        if red[0] == username:
            if (red[-1] == '1'): # ako vec ima oznaku nemoj joj dat jos jednu 
                continue
            red.append('1') # flag = 1 --> oznaka da se ocekuje od usera da si sam promijeni pass
            promijeni = chr(29).join(red) # zapis koji ce ic u bazu 

    if promijeni != '':
        izbrisan = deleteUser(username=username) # izbrisi cijeli redak u kojem je ovaj username, tako da mozemo dodat novi, isti takav samo s 1 na kraju 

        if izbrisan:
            file = open('baza.txt', 'r')
            data = file.read()
            file.close()

            data = data + '\n' + promijeni

            file = open('baza.txt', 'w')
            file.write(data)
            file.close()

        else: 
            print('greska')

        return True

    else: 
        return False

# obrisi usera iz baze (cijeli redak u kojem je taj username)
def deleteUser(username):
    file = open('baza.txt', 'r')
    data = file.read()
    file.close()

    dataList = data.split('\n')

    zaBrisanje = ''
    for red in dataList:
        red = red.split(chr(29))
        if red[0] == username:
            zaBrisanje = chr(29).join(red)

    if zaBrisanje != '':
        dataList.remove(zaBrisanje)
        data = '\n'.join(dataList)

        file = open('baza.txt', 'w')
        file.write(data)
        file.close()

        return True 

    else:
        return False 
