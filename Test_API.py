from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Données initiales (message de bienvenue sous forme de liste pour modification)
welcome = list("Welcome to 3ESE API!")  # Converti en liste pour permettre la modification


@app.route('/api/welcome/<int:index>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_welcome_crud(index):
    # Vérifier si l'index est valide
    if index < 0 or index >= len(welcome):
        abort(404)

    # Méthode GET : Lire un caractère spécifique
    if request.method == 'GET':
        return jsonify({"index": index, "val": welcome[index]})

    # Méthode POST : Ajouter un caractère après l'index spécifié
    if request.method == 'POST':
        data = request.get_json()
        if not data or "val" not in data:
            abort(400)  # 400 Bad Request
        welcome.insert(index + 1, data["val"])
        return "", 202  # 202 Accepted (No Content)

    # Méthode PUT : Modifier un caractère à l'index spécifié
    if request.method == 'PUT':
        data = request.get_json()
        if not data or "val" not in data:
            abort(400)  # 400 Bad Request
        welcome[index] = data["val"]
        return "", 204  # 204 No Content (Success)

    # Méthode DELETE : Supprimer un caractère à l'index spécifié
    if request.method == 'DELETE':
        welcome.pop(index)
        return "", 204  # 204 No Content (Success)


# Route pour afficher tout le message actuel
@app.route('/api/welcome/', methods=['GET'])
def api_welcome_all():
    return jsonify({"message": "".join(welcome)})


# Gestion des erreurs 404
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Index not found"}), 404


# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
