from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import os, argparse
from base64 import b64encode

def encrypt(mass_pass, data):
    mass_pass = bytes(mass_pass, 'UTF-8')

    # generiraj random salt pri svakom initu, velicine 16*8 = 128 bitova 
    salt = get_random_bytes(16)

    # generiraj random string koji na pocetku sluzi za to da mozemo nesto kriptirat nakon pocetnog inita
    secret_string = get_random_bytes(16)
    secret_string = b64encode(secret_string).decode('utf-8')

    # dobij privatan kljuc iz mass_pass i salt-a
    private_key = PBKDF2(mass_pass, salt, 32, count=1000000, hmac_hash_module=SHA512)
    cipher = AES.new(private_key, AES.MODE_GCM)
    data = secret_string + data
    cipher_data, tag = cipher.encrypt_and_digest(bytes(data, 'UTF-8'))  

    # spremanje u bazu chiper.nonce (iv) + tag + cipher_data (kriptirani secret string na pocetku, kasnije uz to i data tj parovi adr;loz)
    file = open('baza.bin', 'wb')
    file.write(salt)         # 16 bajtova
    file.write(cipher.nonce) # 16 bajtova
    file.write(tag)          # 16 bajtova
    file.write(len(secret_string).to_bytes(2, 'big')) # 2 bajta
    file.write(cipher_data)  # od 50. bajta do kraja: secret_string + parovi adr;loz
    file.close()

def decrypt(mass_pass):
    file = open('baza.bin', 'rb')
    salt = file.read(16)
    nonce = file.read(16)
    tag = file.read(16)
    ss_len = int.from_bytes(file.read(2), byteorder='big')
    cipher_data = file.read() # od 50.bajta do kraja je kriptirani data = secret_string + parovi adr;loz

    private_key = PBKDF2(mass_pass, salt, 32, count=1000000, hmac_hash_module=SHA512)
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
    data = cipher.decrypt_and_verify(cipher_data, received_mac_tag=tag) # dekriptirani data = secret_string + parovi adr;loz

    # vrati data koji nije secret string, nego sve nakon njega (parovi adr;loz)
    return data[ss_len:].decode('utf-8')


# parse input
parser = argparse.ArgumentParser()
parser.add_argument('--init', type=str, default='')
parser.add_argument('--put', type=str, nargs='+', default=[])
parser.add_argument('--get', type=str, nargs='+', default=[])
args = parser.parse_args()

# read arguments
if (args.init):
    # stvori bazu ako ne postoji vec, ako postoji obrisat ju (tj sadrzaj iz nje) i napravit na tom mjestu novu, cistu  
    open(os.path.abspath(os.getcwd()) + '/baza.bin', 'w')

    # enkriptiraj secret string smao 
    encrypt(args.init, '')

elif (args.put):
    # dekriptiraj kriptirani sadzaj baze
    data = decrypt(args.put[0])

    # dodaj/promijeni --> ako vec postoji ta adresa promijeni pass --> 1 red 1 par oblika adr;loz
    lista = []
    lista.append(args.put[1])
    lista.append(args.put[2])

    dataList = data.split('\n')
    dataList.remove('')


    dictionary = {}
    for elem in dataList:
        elem = elem.split(';')
        dictionary[elem[0]] = elem[1]

    if lista[0] in dictionary:
        for elem in dataList:
            elem = elem.split(';')
            if elem[0] == lista[0]:
                dataList.remove(';'.join(elem))
    
    dataList.insert(0, '')
    data = '\n'.join(dataList)
    par = ';'.join(lista)
    data = data + '\n' + par

    #print('Sadrzaj baze: ', data)

    # enkriptiraj
    encrypt(args.put[0], data)

elif (args.get):
    # dekriptiraj
    data = decrypt(args.get[0])

    # nadi 
    dataList = data.split('\n')
    dataList.remove('')

    dictionary = {}
    for elem in dataList:
        elem = elem.split(';')
        dictionary[elem[0]] = elem[1]

    if args.get[1] in dictionary:
        for elem in dataList:
            elem = elem.split(';')
            if elem[0] == args.get[1]:
                print('Password za adresu {} je: {}'.format(elem[0], elem[1]))
    else:
        print('Ne postoji adresa {} u bazi.'.format(args.get[1]))

    # enkriptiraj
    encrypt(args.get[0], data)


