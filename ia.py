from flask import Flask, request, jsonify
import json
import difflib

app = Flask(__name__)

# Charger la base de connaissances
try:
    with open("knowledge_base.json", "r") as f:
        knowledge_base = json.load(f)
except FileNotFoundError:
    knowledge_base = {}

def find_closest_match(question, threshold=0.5):
    """Trouve une question similaire dans la base de connaissances."""
    closest_match = difflib.get_close_matches(question, knowledge_base.keys(), n=1, cutoff=threshold)
    return closest_match[0] if closest_match else None

@app.route('/ask', methods=['POST'])
def handle_question(question):
    # Vérifie si la question est dans la base de connaissances
    if question in knowledge_base:
        return knowledge_base[question]
    else:
        return None  # Pas de réponse trouvée

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Aucune question fournie"}), 400

    question = data['question']
    answer = handle_question(question)

    if answer is not None:
        return jsonify({"answer": answer})
    else:
        # Si aucune réponse trouvée, demande à l'utilisateur
        return jsonify({"error": "Je ne connais pas la réponse. Quel est-elle ?"}), 404

@app.route('/add_answer', methods=['POST'])
def add_answer():
    data = request.get_json()
    if not data or 'question' not in data or 'answer' not in data:
        return jsonify({"error": "Question ou réponse non fournie"}), 400

    question = data['question']
    answer = data['answer']
    
    # Ajoute la question et la réponse à la base de connaissances
    knowledge_base[question] = answer
    
    return jsonify({"message": "Réponse ajoutée avec succès!"})


@app.route('/learn', methods=['POST'])
def learn():
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")

    if question and answer:
        knowledge_base[question] = answer
        with open("knowledge_base.json", "w") as f:
            json.dump(knowledge_base, f)
        return jsonify({"message": "J'ai appris la réponse !"}), 200
    return jsonify({"error": "Question ou réponse manquante."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
