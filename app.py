from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Función para obtener los datos del Pokémon
def get_pokemon_data(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        image_url = data['sprites']['front_default']
        return image_url
    else:
        return None

# Página de inicio con el formulario para buscar Pokémon
@app.route("/")
def home():
    return render_template('pokemon.html')

# Endpoint para buscar el Pokémon por nombre
@app.route("/pokemon/<name>")
def search_pokemon(name):
    pokemon_data = get_pokemon_data(name.lower())
    if pokemon_data:
        return jsonify({'image': pokemon_data})
    else:
        return jsonify({'error': f'No se encontró ningún Pokémon con el nombre {name}'}), 404

# Página de detalles del Pokémon (aún por implementar)
@app.route("/detalle")
def detalle():
    # Aquí puedes renderizar la plantilla para mostrar los detalles del Pokémon
    return render_template('detalle.html')

if __name__ == '__main__':
    app.run(debug=True)
