import json
import difflib

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

def ask_question(question):
    # Si la question est déjà connue
    if question in knowledge_base:
        return knowledge_base[question]

    # Sinon, chercher une question similaire
    closest_question = find_closest_match(question)
    if closest_question:
        print(f"Je ne connais pas exactement la réponse, mais cela ressemble à '{closest_question}'. La réponse connue est : {knowledge_base[closest_question]}")
        response = input("Est-ce que cette réponse est correcte (o/n) ? ")

        # Si la réponse est correcte, on l'associe à la nouvelle question
        if response.lower() == 'o':
            knowledge_base[question] = knowledge_base[closest_question]
            with open("knowledge_base.json", "w") as f:
                json.dump(knowledge_base, f)
            return f"J'ai appris que '{question}' signifie aussi : {knowledge_base[question]}"

    # Sinon, apprendre la réponse
    print("Je ne connais pas la réponse, peux-tu me dire ce que c'est ?")
    answer = input("Réponse : ")

    # Ajouter à la base de connaissances
    knowledge_base[question] = answer

    # Sauvegarder dans le fichier
    with open("knowledge_base.json", "w") as f:
        json.dump(knowledge_base, f)

    return f"D'accord, j'ai appris que {question} signifie : {answer}"

# Boucle d'interaction
while True:
    question = input("Pose-moi une question ou tape 'exit' pour quitter : ")
    if question.lower() == "exit":
        break
    print(ask_question(question))