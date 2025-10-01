from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return"Selamat datang di toko Indah UMKM "

@app.route("/produk/snack")
def snack():
    return"halaman produk berisi snack "

@app.route("/produk/drink")
def drink():
    return"halaman produk berisi drink "

@app.route("/produk/snack/<int:id>")
def snack_id(id):
    return f"Halaman Produk Snack dengan id = {id}"

@app.route("/produk/drink/<int:id>")
def drink_id(id):
    return f"Halaman Produk Soft Drink dengan id = {id}"

if __name__ == "__main__":
    app.run(debug=True)
