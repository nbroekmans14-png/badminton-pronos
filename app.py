port streamlit as st
import pandas as pd
import os

# Configuration
st.set_page_config(page_title="Badminton Pronos", page_icon="🏸", layout="wide")
st.title("🏸 Badminton Club : Le Classement Permanent")

# --- GESTION DU FICHIER DE SAUVEGARDE ---
DB_FILE = "classement.csv"

def charger_donnees():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).to_dict(orient="records")
    return []

def sauvegarder_donnees(data):
    df = pd.DataFrame(data)
    df.to_csv(DB_FILE, index=False)

# Charger les données au démarrage
if 'classement' not in st.session_state:
    st.session_state.classement = charger_donnees()

# Liste des 8 matchs
matchs = [
    "Simple Homme 1", "Simple Homme 2", "Simple Dame 1", "Simple Dame 2",
    "Double Homme", "Double Dame", "Double Mixte 1", "Double Mixte 2"
]

# --- SIDEBAR : ZONE ARBITRE ---
with st.sidebar:
    st.header("⚙️ Zone Arbitre")
    resultats_reels = {m: st.selectbox(m, ["Équipe Club", "Équipe Adverse"], key=f"ref_{m}") for m in matchs}
    
    st.divider()
    if st.button("🗑️ Réinitialiser le fichier (Attention !)"):
        st.session_state.classement = []
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        st.rerun()

# --- INTERFACE JOUEUR ---
col_saisie, col_classement = st.columns([1, 1.2])

with col_saisie:
    st.header("1. Faire un Prono")
    nom = st.text_input("Ton Nom / Pseudo")
    
    pronos_joueur = {}
    c1, c2 = st.columns(2)
    for i, m in enumerate(matchs):
        col = c1 if i < 4 else c2
        pronos_joueur[m] = col.radio(f"{m}", ["Équipe Club", "Équipe Adverse"], key=f"p_{m}")

    if st.button("🎯 Enregistrer mon prono !"):
        if not nom:
            st.warning("Précise ton nom !")
        else:
            bons = sum(1 for m in matchs if pronos_joueur[m] == resultats_reels[m])
            total = bons + (3 if bons == 8 else 0)
            
            nouvelle_ligne = {"Joueur": nom, "Matchs Justes": f"{bons}/8", "Score Total": total}
            st.session_state.classement.append(nouvelle_ligne)
            
            # SAUVEGARDE RÉELLE ICI
            sauvegarder_donnees(st.session_state.classement)
            
            st.success(f"Bravo {nom} ! Ton score de {total} est enregistré.")
            if bons == 8: st.balloons()

# --- CLASSEMENT ---
with col_classement:
    st.header("🏆 Classement Général")
    if st.session_state.classement:
        df_visu = pd.DataFrame(st.session_state.classement).sort_values(by="Score Total", ascending=False)
        st.dataframe(df_visu, use_container_width=True, hide_index=True)
    else:
        st.info("En attente des premiers paris...")
