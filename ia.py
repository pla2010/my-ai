from flask import Flask, request, jsonify, redirect, url_for, session, render_template
import json
from difflib import get_close_matches

app = Flask(__name__)
app.secret_key = "votre_cle_secrete_pour_session"  # Change cette clé pour plus de sécurité
DATA_FILE = 'questions.json'

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
@app.route('/handle_question', methods=['POST'])
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
@app.route('/learn', methods=['POST'])
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

# Page d'administration protégée par mot de passe
@app.route('/admin', methods=['GET', 'POST'])
def admin():
  #  if request.method == 'POST':
      #  password = request.form.get('password')
    #    if password == "votre_mot_de_passe_admin":  # Change le mot de passe
  #          session['admin'] = True
  #          return redirect(url_for('admin_dashboard'))
  #      else:
    #        return "Mot de passe incorrect", 403
    return render_template('admin_login.html')

# Tableau de bord d'administration
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))

    data = load_questions()
    return render_template('admin_dashboard.html', questions=data)

# Route pour supprimer une question-réponse depuis le tableau de bord d'administration
@app.route('/delete_question', methods=['POST'])
def delete_question():
    if not session.get('admin'):
        return jsonify({'status': 'Accès refusé'}), 403

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

# Déconnexion de l'administrateur
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
