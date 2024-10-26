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
    try:
        # Récupérer la question de la requête JSON
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Aucune question fournie"}), 400

        question = data['question']
        
        # Vérifier si la question est dans la base de connaissances
        answer = knowledge_base.get(question, "Désolé, je ne connais pas la réponse.")

        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
