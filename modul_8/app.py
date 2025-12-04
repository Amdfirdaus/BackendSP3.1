from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename
import os

# ---------------------------------------------------
# KONFIGURASI FLASK
# ---------------------------------------------------
app = Flask(__name__)
CORS(app)

# folder upload gambar
app.config["UPLOAD_FOLDER"] = "static/images"
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# ---------------------------------------------------
# KONEKSI MONGODB
# ---------------------------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["stok"]
barang_col = db["barang"]


# ===================================================
# ROUTE 1 : HALAMAN INDEX (TAMPILKAN SEMUA BARANG)
# ===================================================
@app.route("/")
def index():
    data = barang_col.find()
    return render_template("index.html", data=data)


# ===================================================
# ROUTE 2 : HALAMAN TAMBAH BARANG
# ===================================================
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        harga = int(request.form["harga"])
        jumlah = int(request.form["jumlah"])

        gambar_file = request.files.get("gambar")
        filename = None

        # upload gambar
        if gambar_file and gambar_file.filename:
            filename = secure_filename(gambar_file.filename)
            gambar_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        barang_col.insert_one({
            "kode": kode,
            "nama": nama,
            "harga": harga,
            "jumlah": jumlah,
            "gambar": filename
        })

        return redirect("/")

    return render_template("add.html")


# ===================================================
# ROUTE 3 : HALAMAN EDIT BARANG
# ===================================================
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    data = barang_col.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        nama = request.form["nama"]
        harga = int(request.form["harga"])
        jumlah = int(request.form["jumlah"])

        gambar_file = request.files.get("gambar")
        update_data = {
            "nama": nama,
            "harga": harga,
            "jumlah": jumlah
        }

        # cek jika ganti gambar
        if gambar_file and gambar_file.filename:
            filename = secure_filename(gambar_file.filename)
            gambar_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            update_data["gambar"] = filename

        barang_col.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        return redirect("/")

    return render_template("edit.html", data=data)


# ===================================================
# ROUTE 4 : HAPUS BARANG
# ===================================================
@app.route("/delete/<id>")
def delete(id):
    barang_col.delete_one({"_id": ObjectId(id)})
    return redirect("/")


# ===================================================
# JALANKAN SERVER
# ===================================================
if __name__ == "__main__":
    app.run(debug=True)
