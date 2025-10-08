from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        umur = request.form['umur']
        agama = request.form['agama']
        
        return f"""
        <div style='font-family:sans-serif; margin:50px;'>
            <h2>Data Berhasil Diterima </h2>
            <p><b>Nama:</b> {nama}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Umur:</b> {umur} tahun</p>
            <p><b>Agama:</b> {agama} </p>
            <a href='/form'>Kembali ke Form</a>
        </div>
        """
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
