import streamlit as st        # Framework pour créer l'interface web
import anthropic               # SDK officiel pour appeler l'API Claude d'Anthropic
import os                      # Module Python natif pour lire les variables d'environnement
from dotenv import load_dotenv # Charge les variables du fichier .env (ta clé API)
from system_prompt import SYSTEM_PROMPT  # Importe le prompt système depuis ton fichier local
import plotly.express as px    # Pour les graphiques interactifs (budget vs rentabilité)
import pandas as pd            # Pour manipuler les données des biens immobiliers

load_dotenv()

# ── CONFIG PAGE ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Trust Invest — Agent IA",
    page_icon="🏠",
    layout="centered"
)

# ── STYLE CUSTOM ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
    }
    .trust-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .trust-header h1 {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .trust-header p {
        color: #7DD3FC;
        font-size: 0.95rem;
        margin-top: 0.4rem;
    }
    .stChatMessage {
        border-radius: 12px !important;
        margin-bottom: 0.5rem;
    }
    .fiche-prospect {
        background: white;
        border-left: 4px solid #0891B2;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        font-size: 0.9rem;
        line-height: 1.8;
    }
    .stButton > button {
        background-color: #0891B2 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        font-weight: 500 !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #0E7490 !important;
    }
    .stChatInputContainer {
        border-top: 1px solid #E2E8F0;
        padding-top: 1rem;
    }
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #334155 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="trust-header">
    <h1>🏠 Trust Invest</h1>
    <p>Agent IA — Qualification Investisseurs</p>
</div>
""", unsafe_allow_html=True)

# ── GRAPHIQUE ────────────────────────────────────────────────────────────────
biens = [
    {"nom": "Le Progrès",       "budget": 187, "rentabilite": 8.1, "zone": "Villeurbanne"},
    {"nom": "Le Flandrin",      "budget": 145, "rentabilite": 5.6, "zone": "Lyon 1er"},
    {"nom": "Le Pierre Voyant", "budget": 235, "rentabilite": 9.0, "zone": "Villeurbanne"},
    {"nom": "Le Longefer",      "budget": 395, "rentabilite": 7.5, "zone": "Lyon 8e"},
    {"nom": "Novembre",         "budget": 280, "rentabilite": 8.6, "zone": "Bron"},
    {"nom": "Le Bonhomme",      "budget": 210, "rentabilite": 5.1, "zone": "Lyon 3e"},
    {"nom": "Le Bastie",        "budget": 170, "rentabilite": 5.6, "zone": "Monplaisir"},
    {"nom": "Le Vitton",        "budget": 168, "rentabilite": 5.7, "zone": "Lyon 3e"},
    {"nom": "Le Raclet",        "budget": 180, "rentabilite": 5.8, "zone": "Lyon 7e"},
    {"nom": "Le Jean Jaurès",   "budget": 260, "rentabilite": 7.6, "zone": "Villeurbanne"},
    {"nom": "Le Paul Bert",     "budget": 370, "rentabilite": 7.5, "zone": "Lyon 3e"},
    {"nom": "Philippe-Goy",     "budget": 275, "rentabilite": 8.1, "zone": "Bron"},
    {"nom": "Le Baraban",       "budget": 165, "rentabilite": 7.0, "zone": "Part-Dieu"},
    {"nom": "Marc Sangnier",    "budget": 315, "rentabilite": 7.8, "zone": "Villeurbanne"},
    {"nom": "Le Dauphiné",      "budget": 209, "rentabilite": 6.3, "zone": "Lyon 3e"},
    {"nom": "Le Zola",          "budget": 209, "rentabilite": 5.6, "zone": "Villeurbanne"},
]

df = pd.DataFrame(biens)

with st.expander("📊 Voir les réalisations Trust Invest — Budget vs Rentabilité"):
    fig = px.scatter(
        df, x="budget", y="rentabilite",
        hover_name="nom", hover_data=["zone"],
        color="rentabilite",
        color_continuous_scale="teal",
        size="rentabilite",
        labels={"budget": "Budget rénové (k€)", "rentabilite": "Rentabilité (%)"},
        title="Budget vs Rentabilité — Réalisations Trust Invest"
    )
    st.plotly_chart(fig, use_container_width=True)

# ── CLIENT ANTHROPIC ─────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── INIT SESSION ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = (
        "Bonjour et bienvenue chez **Trust Invest** ! 👋\n\n"
        "Je suis **Alex**, votre conseiller en investissement immobilier. "
        "En quelques questions, je vais vous aider à identifier la meilleure "
        "stratégie pour votre projet sur Lyon et sa région.\n\n"
        "Pour commencer — quel est votre budget d'investissement ?"
    )
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome
    })

# ── AFFICHAGE HISTORIQUE ─────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "FICHE PROSPECT" in msg["content"] and msg["role"] == "assistant":
            parts = msg["content"].split("---")
            for part in parts:
                if "FICHE PROSPECT" in part:
                    st.markdown(f'<div class="fiche-prospect">{part.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    if part.strip():
                        st.markdown(part)
        else:
            st.markdown(msg["content"])

# ── INPUT UTILISATEUR ────────────────────────────────────────────────────────
if prompt := st.chat_input("Votre réponse..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Alex réfléchit..."):
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages
            )
            answer = response.content[0].text

            if "FICHE PROSPECT" in answer:
                parts = answer.split("---")
                for part in parts:
                    if "FICHE PROSPECT" in part:
                        st.markdown(f'<div class="fiche-prospect">{part.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                    else:
                        if part.strip():
                            st.markdown(part)
            else:
                st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo Trust Invest
    st.image(
        "https://cdn.prod.website-files.com/61dfdcb927e69051cc371d78/61dffe5915a021c6b9845a71_TRUST_logo-RVB-or.png",
        width=150
    )
    st.divider()

    st.markdown("Investissement immobilier clé en main sur Lyon et sa région.")
    st.divider()

    st.markdown("**Stratégies disponibles**")
    st.markdown("""
    🔵 **Patrimoniale** — ~4-5%  
    🟢 **Équilibrée** — ~5-6%  
    🟡 **Dynamique** — ~7-8%  
    🔴 **Offensive** — ~9%+  
    """)
    st.divider()

    st.markdown("**+150 projets** réalisés avec succès")
    st.markdown("**96%** de réussite financement")
    st.markdown("**0** impayé de loyer")
    st.divider()

    if st.button("🔄 Nouvelle conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("[trust-invest.fr](https://trust-invest.fr)", unsafe_allow_html=True)