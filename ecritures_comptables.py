import streamlit as st
import random
import re

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Écritures Comptables",
    page_icon="📒",
    layout="centered",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080b12 !important;
}
[data-testid="stAppViewContainer"] > .main {
    background: #080b12;
    padding-bottom: 3rem;
}
[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

html, body, p, span, div, label {
    font-family: 'Inter', sans-serif;
    color: #cbd5e1;
}

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; left: 50%;
    transform: translateX(-50%);
    width: 700px; height: 300px;
    background: radial-gradient(ellipse at center,
        rgba(99,102,241,0.12) 0%,
        rgba(139,92,246,0.06) 40%,
        transparent 70%);
    pointer-events: none;
}
.hero-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 0.8rem;
    display: block;
}
.hero-title {
    font-family: 'Inter', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.1;
    margin: 0 0 0.6rem;
    letter-spacing: -0.03em;
}
.hero-sub {
    font-size: 0.95rem;
    color: #475569;
    margin: 0;
    font-weight: 400;
}

/* ── SCORE BAR ── */
.score-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    background: #0f1520;
    border: 1px solid #1e2535;
    border-radius: 16px;
    padding: 0;
    margin: 0 auto 1.8rem;
    max-width: 860px;
    overflow: hidden;
}
.score-item {
    text-align: center;
    padding: 1rem 2.5rem;
    flex: 1;
    position: relative;
}
.score-item + .score-item::before {
    content: '';
    position: absolute;
    left: 0; top: 20%; height: 60%;
    width: 1px;
    background: #1e2535;
}
.score-num {
    font-family: 'Inter', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #818cf8;
    line-height: 1;
    letter-spacing: -0.02em;
}
.score-num.green { color: #34d399; }
.score-num.red   { color: #f87171; }
.score-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #334155;
    margin-top: 0.3rem;
}
.score-divider { display: none; }

/* ── BADGE CATÉGORIE ── */
.cat-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(99,102,241,0.08);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 100px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 1rem;
    margin-bottom: 0.9rem;
}

/* ── ÉNONCÉ ── */
.enonce-card {
    background: #0d1221;
    border: 1px solid #1e2535;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin: 0 auto 1.8rem;
    max-width: 860px;
    font-size: 0.97rem;
    line-height: 1.75;
    color: #94a3b8;
    position: relative;
    overflow: hidden;
}
.enonce-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #6366f1, #8b5cf6);
    border-radius: 3px 0 0 3px;
}
.enonce-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 0.7rem;
    display: block;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #64748b;
    max-width: 860px;
    margin: 0 auto 0.8rem;
}

/* ── TABLEAU ── */
.col-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #64748b;
    padding: 0.5rem 0.3rem;
    border-bottom: 1px solid #2a3550;
    margin-bottom: 0.5rem;
}

/* ── INPUTS ── */
[data-testid="stTextInput"] input {
    background: #0d1221 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.83rem !important;
    padding: 0.55rem 0.75rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
    background: #0f1520 !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #3d4f6b !important;
}
[data-testid="stTextInput"] label { display: none !important; }

/* ── BOUTON PRINCIPAL ── */
[data-testid="stButton"] > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.25) !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stButton"] > button:hover {
    box-shadow: 0 6px 25px rgba(99,102,241,0.4) !important;
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #7c7ff3 0%, #9d6ef8 100%) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── BOUTON SECONDAIRE ── */
.btn-secondary [data-testid="stButton"] > button {
    background: transparent !important;
    color: #475569 !important;
    border: 1px solid #1e2535 !important;
    box-shadow: none !important;
}
.btn-secondary [data-testid="stButton"] > button:hover {
    border-color: #334155 !important;
    color: #64748b !important;
    background: #0d1221 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── PROGRESS BAR ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    border-radius: 4px !important;
}
[data-testid="stProgress"] > div {
    background: #1e2535 !important;
    border-radius: 4px !important;
    height: 4px !important;
}

/* ── FEEDBACK ── */
.feedback {
    max-width: 860px;
    margin: 0 auto 1.4rem;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    font-size: 0.88rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.feedback.correct {
    background: rgba(52,211,153,0.07);
    border: 1px solid rgba(52,211,153,0.2);
    color: #34d399;
}
.feedback.wrong {
    background: rgba(248,113,113,0.07);
    border: 1px solid rgba(248,113,113,0.2);
    color: #f87171;
}

/* ── CORRECTION VALEURS ── */
.corr-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
    padding: 0.45rem 0.2rem;
}

/* ── SEPARATEUR ── */
hr {
    border: none !important;
    border-top: 1px solid #1e2d45 !important;
    margin: 0.2rem 0 !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #6366f1 !important;
    border-color: #6366f1 !important;
}

/* ── END CARD ── */
.end-card {
    text-align: center;
    background: #0d1221;
    border: 1px solid #1e2535;
    border-radius: 24px;
    padding: 3.5rem 2rem;
    max-width: 480px;
    margin: 2rem auto;
    position: relative;
    overflow: hidden;
}
.end-card::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 200px;
    background: radial-gradient(ellipse, rgba(99,102,241,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.end-score {
    font-family: 'Inter', sans-serif;
    font-size: 4.5rem;
    font-weight: 800;
    color: #818cf8;
    letter-spacing: -0.04em;
    line-height: 1;
}
.end-label { font-size: 0.9rem; color: #475569; margin: 0.6rem 0 1.8rem; }
.end-grade {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #e2e8f0;
}

/* ── ACCUEIL CARD ── */
.welcome-card {
    background: #0d1221;
    border: 1px solid #1e2535;
    border-radius: 18px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    line-height: 2;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PLAN COMPTABLE (auto-complétion libellé)
# ─────────────────────────────────────────────
PLAN_COMPTABLE = {
    "101":   "Capital social",
    "104":   "Primes liées au capital social",
    "106":   "Réserves",
    "110":   "Report à nouveau (solde créditeur)",
    "119":   "Report à nouveau (solde débiteur)",
    "120":   "Résultat de l'exercice (bénéfice)",
    "129":   "Résultat de l'exercice (perte)",
    "131":   "Subventions d'équipement",
    "142":   "Provisions réglementées",
    "151":   "Provisions pour risques",
    "155":   "Provisions pour impôts",
    "161":   "Emprunts obligataires",
    "162":   "Emprunts et dettes auprès des établissements de crédit",
    "163":   "Autres emprunts obligataires",
    "164":   "Emprunts auprès des établissements de crédit",
    "165":   "Dépôts et cautionnements reçus",
    "166":   "Participation des salariés aux résultats",
    "167":   "Emprunts et dettes assortis de conditions particulières",
    "168":   "Autres emprunts et dettes assimilées",
    "169":   "Primes de remboursement des obligations",
    "171":   "Dettes rattachées à des participations (groupe)",
    "174":   "Dettes rattachées à des participations (hors groupe)",
    "181":   "Dettes rattachées à des sociétés en participation",
    "251":   "Parts dans des entreprises liées",
    "261":   "Titres de participation",
    "271":   "Titres immobilisés (droit de propriété)",
    "272":   "Titres immobilisés (droit de créance)",
    "274":   "Prêts",
    "275":   "Dépôts et cautionnements versés",
    "280":   "Amortissements des immobilisations incorporelles",
    "281":   "Amortissements des immobilisations corporelles",
    "2801":  "Amortissements des frais d'établissement",
    "2803":  "Amortissements des frais de développement",
    "2805":  "Amortissements des concessions",
    "2807":  "Amortissements du fonds commercial",
    "2811":  "Amortissements des terrains",
    "2812":  "Amortissements des agencements de terrains",
    "2813":  "Amortissements des constructions",
    "2814":  "Amortissements des constructions sur sol d'autrui",
    "2815":  "Amortissements des installations techniques",
    "2818":  "Amortissements des autres immobilisations corporelles",
    "28183": "Amortissements du matériel",
    "2182":  "Matériel de transport",
    "2183":  "Matériel informatique",
    "2184":  "Mobilier",
    "2185":  "Matériel de bureau",
    "291":   "Dépréciations des immobilisations incorporelles",
    "292":   "Dépréciations des immobilisations corporelles",
    "296":   "Dépréciations des participations et créances rattachées",
    "297":   "Dépréciations des autres immobilisations financières",
    "301":   "Matières premières",
    "302":   "Autres approvisionnements",
    "310":   "Produits en cours",
    "320":   "Produits intermédiaires et finis",
    "370":   "Stocks de marchandises",
    "380":   "Stocks de services en cours",
    "391":   "Dépréciations des matières premières",
    "397":   "Dépréciations des stocks de marchandises",
    "401":   "Fournisseurs",
    "403":   "Fournisseurs — effets à payer",
    "404":   "Fournisseurs d'immobilisations",
    "405":   "Fournisseurs d'immobilisations — effets à payer",
    "408":   "Fournisseurs — factures non parvenues",
    "409":   "Fournisseurs débiteurs",
    "411":   "Clients",
    "413":   "Clients — effets à recevoir",
    "416":   "Clients douteux ou litigieux",
    "418":   "Clients — produits non encore facturés",
    "419":   "Clients créditeurs",
    "421":   "Personnel — rémunérations dues",
    "422":   "Comités d'entreprise",
    "423":   "Participation des salariés",
    "424":   "Participation syndicale",
    "425":   "Personnel — avances et acomptes",
    "426":   "Personnel — dépôts",
    "427":   "Personnel — oppositions",
    "428":   "Personnel — charges à payer et produits à recevoir",
    "431":   "Sécurité sociale",
    "437":   "Autres organismes sociaux",
    "438":   "Organismes sociaux — charges à payer et produits à recevoir",
    "441":   "État — TVA",
    "4452":  "TVA due intracommunautaire",
    "44562": "TVA déductible sur immobilisations",
    "44566": "TVA déductible sur ABS",
    "44571": "TVA collectée",
    "44581": "Acomptes — Régime simplifié d'imposition",
    "447":   "Autres impôts, taxes et versements assimilés",
    "448":   "État — Charges à payer et produits à recevoir",
    "451":   "Groupe",
    "455":   "Associés — comptes courants",
    "456":   "Associés — opérations sur le capital",
    "457":   "Associés — dividendes à payer",
    "458":   "Associés — opérations faites en commun",
    "462":   "Créances sur cessions d'immobilisations",
    "464":   "Dettes sur acquisitions de valeurs mobilières de placement",
    "465":   "Créances sur cessions de valeurs mobilières de placement",
    "467":   "Autres comptes débiteurs ou créditeurs",
    "468":   "Divers — charges à payer et produits à recevoir",
    "471":   "Opérations en instance (débit)",
    "472":   "Opérations en instance (crédit)",
    "474":   "Différences de conversion — Actif",
    "475":   "Différences de conversion — Passif",
    "476":   "Différences de conversion — Actif (éléments financiers)",
    "477":   "Différences de conversion — Passif (éléments financiers)",
    "481":   "Charges à répartir sur plusieurs exercices",
    "486":   "Charges constatées d'avance",
    "487":   "Produits constatés d'avance",
    "491":   "Dépréciations des comptes clients",
    "495":   "Dépréciations des comptes du groupe et associés",
    "496":   "Dépréciations des débiteurs divers",
    "501":   "Valeurs mobilières de placement",
    "511":   "Valeurs à l'encaissement",
    "512":   "Banque",
    "514":   "Chèques postaux",
    "516":   "Dividendes à encaisser",
    "518":   "Intérêts courus",
    "519":   "Concours bancaires courants",
    "530":   "Caisse",
    "531":   "Chèques postaux",
    "532":   "Banque (étranger)",
    "580":   "Virements internes",
    "590":   "Dépréciations des valeurs mobilières de placement",
    "601":   "Achats stockés — matières premières",
    "602":   "Achats stockés — autres approvisionnements",
    "603":   "Variations des stocks (approvisionnements et marchandises)",
    "604":   "Achats d'études et prestations de services",
    "605":   "Achats de matériels, équipements et travaux",
    "606":   "Achats non stockés de matières et fournitures",
    "607":   "Achats de marchandises",
    "608":   "Frais accessoires sur achats",
    "609":   "Rabais, remises et ristournes obtenus sur achats",
    "611":   "Sous-traitance générale",
    "612":   "Redevances de crédit-bail et contrats similaires",
    "613":   "Locations et charges locatives",
    "614":   "Charges locatives et de copropriété",
    "615":   "Entretien et réparations",
    "616":   "Primes d'assurances",
    "617":   "Études et recherches",
    "618":   "Divers",
    "619":   "Rabais, remises et ristournes obtenus sur services extérieurs",
    "621":   "Personnel extérieur à l'entreprise",
    "622":   "Rémunérations d'intermédiaires et honoraires",
    "623":   "Publicité, publications, relations publiques",
    "624":   "Transports de biens et transports collectifs du personnel",
    "6251":  "Voyages et déplacements",
    "6256":  "Missions",
    "6257":  "Réceptions",
    "626":   "Frais postaux et frais de télécommunications",
    "627":   "Services bancaires et assimilés",
    "628":   "Divers (autres charges externes)",
    "629":   "Rabais, remises et ristournes obtenus sur autres services",
    "631":   "Impôts, taxes et versements assimilés sur rémunérations",
    "633":   "Impôts, taxes et versements assimilés sur rémunérations (autres)",
    "635":   "Autres impôts, taxes et versements assimilés",
    "637":   "Autres impôts, taxes et versements assimilés (autres organismes)",
    "641":   "Salaires et appointements",
    "644":   "Rémunération du travail de l'exploitant",
    "645":   "Charges sociales patronales",
    "646":   "Cotisations sociales personnelles de l'exploitant",
    "647":   "Autres charges sociales",
    "648":   "Autres charges de personnel",
    "651":   "Redevances pour concessions, brevets, licences",
    "652":   "Charges de gestion courante (autres)",
    "653":   "Jetons de présence",
    "654":   "Pertes sur créances irrécouvrables",
    "655":   "Quotes-parts de résultat sur opérations faites en commun",
    "658":   "Charges diverses de gestion courante",
    "661":   "Charges d'intérêts",
    "664":   "Pertes sur créances liées à des participations",
    "665":   "Escomptes accordés",
    "666":   "Pertes de change",
    "667":   "Charges nettes sur cessions de VMP",
    "668":   "Autres charges financières",
    "671":   "Charges exceptionnelles sur opérations de gestion",
    "675":   "Valeurs comptables des éléments d'actifs cédés",
    "678":   "Autres charges exceptionnelles",
    "681":   "Dotations aux amortissements et aux provisions (charges d'exploitation)",
    "6811":  "Dotations aux amortissements des immobilisations",
    "6812":  "Dotations aux amortissements des charges à répartir",
    "6815":  "Dotations aux provisions pour risques et charges d'exploitation",
    "6816":  "Dotations aux dépréciations des immobilisations",
    "6817":  "Dotations aux provisions — dépréciation créances",
    "686":   "Dotations aux amortissements, dépréciations et provisions (charges financières)",
    "687":   "Dotations aux amortissements, dépréciations et provisions (charges exceptionnelles)",
    "691":   "Participation des salariés aux résultats",
    "695":   "Impôts sur les bénéfices",
    "699":   "Produits — report en arrière des déficits",
    "701":   "Ventes de produits finis",
    "702":   "Ventes de produits intermédiaires",
    "703":   "Ventes de produits résiduels",
    "704":   "Travaux",
    "705":   "Études",
    "706":   "Prestations de services",
    "707":   "Ventes de marchandises",
    "708":   "Produits des activités annexes",
    "709":   "Rabais, remises et ristournes accordés",
    "711":   "Variation des stocks de produits en cours",
    "713":   "Variation des stocks de produits",
    "721":   "Production immobilisée — immobilisations incorporelles",
    "722":   "Production immobilisée — immobilisations corporelles",
    "731":   "Produits nets partiels sur opérations à long terme",
    "740":   "Subventions d'exploitation",
    "751":   "Redevances pour concessions, brevets, licences",
    "752":   "Revenus des immeubles non affectés aux activités professionnelles",
    "753":   "Jetons de présence et rémunérations d'administrateurs",
    "754":   "Ristournes perçues des coopératives",
    "755":   "Quotes-parts de résultat sur opérations faites en commun",
    "758":   "Produits divers de gestion courante",
    "761":   "Produits de participations",
    "762":   "Produits des autres immobilisations financières",
    "763":   "Revenus des autres créances",
    "764":   "Revenus des valeurs mobilières de placement",
    "765":   "Escomptes obtenus",
    "766":   "Gains de change",
    "767":   "Produits nets sur cessions de VMP",
    "768":   "Autres produits financiers",
    "771":   "Produits exceptionnels sur opérations de gestion",
    "775":   "Produits des cessions d'éléments d'actif",
    "777":   "Quote-part des subventions virée au résultat",
    "778":   "Autres produits exceptionnels",
    "781":   "Reprises sur amortissements et provisions (produits d'exploitation)",
    "786":   "Reprises sur dépréciations et provisions (produits financiers)",
    "787":   "Reprises sur dépréciations et provisions (produits exceptionnels)",
    "791":   "Transferts de charges d'exploitation",
    "796":   "Transferts de charges financières",
    "797":   "Transferts de charges exceptionnelles",
}


def auto_libelle(compte_key, libelle_key):
    compte = norm_compte(st.session_state.get(compte_key, ""))
    if compte in PLAN_COMPTABLE:
        st.session_state[libelle_key] = PLAN_COMPTABLE[compte]


# ─────────────────────────────────────────────
#  EXERCICES
# ─────────────────────────────────────────────
def generer_exercices():
    exercices = []

    m = random.randint(1, 20) * 500
    tva = round(m * 0.20)
    ttc = m + tva
    exercices.append({
        "categorie": "Achats",
        "date": "15/03/N",
        "enonce": f"L'entreprise achète des marchandises pour <strong>{m:,} € HT</strong> (TVA 20 % = {tva:,} €, TTC = <strong>{ttc:,} €</strong>). Règlement immédiat par virement bancaire.",
        "lignes": [
            {"compte": "607",   "libelle": "Achats de marchandises",           "debit": m,    "credit": None},
            {"compte": "44566", "libelle": "TVA déductible sur ABS",            "debit": tva,  "credit": None},
            {"compte": "512",   "libelle": "Banque",                            "debit": None, "credit": ttc},
        ],
    })

    m = random.randint(1, 15) * 800
    tva = round(m * 0.20)
    ttc = m + tva
    exercices.append({
        "categorie": "Ventes",
        "date": "20/03/N",
        "enonce": f"Vente de marchandises à un client pour <strong>{m:,} € HT</strong> (TVA 20 % = {tva:,} €, TTC = <strong>{ttc:,} €</strong>). Paiement différé à 30 jours.",
        "lignes": [
            {"compte": "411",   "libelle": "Clients",                   "debit": ttc,  "credit": None},
            {"compte": "707",   "libelle": "Ventes de marchandises",    "debit": None, "credit": m},
            {"compte": "44571", "libelle": "TVA collectée",             "debit": None, "credit": tva},
        ],
    })

    m = random.randint(1, 10) * 1200
    exercices.append({
        "categorie": "Trésorerie",
        "date": "05/04/N",
        "enonce": f"Règlement par chèque d'une dette fournisseur de <strong>{m:,} €</strong> (facture déjà comptabilisée).",
        "lignes": [
            {"compte": "401", "libelle": "Fournisseurs", "debit": m,    "credit": None},
            {"compte": "512", "libelle": "Banque",       "debit": None, "credit": m},
        ],
    })

    m = random.randint(5, 30) * 1000
    tva = round(m * 0.20)
    ttc = m + tva
    exercices.append({
        "categorie": "Immobilisations",
        "date": "10/04/N",
        "enonce": f"Acquisition d'un matériel informatique pour <strong>{m:,} € HT</strong> (TVA 20 % = {tva:,} €, TTC = <strong>{ttc:,} €</strong>). Règlement différé (dette fournisseur d'immo).",
        "lignes": [
            {"compte": "2183",  "libelle": "Matériel informatique",                     "debit": m,    "credit": None},
            {"compte": "44562", "libelle": "TVA déductible sur immobilisations",         "debit": tva,  "credit": None},
            {"compte": "404",   "libelle": "Fournisseurs d'immobilisations",             "debit": None, "credit": ttc},
        ],
    })

    sal = random.randint(3, 8) * 500
    cs_sal = round(sal * 0.22)
    cs_pat = round(sal * 0.45)
    net = sal - cs_sal
    exercices.append({
        "categorie": "Personnel",
        "date": "30/04/N",
        "enonce": f"Paie du mois : salaire brut <strong>{sal:,} €</strong>, cotisations salariales <strong>{cs_sal:,} €</strong> (net à payer = {net:,} €), cotisations patronales <strong>{cs_pat:,} €</strong>. Passez les deux écritures.",
        "lignes": [
            {"compte": "641", "libelle": "Salaires et appointements",         "debit": sal,    "credit": None},
            {"compte": "431", "libelle": "Sécurité sociale — part salariale", "debit": None,   "credit": cs_sal},
            {"compte": "421", "libelle": "Personnel — rémunérations dues",    "debit": None,   "credit": net},
            {"compte": "645", "libelle": "Charges sociales patronales",       "debit": cs_pat, "credit": None},
            {"compte": "431", "libelle": "Sécurité sociale — part patronale", "debit": None,   "credit": cs_pat},
        ],
    })

    emp = random.randint(1, 5) * 10000
    exercices.append({
        "categorie": "Financement",
        "date": "02/05/N",
        "enonce": f"Souscription d'un emprunt bancaire de <strong>{emp:,} €</strong> versé sur le compte bancaire.",
        "lignes": [
            {"compte": "512", "libelle": "Banque",                                       "debit": emp,  "credit": None},
            {"compte": "164", "libelle": "Emprunts auprès des établissements de crédit", "debit": None, "credit": emp},
        ],
    })

    base = random.randint(5, 20) * 1000
    taux = random.choice([10, 20, 25, 33])
    dot  = round(base * taux / 100)
    exercices.append({
        "categorie": "Amortissements",
        "date": "31/12/N",
        "enonce": f"Dotation aux amortissements d'un matériel : valeur <strong>{base:,} €</strong>, taux linéaire <strong>{taux} %</strong>. Annuité = <strong>{dot:,} €</strong>.",
        "lignes": [
            {"compte": "6811",  "libelle": "Dotations aux amortissements des immobilisations", "debit": dot,  "credit": None},
            {"compte": "28183", "libelle": "Amortissements du matériel",                        "debit": None, "credit": dot},
        ],
    })

    creance = random.randint(1, 8) * 1000
    taux_p  = random.choice([30, 50, 70])
    prov    = round(creance * taux_p / 100)
    exercices.append({
        "categorie": "Provisions",
        "date": "31/12/N",
        "enonce": f"Créance client en litige de <strong>{creance:,} €</strong>. Risque estimé à <strong>{taux_p} %</strong>, provision = <strong>{prov:,} €</strong>.",
        "lignes": [
            {"compte": "6817", "libelle": "Dotations aux provisions — dépréciation créances", "debit": prov,  "credit": None},
            {"compte": "491",  "libelle": "Dépréciations des comptes clients",                "debit": None,  "credit": prov},
        ],
    })

    enc = random.randint(1, 15) * 600
    exercices.append({
        "categorie": "Trésorerie",
        "date": "12/05/N",
        "enonce": f"Un client règle sa facture de <strong>{enc:,} €</strong> par virement bancaire.",
        "lignes": [
            {"compte": "512", "libelle": "Banque",   "debit": enc,  "credit": None},
            {"compte": "411", "libelle": "Clients",  "debit": None, "credit": enc},
        ],
    })

    loyer = random.randint(1, 4) * 500
    exercices.append({
        "categorie": "Régularisations",
        "date": "31/12/N",
        "enonce": f"Un loyer de <strong>{loyer:,} €</strong> comptabilisé en décembre N concerne la période janvier–mars N+1. Passez la régularisation (CCA).",
        "lignes": [
            {"compte": "486", "libelle": "Charges constatées d'avance",    "debit": loyer, "credit": None},
            {"compte": "613", "libelle": "Locations et charges locatives", "debit": None,  "credit": loyer},
        ],
    })

    cap = random.randint(1, 10) * 5000
    exercices.append({
        "categorie": "Capitaux",
        "date": "01/01/N",
        "enonce": f"Constitution de la société : apport en numéraire de <strong>{cap:,} €</strong> versé sur le compte bancaire.",
        "lignes": [
            {"compte": "512", "libelle": "Banque",         "debit": cap,  "credit": None},
            {"compte": "101", "libelle": "Capital social", "debit": None, "credit": cap},
        ],
    })

    frais = random.randint(1, 6) * 100
    tva_f = round(frais * 0.20)
    ttc_f = frais + tva_f
    exercices.append({
        "categorie": "Charges",
        "date": "08/04/N",
        "enonce": f"Remboursement d'une note de frais de déplacement : <strong>{frais:,} € HT</strong> (TVA 20 % = {tva_f:,} €, TTC = <strong>{ttc_f:,} €</strong>).",
        "lignes": [
            {"compte": "6251",  "libelle": "Voyages et déplacements",       "debit": frais, "credit": None},
            {"compte": "44566", "libelle": "TVA déductible sur ABS",         "debit": tva_f, "credit": None},
            {"compte": "421",   "libelle": "Personnel — rémunérations dues", "debit": None,  "credit": ttc_f},
        ],
    })

    random.shuffle(exercices)
    return exercices


# ─────────────────────────────────────────────
#  CORRECTION  (ordre libre + libellé fuzzy)
# ─────────────────────────────────────────────
def norm_compte(txt):
    return re.sub(r"\s", "", (txt or "").strip().upper())

def norm_montant(txt):
    try:
        return int(float(re.sub(r"[^\d.]", "", (txt or "").strip())))
    except Exception:
        return None

def levenshtein(a, b):
    """Distance d'édition entre deux chaînes (insensible casse/accents)."""
    import unicodedata
    def clean(s):
        s = s.lower().strip()
        s = unicodedata.normalize("NFD", s)
        s = "".join(c for c in s if unicodedata.category(c) != "Mn")
        return re.sub(r"\s+", " ", s)
    a, b = clean(a), clean(b)
    if a == b:
        return 0
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[:]
        dp[0] = i
        for j in range(1, n + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[j] = min(dp[j] + 1, dp[j-1] + 1, prev[j-1] + cost)
    return dp[n]

def libelle_ok(saisi, attendu):
    """Accepte le libellé si la distance relative est ≤ 20 % de la longueur."""
    if not saisi.strip():
        return False
    dist = levenshtein(saisi, attendu)
    seuil = max(3, int(len(attendu) * 0.20))   # tolérance 20%, min 3 caractères
    return dist <= seuil

def corriger(lignes, idx):
    """
    Matching par numéro de compte (ordre libre).
    Chaque ligne saisie est appariée à la ligne attendue
    dont le numéro de compte correspond.
    Les lignes sans correspondance sont marquées en erreur.
    """
    nb = len(lignes)

    # Construire un dict attendu : compte_normalisé -> ligne
    attendus = {}
    for ligne in lignes:
        attendus[norm_compte(ligne["compte"])] = ligne

    resultats_map = {}  # compte_normalisé -> résultat

    for i in range(nb):
        compte_s  = st.session_state.get(f"c_{idx}_{i}", "")
        debit_s   = st.session_state.get(f"d_{idx}_{i}", "")
        credit_s  = st.session_state.get(f"cr_{idx}_{i}", "")

        cle = norm_compte(compte_s)

        if cle in attendus and cle not in resultats_map:
            ligne = attendus[cle]
            ok_compte  = True
            ok_libelle = True  # libellé auto-rempli, pas évalué
            if ligne["debit"] is not None:
                ok_debit = norm_montant(debit_s) == ligne["debit"]
            else:
                ok_debit = debit_s.strip() in ("", "0")
            if ligne["credit"] is not None:
                ok_credit = norm_montant(credit_s) == ligne["credit"]
            else:
                ok_credit = credit_s.strip() in ("", "0")
            resultats_map[cle] = {
                "ok_compte": ok_compte, "ok_libelle": ok_libelle,
                "ok_debit": ok_debit,   "ok_credit":  ok_credit,
                "tout_ok":  ok_compte and ok_libelle and ok_debit and ok_credit,
                "saisi_row": i,
            }
        else:
            # Ligne saisie avec un compte inconnu ou dupliqué
            resultats_map[f"__inconnu_{i}"] = {
                "ok_compte": False, "ok_libelle": False,
                "ok_debit": False,  "ok_credit":  False,
                "tout_ok": False, "saisi_row": i,
            }

    # Réordonner les résultats dans l'ordre des lignes ATTENDUES
    # (pour l'affichage de la correction)
    resultats = []
    for ligne in lignes:
        cle = norm_compte(ligne["compte"])
        if cle in resultats_map:
            resultats.append(resultats_map[cle])
        else:
            # Compte attendu non trouvé dans les saisies
            resultats.append({
                "ok_compte": False, "ok_libelle": False,
                "ok_debit": False,  "ok_credit":  False,
                "tout_ok": False, "saisi_row": None,
            })

    return resultats


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    for k, v in {
        "exercices": [], "ex_index": 0, "score": 0, "wrong": 0,
        "phase": "accueil", "total": 5, "correction": None,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
s = st.session_state

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-label">Entraînement pratique</span>
    <h1 class="hero-title">Écritures Comptables</h1>
    <p class="hero-sub">Lisez l'énoncé · Remplissez le journal de A à Z</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ACCUEIL
# ─────────────────────────────────────────────
if s["phase"] == "accueil":
    st.markdown("<br>", unsafe_allow_html=True)
    col = st.columns([1, 3, 1])[1]
    with col:
        st.markdown("""
        <div class="welcome-card">
            <p style="color:#475569;font-size:0.88rem;line-height:2;margin:0;">
                Un énoncé décrit une opération comptable.<br>
                Le journal est <strong style="color:#e2e8f0">entièrement vide</strong> — à vous de le remplir.<br>
                <span style="color:#6366f1;font-family:'JetBrains Mono',monospace;font-size:0.82rem;">N° compte</span>
                &nbsp;·&nbsp;
                <span style="color:#94a3b8;font-family:'JetBrains Mono',monospace;font-size:0.82rem;">Libellé</span>
                &nbsp;·&nbsp;
                <span style="color:#34d399;font-family:'JetBrains Mono',monospace;font-size:0.82rem;">Débit €</span>
                &nbsp;·&nbsp;
                <span style="color:#f87171;font-family:'JetBrains Mono',monospace;font-size:0.82rem;">Crédit €</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        nb = st.slider("Nombre d'exercices", min_value=3, max_value=12, value=5, step=1)
        if st.button("▶  Commencer", use_container_width=True):
            s["exercices"]  = generer_exercices()[:nb]
            s["total"]      = nb
            s["ex_index"]   = 0
            s["score"]      = 0
            s["wrong"]      = 0
            s["correction"] = None
            s["phase"]      = "exercice"
            st.rerun()


# ─────────────────────────────────────────────
#  EXERCICE
# ─────────────────────────────────────────────
elif s["phase"] == "exercice":
    idx       = s["ex_index"]
    total     = s["total"]
    ex        = s["exercices"][idx]
    nb_lignes = len(ex["lignes"])

    pct = round(s["score"] / max(idx, 1) * 100) if idx > 0 else 0
    st.markdown(f"""
    <div class="score-bar">
        <div class="score-item"><div class="score-num">{idx+1}/{total}</div><div class="score-label">Exercice</div></div>
        <div class="score-divider"></div>
        <div class="score-item"><div class="score-num green">{s['score']}</div><div class="score-label">Réussis</div></div>
        <div class="score-divider"></div>
        <div class="score-item"><div class="score-num red">{s['wrong']}</div><div class="score-label">Erreurs</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(idx / total)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f'<div style="max-width:860px;margin:0 auto 0.5rem;"><span class="cat-badge">{ex["categorie"]}</span></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="enonce-card">
        <p class="enonce-label">📋 Énoncé · {ex['date']}</p>
        {ex['enonce']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-title">✏️  Complétez le journal</p>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns([1.4, 3, 1.4, 1.4])
    h1.markdown('<div class="col-header">N° Compte</div>', unsafe_allow_html=True)
    h2.markdown('<div class="col-header">Libellé</div>', unsafe_allow_html=True)
    h3.markdown('<div class="col-header">Débit (€)</div>', unsafe_allow_html=True)
    h4.markdown('<div class="col-header">Crédit (€)</div>', unsafe_allow_html=True)

    for i in range(nb_lignes):
        c1, c2, c3, c4 = st.columns([1.4, 3, 1.4, 1.4])
        with c1:
            st.text_input("_", key=f"c_{idx}_{i}", placeholder="ex: 607",
                          on_change=auto_libelle,
                          args=(f"c_{idx}_{i}", f"l_{idx}_{i}"))
        with c2:
            st.text_input("_", key=f"l_{idx}_{i}", placeholder="— auto —", disabled=True)
        with c3:
            st.text_input("_", key=f"d_{idx}_{i}",  placeholder="0")
        with c4:
            st.text_input("_", key=f"cr_{idx}_{i}", placeholder="0")
        st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✔  Valider mes réponses", use_container_width=True):
            resultats = corriger(ex["lignes"], idx)
            tout_ok   = all(r["tout_ok"] for r in resultats)
            s["correction"] = {"resultats": resultats, "tout_ok": tout_ok}
            if tout_ok:
                s["score"] += 1
            else:
                s["wrong"] += 1
            s["phase"] = "correction"
            st.rerun()

    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↩  Accueil", use_container_width=True):
            s["phase"] = "accueil"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CORRECTION
# ─────────────────────────────────────────────
elif s["phase"] == "correction":
    idx   = s["ex_index"]
    total = s["total"]
    ex    = s["exercices"][idx]
    corr  = s["correction"]

    pct = round(s["score"] / max(idx + 1, 1) * 100)
    st.markdown(f"""
    <div class="score-bar">
        <div class="score-item"><div class="score-num">{idx+1}/{total}</div><div class="score-label">Exercice</div></div>
        <div class="score-divider"></div>
        <div class="score-item"><div class="score-num green">{s['score']}</div><div class="score-label">Réussis</div></div>
        <div class="score-divider"></div>
        <div class="score-item"><div class="score-num red">{s['wrong']}</div><div class="score-label">Erreurs</div></div>
        <div class="score-divider"></div>
        <div class="score-item"><div class="score-num">{pct}%</div><div class="score-label">Réussite</div></div>
    </div>
    """, unsafe_allow_html=True)

    if corr["tout_ok"]:
        st.markdown('<div class="feedback correct"><strong>Parfait !</strong>&nbsp; Toutes les lignes sont correctes.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="feedback wrong"><strong>Des erreurs sont présentes.</strong>&nbsp; Consultez la correction ci-dessous.</div>', unsafe_allow_html=True)

    st.markdown('<p class="section-title" style="margin-top:1.2rem">✅  Correction complète</p>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns([1.4, 3, 1.4, 1.4])
    h1.markdown('<div class="col-header">N° Compte</div>', unsafe_allow_html=True)
    h2.markdown('<div class="col-header">Libellé</div>', unsafe_allow_html=True)
    h3.markdown('<div class="col-header">Débit (€)</div>', unsafe_allow_html=True)
    h4.markdown('<div class="col-header">Crédit (€)</div>', unsafe_allow_html=True)

    for i, (ligne, res) in enumerate(zip(ex["lignes"], corr["resultats"])):
        c1, c2, c3, c4 = st.columns([1.4, 3, 1.4, 1.4])
        cc = "#34d399" if res["ok_compte"]  else "#f87171"
        lc = "#34d399" if res["ok_libelle"] else "#fbbf24"
        dc = "#34d399" if res["ok_debit"]   else "#f87171"
        rc = "#34d399" if res["ok_credit"]  else "#f87171"
        mc = "✓" if res["ok_compte"]  else "✗"
        ml = "✓" if res["ok_libelle"] else "~"   # ~ = libellé trop différent
        with c1:
            st.markdown(f'<div class="corr-val" style="color:{cc};">{ligne["compte"]} {mc}</div>', unsafe_allow_html=True)
        with c2:
            # Affiche la bonne réponse + indicateur
            st.markdown(
                f'<div class="corr-val" style="color:{lc};">'
                f'{ligne["libelle"]} <span style="font-size:0.75rem;">{ml}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        with c3:
            if ligne["debit"] is not None:
                md = "✓" if res["ok_debit"] else "✗"
                st.markdown(f'<div class="corr-val" style="color:{dc};text-align:right;">{ligne["debit"]:,} € {md}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="corr-val" style="color:#2a2d3a;">—</div>', unsafe_allow_html=True)
        with c4:
            if ligne["credit"] is not None:
                mr = "✓" if res["ok_credit"] else "✗"
                st.markdown(f'<div class="corr-val" style="color:{rc};text-align:right;">{ligne["credit"]:,} € {mr}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="corr-val" style="color:#2a2d3a;">—</div>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        is_last = (idx + 1 >= total)
        if st.button("🏁  Voir mes résultats" if is_last else "→  Exercice suivant", use_container_width=True):
            s["ex_index"]  += 1
            s["correction"] = None
            s["phase"]      = "fin" if is_last else "exercice"
            st.rerun()


# ─────────────────────────────────────────────
#  FIN
# ─────────────────────────────────────────────
elif s["phase"] == "fin":
    total = s["total"]
    score = s["score"]
    pct   = round(score / total * 100) if total else 0

    if pct >= 80:   grade, emoji = "Excellent travail !", "🏆"
    elif pct >= 60: grade, emoji = "Bien joué !", "🎯"
    elif pct >= 40: grade, emoji = "Continuez à réviser.", "📚"
    else:           grade, emoji = "À retravailler !", "💪"

    st.markdown(f"""
    <div class="end-card">
        <div style="font-size:3rem;margin-bottom:1rem">{emoji}</div>
        <div class="end-score">{score}/{total}</div>
        <p class="end-label">{pct}% de réussite</p>
        <p class="end-grade">{grade}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄  Recommencer", use_container_width=True):
            s["exercices"]  = generer_exercices()[:total]
            s["ex_index"]   = 0
            s["score"]      = 0
            s["wrong"]      = 0
            s["correction"] = None
            s["phase"]      = "exercice"
            st.rerun()

    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↩  Retour à l'accueil", use_container_width=True):
            s["phase"] = "accueil"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)