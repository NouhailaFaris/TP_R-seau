from flask import Flask, jsonify, request, render_template, abort
import json

app = Flask(__name__)

# Bienvenue
welcome = "Welcome to 3ESE API!"

# Route de base
@app.route('/')
def hello_world():
    return 'Hello, World!\n'

# Route API pour afficher le message de bienvenue
@app.route('/api/welcome/', methods=['GET'])
def api_welcome():
    return jsonify({"message": welcome})

# Route API pour accéder à un caractère spécifique du message
@app.route('/api/welcome/<int:index>', methods=['GET'])
def api_welcome_index(index):
    try:
        return jsonify({"index": index, "val": welcome[index]})
    except IndexError:
        # Retourne une page 404 si l'index est incorrect
        abort(404)

# Gestion des erreurs 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# API pour tester les différentes méthodes HTTP (GET, POST)
@app.route('/api/request/', methods=['GET', 'POST'])
@app.route('/api/request/<path:path>', methods=['GET', 'POST'])
def api_request(path=None):
    # Réponse initiale avec des détails sur la requête
    resp = {
        "method": request.method,
        "url": request.url,
        "path": path,
        "args": request.args,  # Arguments de la requête GET
        "headers": dict(request.headers),  # Entêtes de la requête
    }
    
    # Si la méthode est POST, ajouter les données reçues dans la réponse
    if request.method == 'POST':
        resp["POST"] = {
            "data": request.get_json(),  # Données JSON envoyées dans le corps
        }
    return jsonify(resp)

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
