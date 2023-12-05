from flask import Flask,render_templates

app = Flask(__name__)

@app.route("/")
def home():
    return render_templates('pokemon.html')

if __name__=='__main__':
    app.run(debug=True)