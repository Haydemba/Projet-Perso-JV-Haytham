import pandas as pd

import random

df = pd.read_csv("Persos.csv", sep=";")

print(df.head())
print(df.columns.tolist()) 

colonnes_questions = [
    "Genre", "Franchise", "Première Apparition", "Jouable",
    "Espèce", "Console", "Morale", "Mascotte\xa0?"
]


colonnes_questions = sorted(colonnes_questions, key=lambda col: df[col].nunique(), reverse=True)

print(df.columns.tolist())


print("Voici les colonnes triées :", colonnes_questions)

#Je cherche le personnage secret
personnage_secret = df.sample(1).iloc[0]

print("Un personnage secret a été choisi !")

#Je fais la liste des candidats
candidats = df.copy()

print(f"Nombre initial de candidats : {len(candidats)}")

#Je vais sélectionner la question dans la colonne
colonne = colonnes_questions[0]

valeurs_possibles = df[colonne].unique()

print(f"Question : quelle est la valeur pour la colonne '{colonne}' ?")

print("Valeurs possibles :", valeurs_possibles)

colonne = colonnes_questions[0]

valeurs_possibles = df[colonne].unique()

print(f"Question : quelle est la valeur pour la colonne '{colonne}' ?")

print("Valeurs possibles :", valeurs_possibles)


#Je récupère la réponse
valeur_utilisateur = input("Votre réponse : ")

candidats = candidats[candidats[colonne] == valeur_utilisateur]

print(f"Nombre de candidats restants : {len(candidats)}")

print(candidats["Nom"].tolist())

for colonne in colonnes_questions:
    valeurs_possibles = candidats[colonne].unique()
    print(f"Question : quelle est la valeur pour la colonne '{colonne}' ?")
    print("Valeurs possibles :", valeurs_possibles)

    valeur_utilisateur = input("Votre réponse : ")

    if valeur_utilisateur not in valeurs_possibles:
        print("Réponse invalide. Essaie encore.")
        continue

    candidats = candidats[candidats[colonne] == valeur_utilisateur]
    print(f"Candidats restants : {len(candidats)}")

    if len(candidats) == 1:
        print(f"Le personnage auquel vous pensez est probablement : {candidats.iloc[0]['Nom']}")
        break
    elif len(candidats) == 0:
        print("Aucun personnage ne correspond à vos réponses. Réessayez avec d’autres critères.")
        break
else:
    print("Je n’ai pas pu deviner précisément. Voici les candidats restants :")
    print(candidats[['Nom', 'Franchise']])

import random

personnage_secret = df.sample(1).iloc[0]
candidats = df.copy()

colonnes_questions = ["Genre", "Franchise", "Première Apparition", "Jouable", "Espèce", "Console", "Morale", "Mascotte ?"]

print("J'ai choisi un personnage. Pose-moi des questions pour le deviner.")

for i in range(5):
    print(f"Question {i+1} sur 5")
    print("Tu peux poser une question sur :", ", ".join(colonnes_questions))
    question = input("Sur quelle caractéristique veux-tu poser une question ? ")

    if question not in colonnes_questions:
        print("Caractéristique non valide. Réessaie.")
        continue

    valeurs_possibles = candidats[question].dropna().unique()
    print("Valeurs possibles :", ", ".join(str(val) for val in valeurs_possibles))

    reponse = input(f"Quelle valeur penses-tu pour '{question}' ? ")
    vraie_valeur = personnage_secret[question]

    if str(reponse).strip().lower() == str(vraie_valeur).strip().lower():
        print("Bonne réponse !")
    else:
        print(f"Non, la bonne réponse était : {vraie_valeur}")

    candidats = candidats[candidats[question].astype(str).str.lower() == reponse.lower()]
    print(f"Candidats restants : {len(candidats)}")

    if len(candidats) == 1:
        break

if len(candidats) == 1:
    perso_final = candidats.iloc[0]
    print(f"Tu as trouvé ! C'était : {perso_final['Nom']} ({perso_final['Franchise']})")
elif len(candidats) == 0:
    print("Aucun personnage ne correspond à tes réponses.")
else:
    print("Voici les personnages restants :")
print(candidats[["Nom", "Franchise"]])
print("=== Mode IA : devinette automatique ===")
personnage_secret = df.sample(1).iloc[0]
candidats = df.copy()
questions_posees = []

while len(candidats) > 1 and colonnes_questions:
    colonne = max(colonnes_questions, key=lambda col: candidats[col].nunique())
    colonnes_questions.remove(colonne)
    questions_posees.append(colonne)
    valeur = personnage_secret[colonne]
    print(f"L'IA pose la question : '{colonne}' vaut-il '{valeur}' ?")
    candidats = candidats[candidats[colonne] == valeur]
    print(f"→ Candidats restants après filtrage : {len(candidats)}")

if len(candidats) == 1:
    print(f"L'IA a deviné ! Le personnage est : {candidats.iloc[0]['Nom']} ({candidats.iloc[0]['Franchise']})")
else:
    print("L'IA n'a pas pu deviner précisément. Personnages restants :")
    print(candidats[['Nom', 'Franchise']])
print("=== Dialogue IA : Oui/Non ===")
personnage_secret = df.sample(1).iloc[0]
candidats = df.copy()
colonnes_binaires = [col for col in colonnes_questions if df[col].nunique() == 2]

for colonne in colonnes_binaires:
    valeur = personnage_secret[colonne]
    question = f"{colonne} : {valeur} ?"
    print(f"IA : {question}")
    reponse = input("Humain (oui/non) : ").strip().lower()

    if reponse == "oui":
        candidats = candidats[candidats[colonne] == valeur]
    elif reponse == "non":
        candidats = candidats[candidats[colonne] != valeur]
    else:
        print("Réponse invalide. Réponds par 'oui' ou 'non'.")
        continue

    print(f"→ Candidats restants : {len(candidats)}")
    if len(candidats) == 1:
        break

if len(candidats) == 1:
    print(f"IA : Je crois que vous pensez à : {candidats.iloc[0]['Nom']} ({candidats.iloc[0]['Franchise']})")
else:
    print("IA : Je n'ai pas réussi à deviner précisément.")
    print("Personnages restants :")
    print(candidats[['Nom', 'Franchise']])