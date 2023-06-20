#!/bin/bash

# pokretanje shell scripte iz terminala: 
    # chmod +x script.sh
    # ./script.sh 

echo "Inicijalizacija master passworda"
python3 symmetric_cryptography.py --init mAssterPassword
echo " "


echo "Dodavanje nekoliko zapisa u bazu"
python3 symmetric_cryptography.py --put mAssterPassword www.a.com A123
python3 symmetric_cryptography.py --put mAssterPassword www.b.hr sifraBBB
python3 symmetric_cryptography.py --put mAssterPassword www.c.net Cpass99
echo " "

echo "Pokusaj dodavanja zapisa u bazu s pogresnim master passwordom "
python3 symmetric_cryptography.py --put nekiDrugiPass www.d.ba blabla
    # ispis: ValueError: MAC check failed
echo " "

echo "Promjena passworda za www.a.com"
python3 symmetric_cryptography.py --put mAssterPassword www.a.com aaa555
echo " "

echo "Dohvacanje passworda za web stranicu www.b.com"
python3 symmetric_cryptography.py --get mAssterPassword www.b.hr
    # ispis: Password za adresu www.b.hr je: sifraBBB
echo " "

echo "Dohvacanje passworda za web stranicu www.e.rs"
python3 symmetric_cryptography.py --get mAssterPassword www.e.rs
    # ispis: Ne postoji adresa www.e.rs u bazi.
echo " "

# baza nakon svih ovih naredbi sadrzi: 
    # www.b.hr;sifraBBB
    # www.c.net;Cpass99
    # www.a.com;aaa555



echo "Inicijalizacija novog master passworda"
python3 symmetric_cryptography.py --init massPass
    # baza je vracena na pocetno stanje te je prazna
echo " "