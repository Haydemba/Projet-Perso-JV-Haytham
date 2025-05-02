import pandas as pd
import random
import numpy as np
import os

# Chargement des données
df = pd.read_csv("Persos.csv", sep=";")

print("Aperçu des données :")
print(df.head())
print("Colonnes disponibles :", df.columns.tolist())

# Correction du nom des colonnes selon l'aperçu des données
colonnes_questions = [
    "Genre", "Franchise", "Première Apparition", "Jouable",
    "Espèce", "Console", "Morale", "Mascotte\xa0?"
]

# Nettoyage : convertir en chaîne pour éviter les erreurs
for col in colonnes_questions:
    df[col] = df[col].astype(str).str.strip()

# === Fonction pour calculer l'entropie avec numpy ===
def entropie(data, colonne):
    valeurs = data[colonne].value_counts(normalize=True)
    return -np.sum(valeurs * np.log2(valeurs))

# === Fonction récursive pour construire l'arbre ===
def construire_arbre(data, colonnes):
    if len(data["Nom"].unique()) == 1 or not colonnes:
        return {"feuille": data["Nom"].iloc[0]}

    entropies = [(col, entropie(data, col)) for col in colonnes if col in data.columns]
    meilleure_colonne = min(entropies, key=lambda x: x[1])[0]

    noeud = {"colonne": meilleure_colonne, "branches": {}}
    for valeur in data[meilleure_colonne].unique():
        sous_donnees = data[data[meilleure_colonne] == valeur]
        nouvelles_colonnes = [c for c in colonnes if c != meilleure_colonne]
        noeud["branches"][valeur] = construire_arbre(sous_donnees, nouvelles_colonnes)
    return noeud

# === Fonction pour dialoguer avec l'utilisateur selon l'arbre ===
def poser_questions(arbre):
    while True:
        if "feuille" in arbre:
            print(f"IA : Je pense que votre personnage est : {arbre['feuille']}")
            confirmation = input("Est-ce correct ? (oui/non) : ").strip().lower()
            if confirmation == "oui":
                print("IA : Super, j'ai trouvé !")
                return
            else:
                nouveau_nom = input("Quel était le personnage ? : ").strip()
                nouvelle_question = input("Propose une nouvelle question pour le différencier : ").strip()
                nouvelle_valeur = input(f"Quelle serait la réponse à cette question pour {nouveau_nom} ? : ").strip()

                # Enrichissement de la base
                ajouter_nouvelle_entree(nouveau_nom, arbre['feuille'], nouvelle_question, nouvelle_valeur)

                # Reconstruction dynamique de l'arbre après apprentissage
                global df
                arbre_maj = construire_arbre(df, colonnes_questions)
                print("Nouvel arbre mis à jour. Reprenons le jeu.")
                poser_questions(arbre_maj)
                return

        question = arbre["colonne"]
        options = list(arbre["branches"].keys())
        print(f"IA : Quelle est la valeur pour '{question}' ?")
        print("Valeurs possibles :", ", ".join(options))
        reponse = input("Votre réponse (choisissez une valeur ci-dessus) : ").strip()

        if reponse in arbre["branches"]:
            arbre = arbre["branches"][reponse]
        else:
            print("IA : Réponse invalide. Merci de choisir une des valeurs listées.")

# === Fonction pour enrichir dynamiquement la base ===
def ajouter_nouvelle_entree(nouveau_nom, ancien_nom, nouvelle_question, nouvelle_valeur):
    global df
    nouvelle_ligne = df[df["Nom"] == ancien_nom].iloc[0].copy()
    nouvelle_ligne["Nom"] = nouveau_nom
    nouvelle_ligne[nouvelle_question] = nouvelle_valeur

    df.loc[len(df)] = nouvelle_ligne

    # Sauvegarde dans un nouveau fichier 
    df.to_csv("Persos_enrichi.csv", sep=";", index=False)

# === Construction et utilisation de l'arbre de décision ===
arbre_decision = construire_arbre(df, colonnes_questions)
poser_questions(arbre_decision)