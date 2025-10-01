from flask import Flask, request, jsonify

app = Flask(__name__)

# Data dummy
produk = [
    {"id": 1, "nama": "Snack A", "harga": 5000},
    {"id": 2, "nama": "Drink B", "harga": 8000}
]

@app.route("/produk", methods=["GET"])
def get_produk():
    return jsonify(produk)

@app.route("/produk", methods=["POST"])
def tambah_produk():
    data = request.get_json()
    produk.append(data)
    return jsonify({"message": "Produk berhasil ditambahkan", "data": data}), 201

if __name__ == "__main__":
    app.run(debug=True)
