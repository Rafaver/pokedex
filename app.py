from flask import Flask, render_template, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,mapped_column 


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokedex.sqlite"
db = SQLAlchemy(app)

class Pokedex(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String,nullable=False)


with app.app_context():
    db.create_all()


def get_pokemon_data(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        image_url = data['sprites']['front_default']
        return image_url
    else:
        return None
@app.route("/")
def home():
    return render_template('pokemon.html')

@app.route("/pokemon/<name>")
def search_pokemon(name):
    pokemon_data = get_pokemon_data(name.lower())
    if pokemon_data:
        return jsonify({'image': pokemon_data})
    else:
        return jsonify({'error': f'No se encontró ningún Pokémon con el nombre {name}'}), 404

@app.route("/detalle")
def detalle():
    return render_template('detalle.html')



@app.route("/insert")
def insert():
    new_pokemon = 'snorlax'
    if new_pokemon:
        obj = Pokedex(name=new_pokemon)
        db.session.add(obj)
        db.session.commit()
    return 'pokemon agregado'

@app.route("/select")
def select():
   lista_pokemon=Pokedex.query.all()
   
   return lista_pokemon


if __name__ == '__main__':
    app.run(debug=True)
