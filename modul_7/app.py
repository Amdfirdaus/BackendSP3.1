from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# koneksi ke MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stok"]
collection = db["barang"]

@app.route("/")
def index():
    data = collection.find()
    return render_template("index.html", barang=data)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        harga = request.form["harga"]
        jumlah = request.form["jumlah"]

        collection.insert_one({
            "kode": kode,
            "nama": nama,
            "harga": harga,
            "jumlah": jumlah
        })

        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/edit/<kode>", methods=["GET", "POST"])
def edit(kode):
    item = collection.find_one({"kode": kode})

    if request.method == "POST":
        nama = request.form["nama"]
        harga = request.form["harga"]
        jumlah = request.form["jumlah"]

        collection.update_one(
            {"kode": kode},
            {"$set": {
                "nama": nama,
                "harga": harga,
                "jumlah": jumlah
            }}
        )

        return redirect(url_for("index"))

    return render_template("edit.html", barang=item)

@app.route("/delete/<kode>")
def delete(kode):
    collection.delete_one({"kode": kode})
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
