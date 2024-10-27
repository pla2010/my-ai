from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import os
import difflib

app = Flask(__name__)
app.secret_key = "secret_key_admin_access"  # Change la clé secrète

DATA_FILE = "data.json"

# Initialiser le fichier JSON s'il n'existe pas
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)
def find_similar_question(question, data):
    # Liste des questions existantes
    questions = list(data.keys())
    # Cherche les questions proches (seuil de similarité 0.8)
    similar = get_close_matches(question, questions, n=1, cutoff=0.8)
    return similar[0] if similar else None
    
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/handle_question", methods=["POST"])
def handle_question():
    data = load_data()
    question = request.json.get("question").strip().lower()
    
    # Vérifier si la question exacte existe
    if question in data:
        response = data[question]
        return jsonify({"response": response, "status": "known"})
    
    # Sinon, vérifier une question proche
    for stored_question in data.keys():
        if stored_question in question or question in stored_question:
            response = data[stored_question]
            return jsonify({"response": response, "status": "similar", "suggested_question": stored_question})

    # Si pas de réponse connue
    return jsonify({"response": "unknown"})

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = load_data()
    question = request.json.get("question").strip().lower()
    answer = request.json.get("answer").strip()

    # Ajouter ou mettre à jour la réponse
    data[question] = answer
    save_data(data)
    return jsonify({"status": "success"})

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "123456":  # Change le mot de passe ici
            session["admin_logged_in"] = True
            return redirect(url_for("admin_panel"))
        return "Mot de passe incorrect", 403
    return render_template("admin.html")

@app.route("/admin/panel")
def admin_panel():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))
    data = load_data()
    return render_template("admin_panel.html", data=data)

@app.route("/admin/delete_question", methods=["POST"])
def delete_question():
    if not session.get("admin_logged_in"):
        return jsonify({"status": "unauthorized"}), 403

    question = request.json.get("question").strip().lower()
    data = load_data()
    if question in data:
        del data[question]
        save_data(data)
        return jsonify({"status": "deleted"})
    return jsonify({"status": "not_found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
