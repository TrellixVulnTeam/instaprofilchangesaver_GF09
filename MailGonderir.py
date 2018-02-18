#!/usr/bin/env python
# -*- coding: cp1254 -*-

import urllib.request
import bs4 as bs
import datetime
import openpyxl
import difflib
import smtplib
from openpyxl import Workbook

sauce = urllib.request.urlopen('https://www.instagram.com/tlgkyck').read()
soup = bs.BeautifulSoup(sauce,'lxml')

titledata=soup.title
titletext=titledata.text

try: #kay�tl� data varsa �ek
    kitap = openpyxl.load_workbook('insta.xlsx')
    sayfa = kitap.worksheets[0]

except IOError as e: #kay�tl� data yoksa olu�tur
    kitap = Workbook()
    sayfa = kitap.active
    kitap.save("insta.xlsx")

A1_verisi = sayfa['A1'].value #ba�lang�� verisi
Z1_verisi = sayfa['Z1'].value #son veri yede�i

text1_lines=titletext.splitlines()
text2_lines=Z1_verisi.splitlines()

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print('\n'.join(diff))

if (A1_verisi == None or Z1_verisi == None): #s�tunlar bo�sa ba�lang�� verilerini ekle
    sayfa['A1'] = sayfa['Z1'] = str(titletext)
    sayfa['K1'] = datetime.datetime.now()
    print("Profil ismi i�lenmi�tir:")
    print(titletext)

else:
    if (Z1_verisi == titletext):
        print('De�i�iklik yoktur')
    else:
        sayfa.append({'A': titletext, 'K': datetime.datetime.now()})

    sayfa['Z1'] = str(titletext)
    print(str(titletext))

kitap.save("insta.xlsx")
kitap.close()

#####################################################################################

# Hesap bilgilerimiz
kullan�c� = "usertolga@gmail.com"
kullan�c�_sifresi = 'gmailsifresi'

al�c� = 'tolga_k94@hotmail.com'  # al�c�n�n mail adresi
konu = 'Selam'
msj = str("G�ncel title verisi %s" %(titletext.encode('utf-8'))).encode('utf-8')

# bilgileri bir metinde derledik
email_text = """
From: {}
To: {}
Subject: {}
{}
""".format(kullan�c�, al�c�, konu, msj)

try:
    server = smtplib.SMTP('smtp.gmail.com:587')  # servere ba�lanmak i�in gerekli host ve portu belirttik

    server.starttls()  # serveri TLS(b�t�n ba�lant� �ifreli olucak bilgiler korunucak) ba�lant�s� ile ba�latt�k

    server.login(kullan�c�, kullan�c�_sifresi)  # Gmail SMTP server'�na giri� yapt�k

    server.sendmail(kullan�c�, al�c�, email_text)  # Mail'imizi g�nderdik

    server.close()  # SMTP serverimizi kapatt�k

    print('email g�nderildi')

except:
    print("bir hata olu�tu")