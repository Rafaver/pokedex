from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('pokemon.html')

@app.route("/detalle")
def detalle():
    return render_template('detalle.html')


if __name__ == '__main__':
    app.run(debug=True)
