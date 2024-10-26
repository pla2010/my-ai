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
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Aucune question fournie"}), 400

    # Si la question est déjà connue
    if question in knowledge_base:
        return jsonify({"answer": knowledge_base[question]})

    # Chercher une question similaire
    closest_question = find_closest_match(question)
    if closest_question:
        response = {
            "answer": knowledge_base[closest_question],
            "similar": True,
            "closest_question": closest_question
        }
        return jsonify(response)

    # Si aucune réponse trouvée, demande la réponse
    return jsonify({"error": "Je ne connais pas la réponse, peux-tu me dire ce que c'est ?"}), 404

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
    app.run(host='0.0.0.0', port=5000)
