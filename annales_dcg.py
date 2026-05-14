import streamlit as st
import requests
import json
import re
import pdfplumber
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
ANNALES_DIR  = Path("annales_dcg")
CACHE_FILE   = Path("annales_cache.json")
OLLAMA_URL   = "http://localhost:11434"
MODELE_DEF   = "llama3.1:8b"
MAX_CHARS    = 8000   # chars par annale dans le contexte

st.set_page_config(
    page_title="Générateur Annales DCG",
    page_icon="📚",
    layout="centered",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] { background: #080b12 !important; }
[data-testid="stAppViewContainer"] > .main { background: #080b12; padding-bottom: 4rem; }
[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
html, body, p, span, div, label { font-family: 'Inter', sans-serif; color: #cbd5e1; }

.hero { text-align: center; padding: 3rem 1rem 2rem; position: relative; }
.hero::before {
    content: ''; position: absolute; top: -40px; left: 50%;
    transform: translateX(-50%); width: 700px; height: 300px;
    background: radial-gradient(ellipse at center, rgba(99,102,241,0.12) 0%, rgba(139,92,246,0.06) 40%, transparent 70%);
    pointer-events: none;
}
.hero-label { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; letter-spacing: 0.3em; text-transform: uppercase; color: #818cf8; margin-bottom: 0.8rem; display: block; }
.hero-title { font-family: 'Inter', sans-serif; font-size: 2.8rem; font-weight: 700; color: #f1f5f9; line-height: 1.1; margin: 0 0 0.6rem; letter-spacing: -0.03em; }
.hero-sub   { font-size: 0.95rem; color: #475569; margin: 0; }

.section-label { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; letter-spacing: 0.22em; text-transform: uppercase; color: #64748b; max-width: 860px; margin: 1.8rem auto 0.8rem; }

.card { background: #0d1221; border: 1px solid #1e2535; border-radius: 16px; padding: 1.4rem 1.8rem; margin: 0 auto 1rem; max-width: 860px; }

.status-bar { display: flex; align-items: center; gap: 1rem; background: #0d1221; border: 1px solid #1e2535; border-radius: 14px; padding: 1rem 1.6rem; margin: 0 auto 1rem; max-width: 860px; }
.status-bar.ok  { border-color: rgba(52,211,153,0.3); }
.status-bar.err { border-color: rgba(248,113,113,0.2); }
.status-icon { font-size: 1.4rem; }
.status-title { font-weight: 600; font-size: 0.9rem; color: #e2e8f0; }
.status-sub   { font-size: 0.75rem; color: #475569; margin-top: 0.15rem; }

.badge { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.2rem 0.7rem; border-radius: 100px; margin-left: auto; }
.badge-ok  { background: rgba(52,211,153,0.08); color: #34d399; border: 1px solid rgba(52,211,153,0.2); }
.badge-err { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
.badge-info { background: rgba(99,102,241,0.08); color: #818cf8; border: 1px solid rgba(99,102,241,0.2); }

.year-block { margin-bottom: 0.9rem; padding-bottom: 0.9rem; border-bottom: 1px solid #131c2e; }
.year-block:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.year-title { font-size: 0.88rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.4rem; }
.file-row { display: flex; align-items: center; gap: 0.6rem; padding: 0.2rem 0 0.2rem 1.1rem; }
.file-name { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #64748b; flex: 1; }

.steps-box { background: #0d1221; border: 1px solid rgba(248,113,113,0.15); border-radius: 14px; padding: 1.4rem 1.8rem; margin: 0 auto 1rem; max-width: 860px; }
.steps-title { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; letter-spacing: 0.2em; text-transform: uppercase; color: #f87171; margin-bottom: 0.8rem; }
.step-line { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #475569; padding: 0.25rem 0; }
.step-line code { color: #818cf8; background: rgba(99,102,241,0.08); padding: 0.12rem 0.45rem; border-radius: 5px; }

.result-card { background: #0a0f1d; border: 1px solid rgba(99,102,241,0.2); border-radius: 16px; padding: 2rem 2.2rem; margin: 0 auto 1.5rem; max-width: 860px; position: relative; overflow: hidden; font-family: 'Inter', sans-serif; font-size: 0.9rem; line-height: 1.75; color: #cbd5e1; white-space: pre-wrap; }
.result-card::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: linear-gradient(180deg, #6366f1, #8b5cf6); border-radius: 3px 0 0 3px; }

[data-testid="stSelectbox"] > div > div { background: #0d1221 !important; border: 1px solid #1e2535 !important; border-radius: 10px !important; color: #e2e8f0 !important; }
[data-testid="stSelectbox"] label { color: #475569 !important; font-size: 0.78rem !important; }
[data-testid="stTextArea"] textarea { background: #0d1221 !important; border: 1px solid #1e2535 !important; border-radius: 10px !important; color: #e2e8f0 !important; font-size: 0.88rem !important; }
[data-testid="stTextArea"] label { color: #475569 !important; font-size: 0.78rem !important; }
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] { background: #6366f1 !important; border-color: #6366f1 !important; }

[data-testid="stButton"] > button { font-family: 'Inter', sans-serif !important; font-weight: 600 !important; font-size: 0.88rem !important; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important; color: #fff !important; border: none !important; border-radius: 12px !important; padding: 0.75rem 2rem !important; cursor: pointer !important; transition: all 0.2s !important; box-shadow: 0 4px 15px rgba(99,102,241,0.25) !important; }
[data-testid="stButton"] > button:hover { box-shadow: 0 6px 25px rgba(99,102,241,0.4) !important; transform: translateY(-2px) !important; }
[data-testid="stButton"] > button:disabled { opacity: 0.35 !important; transform: none !important; box-shadow: none !important; }

[data-testid="stDownloadButton"] > button { font-family: 'Inter', sans-serif !important; font-weight: 500 !important; font-size: 0.82rem !important; background: transparent !important; color: #64748b !important; border: 1px solid #1e2535 !important; border-radius: 10px !important; box-shadow: none !important; }
[data-testid="stDownloadButton"] > button:hover { border-color: #334155 !important; color: #94a3b8 !important; background: #0d1221 !important; transform: none !important; box-shadow: none !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FONCTIONS OLLAMA
# ─────────────────────────────────────────────
def ollama_status():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        modeles = [m["name"] for m in r.json().get("models", [])]
        return True, modeles
    except Exception:
        return False, []

def stream_ollama(modele: str, system: str, prompt: str):
    payload = {
        "model": modele,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
        "stream": True,
    }
    with requests.post(f"{OLLAMA_URL}/api/chat", json=payload, stream=True, timeout=300) as r:
        for line in r.iter_lines():
            if line:
                chunk = json.loads(line)
                token = chunk.get("message", {}).get("content", "")
                if token:
                    yield token


# ─────────────────────────────────────────────
#  FONCTIONS CACHE
# ─────────────────────────────────────────────
def load_cache() -> dict:
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache: dict):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def extract_year(text: str) -> str:
    m = re.search(r"20\d{2}", text)
    return m.group(0) if m else "inconnue"

def is_corrige(filename: str) -> bool:
    return any(k in filename.lower() for k in ["corrig", "correction", "reponse", "solution"])

def extract_text(path: Path) -> tuple[str, str]:
    year = extract_year(path.name)
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            t = page.extract_text()
            if t:
                if year == "inconnue" and i == 0:
                    year = extract_year(t)
                pages.append(t)
    return "\n\n".join(pages), year

def sync_annales() -> tuple[dict, list]:
    ANNALES_DIR.mkdir(exist_ok=True)
    cache = load_cache()
    cached_files = {
        doc["filename"]
        for k, v in cache.items() if not k.startswith("_")
        for doc in v.values() if isinstance(doc, dict) and "filename" in doc
    }
    new_files = []
    for pdf in sorted(ANNALES_DIR.glob("*.pdf")):
        if pdf.name in cached_files:
            continue
        with st.spinner(f"Extraction de {pdf.name}…"):
            text, year = extract_text(pdf)
        doc_type = "corrige" if is_corrige(pdf.name) else "sujet"
        cache.setdefault(year, {})[doc_type] = {"filename": pdf.name, "text": text}
        new_files.append(pdf.name)
    if new_files:
        save_cache(cache)
    return cache, new_files


# ─────────────────────────────────────────────
#  PROMPT DE GÉNÉRATION
# ─────────────────────────────────────────────
def build_prompt(cache: dict, theme: str, difficulte: str, consignes: str) -> tuple[str, str]:
    years = sorted(k for k in cache if not k.startswith("_"))
    corpus = ""
    for year in years:
        yd = cache[year]
        corpus += f"\n\n{'='*55}\nANNÉE {year}\n{'='*55}"
        if "sujet" in yd:
            corpus += f"\n\n[SUJET {year}]\n{yd['sujet']['text'][:MAX_CHARS]}"
        if "corrige" in yd:
            corpus += f"\n\n[CORRIGÉ {year}]\n{yd['corrige']['text'][:MAX_CHARS]}"

    opts = []
    if theme:      opts.append(f"Thème : {theme}")
    if difficulte: opts.append(f"Difficulté : {difficulte}")
    if consignes:  opts.append(f"Consignes : {consignes}")
    opts_str = "\n".join(opts) if opts else "Inspire-toi librement des patterns des annales."

    system = (
        "Tu es un inspecteur de l'Éducation Nationale. Tu rédiges un vrai sujet d'examen DCG UE9. "
        "Tu écris directement le contenu complet et détaillé — entreprise fictive réelle, chiffres précis, "
        "questions concrètes, tableaux remplis avec des données inventées mais cohérentes. "
        "Tu n'écris JAMAIS de méta-description, jamais de '[insérer ici]', jamais de placeholder. "
        "AUCUNE réponse, AUCUN corrigé. Uniquement les questions et les documents annexes avec leurs données."
    )

    user = f"""Voici des annales DCG UE9 officielles pour référence de format et de niveau :
{corpus}

---

Écris maintenant un sujet d'examen DCG UE9 COMPLET. Commence directement par le contenu, sans introduction.
Invente une vraie entreprise avec de vrais chiffres. Ne mets AUCUNE réponse.

Voici EXACTEMENT le format et le niveau de détail attendu — reproduis ce niveau de précision :

═══════════════════════════════════════════════════════════
DIPLÔME DE COMPTABILITÉ ET DE GESTION
Session 2027
Épreuve n°9 — Introduction à la comptabilité
Durée : 4 heures — Coefficient : 1
Matériel autorisé : calculatrice de poche sans imprimante

Le sujet comporte 10 pages et 5 annexes.
La présentation, la lisibilité, la qualité de la rédaction et
des calculs entreront pour une part importante dans l'appréciation des copies.
═══════════════════════════════════════════════════════════

PRÉSENTATION DE L'ENTREPRISE

[Invente ici une vraie entreprise : nom, forme juridique, secteur précis, activité, CA, adresse fictive]
Exemple de niveau de détail :
"La société MEUNERIE DES FLANDRES SARL, au capital de 150 000 €, est spécialisée dans la transformation
et la vente de farines industrielles. Son siège est situé à Armentières (59). Elle emploie 42 salariés
et réalise un chiffre d'affaires annuel d'environ 3 200 000 € HT."

═══════════════════════════════════════════════════════════
DOSSIER 1 — OPÉRATIONS COURANTES (30 points)
═══════════════════════════════════════════════════════════

Au cours du mois de mars N, l'entreprise a réalisé les opérations suivantes. Toutes les factures
sont réglées selon les conditions indiquées. La TVA applicable est de 20% sauf mention contraire.

[Écris 6 à 8 opérations réelles, numérotées, avec date, montants exacts HT+TVA+TTC, conditions de règlement.
Exemples du niveau attendu :]

Opération 1 — 03/03/N
Achat de matières premières auprès du fournisseur AGRI-NORD, facture n°AF-2247 :
- Montant HT : 12 480,00 €
- TVA 20% : 2 496,00 €
- Net à payer TTC : 14 976,00 €
Règlement : traite à 60 jours échéance 03/05/N

Opération 2 — 07/03/N
Vente de farine type 55 à la boulangerie DUPONT & FILS, facture n°VF-0891 :
- Prix unitaire HT : 0,85 €/kg — Quantité : 18 000 kg
- Remise 3% accordée pour volume
- TVA 5,5% (produit alimentaire de base)
- Règlement : 50% comptant par virement, 50% à 30 jours

[Continue avec des opérations similaires : avoir, escompte, LCR, acompte...]

TRAVAIL À FAIRE :
1. Passez toutes les écritures comptables au journal pour le mois de mars N. (15 points)
2. Le 15/04/N, la traite de l'opération 1 est présentée au paiement et réglée par la banque.
   Passez l'écriture correspondante. (3 points)

═══════════════════════════════════════════════════════════
ANNEXE 1 — Récapitulatif des opérations de mars N
═══════════════════════════════════════════════════════════

| N° | Date | Nature de l'opération | Fournisseur/Client | HT (€) | Taux TVA | TVA (€) | TTC (€) | Règlement |
|----|------|----------------------|-------------------|--------|----------|---------|---------|-----------|
[Remplis ce tableau avec les mêmes opérations que le dossier 1, chiffres identiques]

═══════════════════════════════════════════════════════════
DOSSIER 2 — DÉCLARATION DE TVA (25 points)
═══════════════════════════════════════════════════════════

L'entreprise est soumise au régime réel normal de TVA. Vous disposez des informations suivantes
pour le mois de mars N :

TVA COLLECTÉE :
[Liste réelle des ventes avec HT et taux — invente des montants cohérents avec le dossier 1 et d'autres]
- Ventes de produits taux 20% : HT = [montant] €
- Ventes de produits taux 5,5% : HT = [montant] €
- Prestations de services 20% : HT = [montant] €

TVA DÉDUCTIBLE :
- Achats de marchandises/matières (20%) : HT = [montant] €
- Autres charges externes (20%) : HT = [montant] €
- Acquisition d'immobilisation (20%) : HT = [montant] €
- Crédit de TVA du mois de février N : [montant] €

TRAVAIL À FAIRE :
1. Calculez le montant total de la TVA collectée au titre du mois de mars N. (4 points)
2. Calculez le montant total de la TVA déductible au titre du mois de mars N. (4 points)
3. Déterminez le montant de la TVA à décaisser ou du crédit de TVA à reporter. (3 points)
4. Passez l'écriture de règlement de la TVA au 20/04/N (ou constatation du crédit). (4 points)

═══════════════════════════════════════════════════════════
ANNEXE 2 — Récapitulatif TVA mars N
═══════════════════════════════════════════════════════════

| Nature de l'opération | Base HT (€) | Taux | TVA (€) |
|----------------------|------------|------|---------|
| Ventes taux 20%      | [montant]  | 20%  |         |
| Ventes taux 5,5%     | [montant]  | 5,5% |         |
| ... | | | |
| TOTAL TVA COLLECTÉE  |            |      |         |
| Achats mat. 20%      | [montant]  | 20%  |         |
| ... | | | |
| TOTAL TVA DÉDUCTIBLE |            |      |         |

[Remplis toutes les cases avec de vrais chiffres cohérents. Laisse la case TVA vide = à compléter par l'étudiant]

═══════════════════════════════════════════════════════════
DOSSIER 3 — OPÉRATIONS D'INVENTAIRE (25 points)
═══════════════════════════════════════════════════════════

Au 31/12/N, vous devez procéder aux écritures d'inventaire suivantes :

1. AMORTISSEMENT DU MATÉRIEL INDUSTRIEL
Un broyeur industriel a été acquis le [date] pour [valeur] € HT. Il est amorti en mode linéaire
sur [durée] ans. L'amortissement de l'exercice N s'élève à [montant calculé] €.
→ Passez l'écriture de dotation aux amortissements au 31/12/N. (4 points)

2. DÉPRÉCIATION D'UNE CRÉANCE CLIENT
Le client MINOTERIES DU SUD est en redressement judiciaire. Sa créance TTC de [montant] €
est estimée irrécouvrable à [taux]%. Une dépréciation doit être constatée.
→ Passez l'écriture de dépréciation au 31/12/N. (5 points)

3. CHARGES CONSTATÉES D'AVANCE
Une prime d'assurance annuelle de [montant] € a été comptabilisée le [date].
Elle couvre la période du [date début] au [date fin].
→ Calculez le montant de la CCA et passez l'écriture de régularisation. (5 points)

4. VARIATION DE STOCKS
Stock de matières premières au 01/01/N : [montant] €
Stock de matières premières au 31/12/N (inventaire physique) : [montant] €
→ Passez l'écriture de variation de stocks. (3 points)

═══════════════════════════════════════════════════════════
ANNEXE 3 — Extrait de la balance avant inventaire au 31/12/N
═══════════════════════════════════════════════════════════

| N° compte | Intitulé | Solde débiteur (€) | Solde créditeur (€) |
|-----------|----------|-------------------|---------------------|
| 2154 | Matériel industriel | [valeur brute] | |
| 28154 | Amortissements matériel | | [cumulé N-1] |
| 411 | Clients | [total TTC] | |
| 416 | Clients douteux | [montant TTC] | |
| 301 | Stocks matières premières | [SI] | |
| 616 | Primes d'assurances | [prime annuelle] | |
[Ajoute d'autres comptes cohérents avec le sujet]

═══════════════════════════════════════════════════════════
DOSSIER 4 — DOCUMENTS DE SYNTHÈSE (20 points)
═══════════════════════════════════════════════════════════

À partir de la balance après inventaire (Annexe 4), établissez les documents de synthèse.

TRAVAIL À FAIRE :
1. Complétez le compte de résultat simplifié (Annexe 5). (10 points)
2. Calculez le résultat net de l'exercice N. (3 points)
3. Complétez l'extrait du bilan au 31/12/N (Annexe 6) en distinguant actif brut,
   amortissements/dépréciations et actif net. (7 points)

═══════════════════════════════════════════════════════════
ANNEXE 4 — Balance après inventaire au 31/12/N (extrait)
═══════════════════════════════════════════════════════════

| N° compte | Intitulé du compte | Débit (€) | Crédit (€) |
|-----------|-------------------|-----------|------------|
| 101 | Capital social | | [montant] |
| 164 | Emprunts bancaires | | [montant] |
| 2154 | Matériel industriel | [montant] | |
| 28154 | Amort. matériel | | [montant] |
| 301 | Stocks matières | [montant] | |
| 411 | Clients | [montant] | |
| 491 | Dépréc. clients | | [montant] |
| 401 | Fournisseurs | | [montant] |
| 512 | Banque | [montant] | |
| 601 | Achats matières | [montant] | |
| 607 | Achats marchandises | [montant] | |
| 641 | Salaires | [montant] | |
| 645 | Charges sociales | [montant] | |
| 701 | Ventes produits | | [montant] |
| 707 | Ventes marchandises | | [montant] |
| 6811 | Dot. amortissements | [montant] | |
[Complète avec des montants réels cohérents — laisse vide uniquement les cases à calculer]

═══════════════════════════════════════════════════════════
ANNEXE 5 — Compte de résultat à compléter
═══════════════════════════════════════════════════════════

CHARGES | Montant | PRODUITS | Montant
Achats de marchandises | | Ventes de marchandises |
Variation stocks marchandises | | Ventes de produits finis |
Achats de matières premières | | Production stockée |
Variation stocks mat. premières | | |
Autres achats et charges ext. | | |
Impôts et taxes | | |
Charges de personnel | | |
Dotations amort. et dépréc. | | |
TOTAL CHARGES EXPLOITATION | | TOTAL PRODUITS EXPLOITATION |
RÉSULTAT D'EXPLOITATION | | |

═══════════════════════════════════════════════════════════

MAINTENANT RÉDIGE L'INTÉGRALITÉ DU SUJET en remplaçant tous les [montants] et [dates] par de
vraies valeurs inventées cohérentes. Ne laisse aucun placeholder vide.
Tous les chiffres doivent être arithmétiquement corrects et cohérents entre les dossiers.
Paramètres supplémentaires : {opts_str}"""

    return system, user


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
for k, v in {"cache": None, "annale_generee": None, "nom_pdf": ""}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-label">IA Locale · DCG UE9 · LLaMA 3.1</span>
    <h1 class="hero-title">Générateur d'Annales</h1>
    <p class="hero-sub">100% local · Gratuit · Sans internet après installation</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  STATUT OLLAMA
# ─────────────────────────────────────────────
ollama_ok, modeles_dispos = ollama_status()

if ollama_ok:
    noms = ", ".join(modeles_dispos) if modeles_dispos else "aucun modèle"
    st.markdown(f"""
    <div class="status-bar ok">
        <span class="status-icon">🟢</span>
        <div><div class="status-title">Ollama actif</div>
        <div class="status-sub">{noms}</div></div>
        <span class="badge badge-ok">Connecté</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="status-bar err">
        <span class="status-icon">🔴</span>
        <div><div class="status-title" style="color:#f87171;">Ollama non détecté</div>
        <div class="status-sub">Lance le setup pour installer Ollama et le modèle</div></div>
        <span class="badge badge-err">Hors ligne</span>
    </div>
    <div class="steps-box">
        <div class="steps-title">Installation requise</div>
        <div class="step-line">1. <code>python ia/setup.py</code> — installe Ollama et télécharge le modèle</div>
        <div class="step-line">2. Relance cette page une fois terminé</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Sélection du modèle
modeles_llm = modeles_dispos if modeles_dispos else [MODELE_DEF]
modele_choisi = st.selectbox("Modèle", modeles_llm, label_visibility="collapsed") if len(modeles_llm) > 1 else modeles_llm[0]
if len(modeles_llm) == 1:
    st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#475569;margin-bottom:1rem;">Modèle : {modele_choisi}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ANNALES EN MÉMOIRE
# ─────────────────────────────────────────────
st.markdown('<p class="section-label">📂 Annales en mémoire</p>', unsafe_allow_html=True)

if st.session_state.cache is None:
    st.session_state.cache = load_cache()
cache = st.session_state.cache

if st.button("Scanner annales_dcg/"):
    cache, new_files = sync_annales()
    st.session_state.cache = cache
    if new_files:
        st.success(f"{len(new_files)} fichier(s) ajouté(s) au cache.")
    else:
        st.info("Cache déjà à jour.")
    st.rerun()

years = sorted(k for k in cache if not k.startswith("_"))
if years:
    blocks = ""
    for year in years:
        yd = cache[year]
        s = f'<div class="file-row"><span>📄</span><span class="file-name">{yd["sujet"]["filename"]}</span><span class="badge badge-info">Sujet</span></div>' if "sujet" in yd else '<div class="file-row"><span>⚠️</span><span class="file-name" style="color:#fbbf24">Sujet manquant</span></div>'
        c = f'<div class="file-row"><span>✅</span><span class="file-name">{yd["corrige"]["filename"]}</span><span class="badge badge-ok">Corrigé</span></div>' if "corrige" in yd else '<div class="file-row"><span>⚠️</span><span class="file-name" style="color:#fbbf24">Corrigé manquant</span></div>'
        blocks += f'<div class="year-block"><div class="year-title">📅 {year}</div>{s}{c}</div>'
    st.markdown(f'<div class="card">{blocks}</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="card"><div style="text-align:center;padding:1.5rem 0;color:#334155;font-size:0.88rem;">
        <div style="font-size:2rem;margin-bottom:0.5rem;">📁</div>
        Dépose tes PDFs dans <code style="color:#818cf8">annales_dcg/</code> puis clique Scanner.<br><br>
        <span style="font-size:0.78rem;color:#475569;">Convention : <code style="color:#6366f1">2022_sujet.pdf</code> · <code style="color:#34d399">2022_corrige.pdf</code></span>
    </div></div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PARAMÈTRES
# ─────────────────────────────────────────────
st.markdown('<p class="section-label">⚙️  Paramètres</p>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    theme = st.selectbox("Thème principal", [
        "Automatique", "Comptabilité des sociétés", "Consolidation",
        "Opérations courantes", "Fin d'exercice",
        "Fiscalité & IS", "Amortissements & dépréciations",
    ])
    if theme == "Automatique":
        theme = ""
with col2:
    difficulte = st.selectbox("Difficulté", [
        "Similaire aux annales", "Plus accessible", "Plus difficile", "Niveau concours",
    ])

consignes = st.text_area(
    "Consignes libres (optionnel)",
    placeholder="Ex: PME du secteur industriel, inclure un dossier sur les fusions…",
    height=75,
)
st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  GÉNÉRER
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    gen_ok = len(years) > 0
    if st.button(
        "Générer une annale inédite" if gen_ok else "Scannez vos annales d'abord",
        use_container_width=True,
        disabled=not gen_ok,
    ):
        system, user = build_prompt(cache, theme, difficulte, consignes)
        texte_complet = ""

        with st.spinner("Votre IA génère l'annale… (3 à 10 min)"):
            for token in stream_ollama(modele_choisi, system, user):
                texte_complet += token

        # Génération PDF
        try:
            from ia.genere_pdf import generer_pdf
            OUTPUT_DIR = Path("annales_generees")
            OUTPUT_DIR.mkdir(exist_ok=True)
            nom_pdf = OUTPUT_DIR / f"annale_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            generer_pdf(texte_complet, nom_pdf)
            st.session_state.annale_generee = nom_pdf.read_bytes()
            st.session_state.nom_pdf = nom_pdf.name
        except Exception as e:
            st.error(f"Erreur PDF : {e}")

        st.rerun()


# ─────────────────────────────────────────────
#  TÉLÉCHARGEMENT PDF
# ─────────────────────────────────────────────
if st.session_state.annale_generee:
    st.markdown('<p class="section-label">📄 Annale prête</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card" style="text-align:center;padding:2rem;">
        <div style="font-size:2.5rem;margin-bottom:0.8rem;">✅</div>
        <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.4rem;">Annale générée avec succès</div>
        <div style="font-size:0.78rem;color:#475569;">{st.session_state.get('nom_pdf','')}</div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            "Télécharger le PDF",
            data=st.session_state.annale_generee,
            file_name=st.session_state.get("nom_pdf", "annale_dcg.pdf"),
            mime="application/pdf",
            use_container_width=True,
        )
