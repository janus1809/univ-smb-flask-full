from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = 'JanusLePetit' # Clé secrète pour les sessions

@app.route('/login', methods=['GET'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Rechercher l'utilisateur dans la base de données identity
    user = Identity.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # Enregistrer l'utilisateur dans une session
        session['username'] = user.username
        session['nom'] = user.nom
        session['prenom'] = user.prenom
        session['anniv'] = user.anniv.strftime('%Y-%m-%d')
        return jsonify({'message': 'ok'})
    else:
        return jsonify({'error': 'Mauvais mdp'}), 401

@app.route('/identity')
def identity():
    # Vérifier que l'utilisateur est connecté en vérifiant s'il y a une session
    if not session.get('username'):
        return jsonify({'error': 'pas co'}), 401

    # Récupérer les informations de l'utilisateur depuis la session
    identity = {
        'username': session['username'],
        'nom': session['nom'],
        'prenom': session['prenom'],
        'anniv': session['anniv']
    }

    return jsonify(identity)

@app.route('/identity/<username>')
def get_identity(username):
    # Vérifier que l'utilisateur est connecté en vérifiant s'il y a une session
    if not session.get('username'):
        return jsonify({'error': 'Pas co'}), 401

    # Vérifier que l'utilisateur a les permissions pour accéder à cette ressource
    if session['username'] != username:
        return jsonify({'error': 'Pas autoriser'}), 403 #utile si ajout srv ou autre par un admin

    # Rechercher l'utilisateur dans la base de données identity
    user = Identity.query.filter_by(username=username).first()

    if user:
        # Retourner les informations de l'utilisateur
        identity = {
            'username': user.username,
            'nom': user.nom,
            'prenom': user.prenom,
            'anniv': user.anniv.strftime('%Y-%m-%d')
        }
        return jsonify(identity)
    else:
        return jsonify({'error': 'U'}), 404
