import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fonction pour sauvegarder les réponses
def save_response(reponses):
    df = pd.DataFrame([reponses])
    df.to_csv("resultats_sondage.csv", mode="a", header=False, index=False)

# Fonction pour afficher les résultats
def show_results():
    try:
        results = pd.read_csv("resultats_sondage.csv")
        st.subheader("Résultats du sondage")
        for rubrique in rubriques.keys():
            st.write(f"\n{rubrique}:")
            st.write(results[rubrique].describe())
            
            fig, ax = plt.subplots()
            results[rubrique].value_counts().plot(kind='bar', ax=ax)
            plt.title(f"Distribution des réponses pour {rubrique}")
            plt.xlabel("Montant (FCFA)")
            plt.ylabel("Nombre de réponses")
            st.pyplot(fig)
    except FileNotFoundError:
        st.warning("Aucun résultat disponible pour le moment.")

st.title("Sondage sur les dépenses")

rubriques = {
    "Nourriture Etoug-Ebe": [30000, 35000, 40000],
    "Nourriture Maman": [30000, 35000, 40000],
    "Médicaments Maman & autres": [30000, 35000, 40000],
    "Participation mensuelle au fonds d'urgence": [5000, 10000, 150000]
}

reponses = {}

for rubrique, montants in rubriques.items():
    st.subheader(rubrique)
    choix = st.radio(
        f"Choisissez une option pour {rubrique}:",
        ["Montant personnalisé"] + [f"{m} FCFA" for m in montants],
        key=rubrique
    )
    
    if choix == "Montant personnalisé":
        montant = st.number_input(f"Entrez le montant pour {rubrique} (en FCFA):", min_value=0, step=1000, key=f"{rubrique}_custom")
    else:
        montant = int(choix.replace(" FCFA", ""))
    
    reponses[rubrique] = montant

col1, col2 = st.columns(2)

with col1:
    if st.button("Soumettre"):
        df = pd.DataFrame([reponses])
        st.write("Vos réponses :")
        st.dataframe(df)
        save_response(reponses)
        st.success("Merci pour votre participation au sondage !")

with col2:
    if st.button("Voir les résultats du sondage"):
        show_results()
