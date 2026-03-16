# 🏠 Agent IA — Qualification Investisseurs Trust Invest

> Projet réalisé dans le cadre d'une candidature au stage IA & Automatisation chez Trust Invest — Mars 2026  
> Auteure : **Damarice MENGBA NKOA** · Master IA XP · EPSI Lyon

Un agent conversationnel intelligent qui qualifie les prospects investisseurs immobiliers en 5-6 questions et génère automatiquement une fiche de recommandation personnalisée avec stratégie d'investissement adaptée.

---

## 🎯 Fonctionnalités

- Conversation guidée en langage naturel avec l'agent **Alex**
- Qualification du prospect en 5-6 questions ciblées
- Détection automatique du profil investisseur (patrimonial → offensif)
- Dialogues adaptés à chaque stratégie avec exemples de biens réels Trust Invest
- Génération d'une fiche prospect structurée en fin de conversation
- Graphique interactif Budget vs Rentabilité des réalisations Trust Invest
- Interface aux couleurs Trust Invest (header sombre, sidebar, encadré fiche)
- Bouton de réinitialisation de conversation

---

## 🧱 Stack technique

| Outil | Rôle |
|---|---|
| `Python 3.9+` | Langage principal |
| `Streamlit` | Interface web |
| `Anthropic API` | Cerveau de l'agent (Claude) |
| `python-dotenv` | Gestion sécurisée de la clé API |
| `Plotly` | Graphique interactif |
| `Pandas` | Manipulation des données |
| `fpdf2` | Export PDF de la fiche prospect |

---

## 📁 Structure du projet

```
trust-invest-agent/
├── app.py                 ← Application principale Streamlit
├── system_prompt.py       ← Personnalité et règles de l'agent Alex
├── .env                   ← Clé API Anthropic (non versionné)
├── .gitignore             ← Ignore .env, venv, __pycache__
├── requirements.txt       ← Dépendances Python
└── README.md              ← Ce fichier
```

---

## ⚙️ Installation

### 1. Prérequis

- Python 3.9 ou supérieur
- Un compte Anthropic avec une clé API → [console.anthropic.com](https://console.anthropic.com)

### 2. Cloner le projet

```bash
git clone https://github.com/damaMOI/trust-invest-agent.git
cd trust-invest-agent
```

### 3. Créer un environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer la clé API

Crée un fichier `.env` à la racine du projet :

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ Ne jamais commiter ce fichier. Il est déjà dans le `.gitignore`.

---

## 🚀 Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans le navigateur :
```
http://localhost:8501
```

---

## 🌐 Déploiement sur Streamlit Cloud

1. Pousse le projet sur GitHub
2. Va sur [share.streamlit.io](https://share.streamlit.io)
3. Connecte ton repo GitHub
4. Dans **Secrets**, ajoute :
```
ANTHROPIC_API_KEY = "sk-ant-xxxxxxx"
```
5. Clique **Deploy** → lien public généré automatiquement

---

## 🤖 Comment fonctionne l'agent

```
Utilisateur envoie un message
           ↓
app.py ajoute le message à l'historique (st.session_state)
           ↓
Appel API Anthropic avec tout l'historique + system_prompt
           ↓
Claude génère la réponse selon le profil détecté
           ↓
Si profil identifié → dialogue adapté à la stratégie
           ↓
Si qualification complète → génération de la fiche prospect
           ↓
Streamlit affiche la réponse (fiche dans encadré stylisé)
```

---

## 📊 Stratégies d'investissement couvertes

| Stratégie | Rentabilité | Profil |
|---|---|---|
| 🔵 Patrimoniale | ~4–5% | Prudent, long terme, retraite |
| 🟢 Équilibrée | ~5–6% | Modéré, revenus + valorisation |
| 🟡 Dynamique | ~7–8% | Averti, cash-flow prioritaire |
| 🔴 Offensive | ~9%+ | Expérimenté, rendement maximum |

---

## 📄 requirements.txt

```
streamlit
anthropic
python-dotenv
plotly
pandas
fpdf2
```

---

## 🛠️ Dépannage

**L'app ne se lance pas :**
```bash
# Vérifie que tu es dans le bon dossier
cd trust-invest-agent

# Vérifie que le venv est activé
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**Erreur `ANTHROPIC_API_KEY not found` :**
- Vérifie que le fichier `.env` existe à la racine
- Vérifie que la clé commence par `sk-ant-`
- Relance le terminal après avoir créé le `.env`

**Erreur module manquant :**
```bash
pip install -r requirements.txt
```

**La page s'ouvre mais l'agent ne répond pas :**
- Vérifie ta clé API sur [console.anthropic.com](https://console.anthropic.com)
- Vérifie que tu as des crédits disponibles

---

## 💡 Améliorations prévues

- Export PDF de la fiche prospect (`fpdf2`)
- Sauvegarde des fiches en base SQLite
- Tableau de bord des prospects qualifiés
- Intégration webhook vers CRM
- Scoring automatique des prospects
- Automatisation n8n : envoi de la fiche par email au conseiller

---

## 👩‍💻 Auteure

**Damarice MENGBA NKOA**  
Étudiante Master IA XP — EPSI Lyon  
Recherche un stage IA & Automatisation — 4 mois à partir d'avril 2026

[github.com/damaMOI]