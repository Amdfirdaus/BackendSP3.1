from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret123'

# Konfigurasi database MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'       
app.config['MYSQL_PASSWORD'] = 'firdaus'
app.config['MYSQL_DB'] = 'UMKM'
app.config['UPLOAD_FOLDER'] = 'uploads' # Folder tempat menyimpan file upload
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Format file yang diizinkan

mysql = MySQL(app)

# Pastikan folder uploads ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# Fungsi untuk memeriksa ekstensi file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Halaman utama untuk menampilkan data
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stok")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', files=data)

# Menampilkan gambar dari folder uploads
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

# Halaman untuk menambah data
@app.route('/add', methods=['GET', 'POST'])
def add_file():
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO stok (kode, nama, harga, filename) VALUES (%s, %s, %s, %s)", 
                        (kode, nama, harga, filename))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('index'))

    return render_template('add.html')


# Halaman untuk menghapus data
@app.route('/delete/<id>', methods=['GET'])
def delete_file(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT filename FROM stok WHERE kode = %s", (id,))
    file_data = cur.fetchone()

    if file_data:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_data[0]))  # Hapus file dari folder

    cur.execute("DELETE FROM stok WHERE kode = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

# Halaman untuk mengedit data
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_file(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stok WHERE kode = %s", (id,))
    file_data = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        # Hapus gambar lama
        if file_data and file_data[3]:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_data[3]))  # Hapus file lama dari folder

        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        new_file = request.files['file']

        # Ganti gambar baru
        if new_file and allowed_file(new_file.filename):
            filename = secure_filename(new_file.filename)
            new_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE stok SET kode=%s, nama=%s, harga=%s, filename=%s WHERE kode=%s",
                        (kode, nama, harga, filename, id))
        else:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE stok SET kode=%s, nama=%s, harga=%s WHERE kode=%s",
                        (kode, nama, harga, id))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('edit.html', file=file_data)


if __name__ == '__main__':
    app.run(debug=True)