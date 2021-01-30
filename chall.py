#!/usr/bin/python3
import re
import random
import json
import mysql.connector
from markupsafe import Markup

# class fitur
class Fitur:
    def __init__(self):
        pass

    # ---------------------------Nested Loop-------------------------------
    # cari bilangan prima
    def prime(self,listnya):
        i = 2
        hasil = []
        while(i < int(listnya)):
            j = 2
            while(j <= (i/j)):
                if not(i%j):
                    break
                j += 1
            if (j > i/j) :
                    hasil.append(i)
            i += 1
        return hasil # list

    def ganjilgenap(self,num1,num2):
        ganjil = []
        genap = []
        for x in range(int(num1),int(num2)):
            if x % 2 == 0 :
                genap.append(x)
            elif x % 2 != 0 :
                ganjil.append(x)

        return ganjil,genap # list
    # ------------------------------Nested if----------------------------------
    # cari kata
    def carikata(self,data,kata):
        hasil = []
        if kata != " ":
            if re.search(kata,data) != None:
                hasilnya = data.replace(kata,Markup("<font color= #00ff00 ><b>"+kata+"</b></font>"))# grant only this tag to render
                hasil.append(hasilnya)
            else:
                pass

        else:
            hasil.append("Harap masukkan kata")
        return hasil

    # ------------------------------Mathematics-------------------------------------
    # diskon
    def hitungdiskon(self,nama,hargabarang,diskonbarang,jumlahbarang):
        nama = nama # nama barang
        harga = hargabarang # harga sebelum diskonbarang
        diskon = diskonbarang # diskon potongan
        jumlahbarang = jumlahbarang # jumlah barang yang dibeli
        jumlahpotongan = harga*jumlahbarang*diskon/100 # total potongan harga
        hargaakhir = harga*jumlahbarang-jumlahpotongan
        return {"nama":str(nama),"harga":str(harga),"diskon":str(diskon),"jumlahbarang":str(jumlahbarang),"jumlahpotongan":str(jumlahpotongan),"hargaakhir":str(hargaakhir)} # json

    # Gaji karyawan
    def gaji(self,nama,gajikaryawan,masuk,lembur,bonus,ijin):
        karyawan = nama
        totalgaji = gajikaryawan
        gajiperhari = int(totalgaji/30)
        total_ijin= ijin
        totalmasuk = masuk-ijin
        gajipotongan = gajiperhari*totalmasuk
        if ijin == 0 :
            potongan = 0
        else:
            potongan = totalgaji-gajipotongan
        bonus = lembur*bonus
        gajibulanini = totalgaji+bonus-potongan
        # {'nama_karyawan': 'ucup', 'gaji_pokok': 4500000, 'gaji_perhari': 150000, 'potongan': 450000, 'bonus': 200000, 'gaji_bulan_ini': 4250000}
        return {'nama_karyawan':str(karyawan),'gaji_pokok':str(totalgaji),'gaji_perhari':str(gajiperhari),'potongan':str(potongan),'bonus':str(bonus),'gaji_bulan_ini':str(gajibulanini),'total_masuk':str(totalmasuk),'total_ijin':str(total_ijin)}
        # json

    # ----------------------Menghitung jumlah karakter-------------
    def count(self,in1,in2):
        karakter = ""
        for x in in1.lower():
            if x in in2.lower() and in2.count(x) == in1.count(x):
                karakter += x
            elif x in in2.lower() and x not in karakter:
                karakter += x
        karakter_ditemukan = len(karakter)/len(in1)*100
        persen = str("{:.2f}%").format(karakter_ditemukan)
        return str(persen)+" Ditemukan ("+str(len(karakter))+") huruf sama di kalimat"+" \""+in2.upper()+"\" ("+"".join(karakter).upper()+") pada karakter ("+str(in1.upper())+")"

class Crud:
    def __init__(self,host,user,password,mydb):
        self.conn = mysql.connector.connect(host=host,user=user,password=password,database=mydb)
        self.mycursor = self.conn.cursor(dictionary=True)

    def addData(self,namaPengunjung,namaBuku,jenisBuku,tanggalPinjam,tanggalKembali,hargaSewa):
        try:
            self.mycursor.execute("INSERT INTO perpus (id,namaPengunjung,namaBuku,jenisBuku,tanggalPinjam,tanggalKembali,hargaSewa) VALUES(NULL,%s,%s,%s,%s,%s,%s)",(namaPengunjung,namaBuku,jenisBuku,tanggalPinjam,tanggalKembali,hargaSewa))
            self.res = self.conn.commit() # None
        except Exception as e:
            self.res = "error"

        return self.res

    def lihatData(self,data):
        self.hasilData = []
        try:
            self.mycursor.execute("select * from "+data)
            self.result = self.mycursor.fetchall()
            for x in self.result:
                self.hasilData.append(x) # list
        except Exception as e:
            self.hasilData = "error"
        return self.hasilData

    def updateData(self,id,namaPengunjung,namaBuku,jenisBuku,tanggalPinjam,tanggalKembali,hargaSewa):
        try:
            self.mycursor.execute("UPDATE perpus SET namaPengunjung ='"+namaPengunjung+"',namaBuku ='"+namaBuku+"',jenisBuku ='"+jenisBuku+"',tanggalPinjam ='"+tanggalPinjam+"',tanggalKembali ='"+tanggalKembali+"',hargaSewa ='"+hargaSewa+"' WHERE id = "+id)
            self.res = self.conn.commit() # None
        except Exception as e:
            self.res = e

        return self.res

    def deleteData(self,id):
        try:
            self.mycursor.execute("DELETE from perpus WHERE id = "+id)
            self.res = self.conn.commit() # None
        except Exception as e:
            self.res = e

        return self.res
#sql = Crud('localhost','root','','hashmicro_test')
