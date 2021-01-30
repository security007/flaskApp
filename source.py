#!/usr/bin/python3
from markupsafe import escape # fileter tag to prevent xss
class Sumber:
    def __init__(self):
        self.main =  escape("""
        #!/usr/bin/python3
        import chall
        import re
        from flask import Flask,render_template,url_for,request,session,redirect
        from markupsafe import escape
        from source import Sumber
        import string
        import random
        import hashlib
        app = Flask(__name__)
        letters = string.ascii_lowercase
        secret = ''.join(random.choice(letters) for i in range(10))
        app.secret_key = hashlib.sha1(secret.encode()).hexdigest()

        fitur = chall.Fitur()
        @app.route('/',methods=['GET', 'POST'])
        def index():
            try:
                sess = session['username']
                return render_template('index.html')
            except:
                return redirect(url_for('login'))

        @app.route('/prime',methods=['GET', 'POST'])
        def fiturPrime():
            try:
                sess = session['username']
                if request.method == 'POST':
                    range = request.form['range']
                    try:
                        res = fitur.prime(int(range))
                        return render_template('prime.html',result=res)
                    except:
                        return "Ilegal Character : range must be integer not string<br><a href='/prime'>back</a>"
                elif request.method == 'GET':
                    return render_template('prime.html')
            except:
                return redirect(url_for('login'))

        @app.route('/oddeven',methods=['GET', 'POST'])
        def fiturOddeven():
            try:
                sess = session['username']
                if request.method == 'POST':
                    range1 = request.form['range1']
                    range2 = request.form['range2']
                    try:
                        res = fitur.ganjilgenap(range1,range2)
                        return render_template('oddeven.html',result=res)
                    except Exception as e:
                        return "Ilegal Character : range must be integer not string<br><a href='/oddeven'>back</a>"
                elif request.method == 'GET':
                    return render_template('oddeven.html')
            except:
                return redirect(url_for('login'))

        @app.route('/findword',methods=['GET', 'POST'])
        def fiturFindword():
            try:
                sess = session['username']
                if request.method == 'POST':
                    word = request.form['word']
                    data = request.form['data']
                    try:
                        res = fitur.carikata(escape(data),word)# filter all tag to prevent xss
                        if len(res) != 0:
                            return render_template('findword.html',result=res)
                        else:
                            res = [word+' not found']
                            return render_template('findword.html',result=res)
                    except Exception as e:
                        return str(e)
                elif request.method == 'GET':
                    return render_template('findword.html')
            except:
                return redirect(url_for('login'))
        @app.route('/olshop',methods=['GET', 'POST'])
        def fiturMath1():
            if request.method == 'POST':
                nama = request.form['nama']
                harga = request.form['harga']
                diskon = request.form['diskon']
                jumlah = request.form['jumlah']
                try:
                    res = fitur.hitungdiskon(nama,int(harga),int(diskon),int(jumlah))
                    return render_template('olshop.html',result=res)
                except Exception as e:
                    return str(e)
            elif request.method == 'GET':
                return render_template('olshop.html')

        @app.route('/payment',methods=['GET', 'POST'])
        def fiturMath2():
            if request.method == 'POST':
                nama = request.form['nama']
                gajikaryawan = request.form['gajikaryawan']
                masuk = request.form['masuk']
                lembur = request.form['lembur']
                bonus = request.form['bonus']
                ijin = request.form['ijin']
                try:
                    res = fitur.gaji(nama,int(gajikaryawan),int(masuk),int(lembur),int(bonus),int(ijin))
                    return render_template('payment.html',result=res)
                except Exception as e:
                    return str(e)
            elif request.method == 'GET':
                return render_template('payment.html')

        @app.route('/countcharacter',methods=['GET', 'POST'])
        def countChar():
            if request.method == 'POST':
                in1 = request.form['char'] # input 1
                in2 = request.form['text'] # input 2
                res = fitur.count(in1,in2)
                return render_template('countchar.html',result=res)
            elif request.method == 'GET':
                return render_template('countchar.html')

        sql = chall.Crud('localhost','root','','hashmicro_test')
        @app.route('/crud',methods=['GET', 'POST'])
        def crud():
            res = sql.lihatData('perpus')
            return render_template("crud.html",result=res)

        @app.route('/crud/add',methods=['GET', 'POST'])
        def crudAdd():
            if request.method == 'POST':
                namaPengunjung = request.form['namaPengunjung']
                namaBuku = request.form['namaBuku']
                jenisBuku = request.form['jenisBuku']
                tanggalPinjam = request.form['tanggalPinjam']
                tanggalKembali = request.form['tanggalKembali']
                hargaSewa = request.form['hargaSewa']
                query = sql.addData(namaPengunjung,namaBuku,jenisBuku,tanggalPinjam,tanggalKembali,hargaSewa)
                if query == None:
                    return render_template('tambah.html',result="<font color=#00ff00 >Berhasil Tambah Data</font><a href='/crud'> Back To Home</a>")
                else:
                    return render_template('tambah.html',result="<font color=red >Gagal Tambah Data</font><a href='/crud'> Back To Home</a>")
            elif request.method == 'GET':
                return render_template('tambah.html')

        @app.route('/crud/edit/<id>',methods=['GET', 'POST'])
        def crudedit(id):
            if request.method == 'POST':
                id = id
                namaPengunjung = request.form['namaPengunjung']
                namaBuku = request.form['namaBuku']
                jenisBuku = request.form['jenisBuku']
                tanggalPinjam = request.form['tanggalPinjam']
                tanggalKembali = request.form['tanggalKembali']
                hargaSewa = request.form['hargaSewa']
                query = sql.updateData(id,namaPengunjung,namaBuku,jenisBuku,tanggalPinjam,tanggalKembali,hargaSewa)
                if query == None:
                    return render_template('edit.html',result="<font color=#00ff00 >Berhasil Edit Data</font><a href='/crud'> Back To Home</a>")
                else:
                    return render_template('edit.html',result="<font color=red >Gagal Edit Data</font><a href='/crud'> Back To Home</a>")
            elif request.method == 'GET':
                res = sql.lihatData('perpus WHERE id='+id)
                return render_template('edit.html',result=res)

        @app.route('/crud/delete/<id>',methods=['GET', 'POST'])
        def cruddelete(id):
            query = sql.deleteData(id)
            if query == None:
                return "<h3>Redirecting...</h3><script>alert('Berhasil Delete Data')</script><meta http-equiv=\"refresh\" content=\"2; URL=/crud\" />"
            else:
                return "<h3>Redirecting...</h3><script>alert('Gagal Delete Data')</script><meta http-equiv=\"refresh\" content=\"2; URL=/crud\" />"

        @app.route('/source',methods=['GET', 'POST'])
        def source():
            src = Sumber()
            return "<h2>Main Code :</h2><br><pre>"+str(src.main)+"</pre><br><hr><h2>Function,Object,Class,Fitur Code :</h2><br><pre>"+str(src.chall)+"</pre>"

        @app.route('/login', methods = ['GET', 'POST'])
        def login():
            if request.method == 'POST':
                if request.form['username'] == "security007" and request.form['password'] == "security007":
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
            elif request.method == 'GET':
                return render_template('login.html',result="<font color=red>Wrong Username/Password</font>")

        @app.route('/logout')
        def logout():
           # remove the username from the session if it is there
           session.pop('username', None)
           return redirect(url_for('login'))
        if __name__ == '__main__':
            app.run(debug=True)
""")
        self.chall = escape("""
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

        """)
