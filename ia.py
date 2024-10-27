from flask import Flask, request, jsonify, redirect, url_for, render_template
import json
from difflib import get_close_matches
import os

ia = Flask(__name__)
ia.secret_key = "votre_cle_secrete_pour_session"  # Change cette clé pour plus de sécurité
DATA_FILE = 'data.json'

# Charger les questions-réponses depuis le fichier JSON
def load_questions():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Sauvegarder les questions-réponses dans le fichier JSON
def save_questions(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Cherche une question similaire dans les données existantes
def find_similar_question(question, data):
    questions = list(data.keys())
    similar = get_close_matches(question, questions, n=1, cutoff=0.8)
    return similar[0] if similar else None

# Route principale pour recevoir les questions du client
@ia.route('/handle_question', methods=['POST'])
def handle_question():
    data = load_questions()
    question = request.json.get('question')
    if not question:
        return jsonify({'response': 'Question non valide.'}), 400

    # Vérifie si la question est déjà connue
    if question in data:
        return jsonify({'response': data[question], 'is_known': True})
    else:
        # Cherche une question similaire
        similar_question = find_similar_question(question, data)
        if similar_question:
            return jsonify({'response': data[similar_question], 'is_known': False, 'similar_question': similar_question})
        else:
            return jsonify({'response': 'réponse inconnue', 'is_known': False})

# Route pour apprendre une nouvelle réponse ou mettre à jour une question existante
@ia.route('/learn', methods=['POST'])
def learn():
    data = load_questions()
    question = request.json.get('question')
    response = request.json.get('response')
    
    if not question or not response:
        return jsonify({'status': 'Erreur: question ou réponse manquante.'}), 400

    # Sauvegarde la réponse fournie pour la question
    data[question] = response
    save_questions(data)
    return jsonify({'status': 'Apprentissage réussi!'})

# Tableau de bord d'administration sans authentification
@ia.route('/admin_dashboard')
def admin_dashboard():
    data = load_questions()
    return jsonify(data)  # Renvoyer en JSON pour la requête GET

# Route pour supprimer une question-réponse depuis le tableau de bord d'administration
@ia.route('/delete_question', methods=['POST'])
def delete_question():
    question = request.json.get('question')
    if not question:
        return jsonify({'status': 'Question manquante'}), 400

    data = load_questions()
    if question in data:
        del data[question]
        save_questions(data)
        return jsonify({'status': 'Question supprimée'})
    else:
        return jsonify({'status': 'Question non trouvée'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Définit le port
    ia.run(host='0.0.0.0', port=port)  # Écoute sur 0.0.0.0
