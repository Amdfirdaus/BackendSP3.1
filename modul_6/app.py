from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'tokobangunan123'

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'firdaus'
app.config['MYSQL_DB'] = 'toko_bangunan'

# Folder upload & format file gambar
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

mysql = MySQL(app)

# Pastikan folder uploads ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Cek ekstensi file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ==================== ROUTE CRUD ====================

# Halaman utama: tampilkan data barang (dengan search + pagination)
@app.route('/')
def index():
    cur = mysql.connection.cursor()

    # ambil parameter dari URL
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    # ambil data sesuai pencarian
    if search_query:
        cur.execute("""
            SELECT * FROM barang
            WHERE nama_barang LIKE %s OR kode_barang LIKE %s
            LIMIT %s OFFSET %s
        """, (f"%{search_query}%", f"%{search_query}%", per_page, offset))
    else:
        cur.execute("SELECT * FROM barang LIMIT %s OFFSET %s", (per_page, offset))
    data = cur.fetchall()

    # hitung total data untuk pagination
    if search_query:
        cur.execute("""
            SELECT COUNT(*) FROM barang
            WHERE nama_barang LIKE %s OR kode_barang LIKE %s
        """, (f"%{search_query}%", f"%{search_query}%"))
    else:
        cur.execute("SELECT COUNT(*) FROM barang")
    total_data = cur.fetchone()[0]
    total_pages = (total_data + per_page - 1) // per_page

    cur.close()

    return render_template(
        'index.html',
        barang=data,
        search_query=search_query,
        page=page,
        total_pages=total_pages
    )


# Route menampilkan gambar
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Tambah barang
@app.route('/add', methods=['GET', 'POST'])
def add_barang():
    if request.method == 'POST':
        kode = request.form['kode_barang']
        nama = request.form['nama_barang']
        satuan = request.form['satuan']
        stok = request.form['stok']
        harga = request.form['harga']
        file = request.files['gambar']

        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO barang (kode_barang, nama_barang, satuan, stok, harga, gambar) VALUES (%s, %s, %s, %s, %s, %s)",
                    (kode, nama, satuan, stok, harga, filename))
        mysql.connection.commit()
        cur.close()
        flash('Barang berhasil ditambahkan!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html')

# Edit barang
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_barang(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM barang WHERE id = %s", (id,))
    data = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        kode = request.form['kode_barang']
        nama = request.form['nama_barang']
        satuan = request.form['satuan']
        stok = request.form['stok']
        harga = request.form['harga']
        file = request.files['gambar']

        # Jika upload gambar baru, hapus lama
        filename = data[6]
        if file and allowed_file(file.filename):
            if filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE barang
            SET kode_barang=%s, nama_barang=%s, satuan=%s, stok=%s, harga=%s, gambar=%s
            WHERE id=%s
        """, (kode, nama, satuan, stok, harga, filename, id))
        mysql.connection.commit()
        cur.close()
        flash('Barang berhasil diperbarui!', 'info')
        return redirect(url_for('index'))

    return render_template('edit.html', barang=data)

# Hapus barang
@app.route('/delete/<int:id>')
def delete_barang(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT gambar FROM barang WHERE id = %s", (id,))
    gambar = cur.fetchone()
    if gambar and gambar[0]:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], gambar[0])
        if os.path.exists(file_path):
            os.remove(file_path)

    cur.execute("DELETE FROM barang WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Barang berhasil dihapus!', 'danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
