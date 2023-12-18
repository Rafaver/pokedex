from flask import Flask, render_template, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokedex.sqlite"
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

def get_pokemon_data(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        image_url = data['sprites']['front_default']
        height = data['height']
        weight = data['weight']
        order = data['order']
        types = ', '.join([t['type']['name'] for t in data['types']])

        # Nuevas estadísticas adicionales
        stats = {
            'HP': data['stats'][5]['base_stat'],  # 'hp' está representado como 'HP' en la API
            'ataque': data['stats'][4]['base_stat'],
            'defensa': data['stats'][3]['base_stat'],
            'velocidad': data['stats'][0]['base_stat']
            # Agrega más estadísticas si es necesario
        }

        # Peso que come (un ejemplo de dato personalizado)
        peso_comida = 50  # Esto debe ser ajustado a la información real del Pokémon

        return {
            'image': image_url,
            'name': pokemon.capitalize(),
            'height': height,
            'weight': weight,
            'order': order,
            'type': types,
            'stats': stats,
            'peso_comida': peso_comida
        }
    else:
        return None

@app.route("/")
def home():
    return render_template('pokemon.html')

@app.route("/pokemon/<name>")
def search_pokemon(name):
    data = get_pokemon_data(name.lower())
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': f'No se encontró ningún Pokémon con el nombre {name}'}), 404

@app.route("/insert")
def insert():
    pokemon_name = request.args.get('name')
    if pokemon_name:
        image_url, height, weight, order, types = get_pokemon_data(pokemon_name)
        if image_url:
            obj = Pokemon(name=pokemon_name, height=height, weight=weight, order=order, type=types)
            db.session.add(obj)
            db.session.commit()
            return 'Pokemon agregado'
        else:
            return 'No se encontró el Pokemon en la API'
    else:
        return 'No se proporcionó el nombre del Pokemon'

@app.route("/detalle/<pokemon_name>")
def detalle(pokemon_name):
    data = get_pokemon_data(pokemon_name.lower())
    if data:
        return render_template('detalle.html', pokemon=data)
    else:
        return jsonify({'error': f'No se encontró ningún Pokémon con el nombre {pokemon_name}'}), 404

@app.route("/select")
def select():
    lista_pokemon = Pokemon.query.all()
    return jsonify([pokemon.name for pokemon in lista_pokemon])

if __name__ == '__main__':
    app.run(debug=True)
