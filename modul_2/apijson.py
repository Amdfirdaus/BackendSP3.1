from flask import Flask

app = Flask(__name__)

@app.route("/")
def home ():
    return"Hallo Selamat Datang di Aplikasi"

@app.route("/about")
def about():
    return "Ini adalah halaman About"


if __name__ == "__main__":
    app.run(debug=True)