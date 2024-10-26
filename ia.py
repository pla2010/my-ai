import json
import difflib
from flask import Flask, request, jsonify

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
def ask_question():
    question = request.json.get('question', '')

    # Si la question est déjà connue
    if question in knowledge_base:
        return jsonify({"answer": knowledge_base[question]})

    # Sinon, chercher une question similaire
    closest_question = find_closest_match(question)
    if closest_question:
        return jsonify({"message": f"Je ne connais pas exactement la réponse, mais cela ressemble à '{closest_question}'. La réponse connue est : {knowledge_base[closest_question]}",
                        "similar": True})

    # Sinon, apprendre la réponse
    return jsonify({"message": "Je ne connais pas la réponse, peux-tu me dire ce que c'est ?", "learn": True})

@app.route('/learn', methods=['POST'])
def learn_answer():
    data = request.json
    question = data.get('question', '')
    answer = data.get('answer', '')

    # Ajouter à la base de connaissances
    knowledge_base[question] = answer

    # Sauvegarder dans le fichier
    with open("knowledge_base.json", "w") as f:
        json.dump(knowledge_base, f)

    return jsonify({"message": f"D'accord, j'ai appris que '{question}' signifie : {answer}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
