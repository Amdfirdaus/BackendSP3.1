from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "12345"

# Konfigurasi koneksi ke database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'firdaus'
app.config['MYSQL_DB'] = 'crud_db'

mysql = MySQL(app)

# Halaman utama (tampilkan semua data)
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stok")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', stok=data)

# Halaman tambah data (form)
@app.route('/tambah')
def tambah():
    return render_template('add.html')

# Proses tambah data ke database
@app.route('/add', methods=['POST'])
def add():
    nama = request.form['nama_barang']
    jumlah = request.form['jumlah']
    harga = request.form['harga']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO stok (nama_barang, jumlah, harga) VALUES (%s, %s, %s)", (nama, jumlah, harga))
    mysql.connection.commit()
    flash("Data berhasil ditambahkan!")
    return redirect(url_for('index'))

# Halaman edit data
@app.route('/edit/<id>')
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stok WHERE id=%s", (id,))
    data = cur.fetchone()
    cur.close()
    return render_template('edit.html', data=data)

# Proses update data
@app.route('/update', methods=['POST'])
def update():
    id_data = request.form['id']
    nama = request.form['nama_barang']
    jumlah = request.form['jumlah']
    harga = request.form['harga']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE stok SET nama_barang=%s, jumlah=%s, harga=%s WHERE id=%s", (nama, jumlah, harga, id_data))
    mysql.connection.commit()
    flash("Data berhasil diperbarui!")
    return redirect(url_for('index'))

# Hapus data
@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM stok WHERE id=%s", (id,))
    mysql.connection.commit()
    flash("Data berhasil dihapus!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
