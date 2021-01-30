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
    try:
        sess = session['username']
        src = Sumber()
        return "<h2>Main Code :</h2><br><pre>"+str(src.main)+"</pre><br><hr><h2>Function,Object,Class,Fitur Code :</h2><br><pre>"+str(src.chall)+"</pre>"
    except:
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    try:
        sess = session['username']
        return redirect(url_for('index'))
    except:
        pass
    if request.method == 'POST':
        if request.form['username'] == "security007" and request.form['password'] == "security007":
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_template('login.html',result="<font color=red>Wrong Username/Password</font>")

    elif request.method == 'GET':
        return render_template('login.html',result="<font color=red>Wrong Username/Password</font>")

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)
