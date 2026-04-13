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
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] { background: #0f1117 !important; }
[data-testid="stAppViewContainer"] > .main { background: #0f1117; }
[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

html, body, p, span, div, label {
    font-family: 'DM Sans', sans-serif;
    color: #e8e8e8;
}

.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 250px;
    background: radial-gradient(ellipse at center, rgba(99,179,237,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: #ffffff;
    line-height: 1.15;
    margin: 0 0 0.4rem;
}
.hero-sub { font-size: 0.9rem; color: #666; margin: 0; }

.enonce-card {
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-left: 4px solid #63b3ed;
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    margin: 0 auto 1.5rem;
    max-width: 860px;
    font-size: 1rem;
    line-height: 1.7;
    color: #d0d8e8;
}
.enonce-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 0.5rem;
}

.col-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #444;
    padding: 0.4rem 0;
    border-bottom: 1px solid #2a2d3a;
    margin-bottom: 0.4rem;
}

.feedback {
    max-width: 860px;
    margin: 0 auto 1.2rem;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    font-size: 0.88rem;
}
.feedback.correct {
    background: rgba(104,211,145,0.08);
    border: 1px solid rgba(104,211,145,0.25);
    color: #68d391;
}
.feedback.wrong {
    background: rgba(252,129,129,0.08);
    border: 1px solid rgba(252,129,129,0.25);
    color: #fc8181;
}

.score-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-radius: 14px;
    padding: 1rem 2rem;
    margin: 0 auto 1.5rem;
    max-width: 860px;
}
.score-item { text-align: center; }
.score-num {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: #63b3ed;
    line-height: 1;
}
.score-num.green { color: #68d391; }
.score-num.red   { color: #fc8181; }
.score-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #444;
    margin-top: 0.2rem;
}
.score-divider { width: 1px; height: 36px; background: #2a2d3a; }

[data-testid="stTextInput"] input {
    background: #13151f !important;
    border: 1px solid #2a2d3a !important;
    border-radius: 6px !important;
    color: #e0e0e0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 0.6rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #63b3ed !important;
    box-shadow: 0 0 0 2px rgba(99,179,237,0.12) !important;
}
[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stButton"] > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    background: #63b3ed !important;
    color: #0f1117 !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.7rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
}
[data-testid="stButton"] > button:hover {
    background: #90cdf4 !important;
    box-shadow: 0 0 20px rgba(99,179,237,0.2) !important;
    transform: translateY(-1px) !important;
}
.btn-secondary [data-testid="stButton"] > button {
    background: transparent !important;
    color: #555 !important;
    border: 1px solid #2a2d3a !important;
}
.btn-secondary [data-testid="stButton"] > button:hover {
    border-color: #444 !important;
    color: #999 !important;
    background: #1a1d27 !important;
    box-shadow: none !important;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #63b3ed, #4299e1) !important;
    border-radius: 4px !important;
}
[data-testid="stProgress"] > div {
    background: #2a2d3a !important;
    border-radius: 4px !important;
}

.end-card {
    text-align: center;
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-radius: 20px;
    padding: 3rem 2rem;
    max-width: 500px;
    margin: 2rem auto;
}
.end-score { font-family: 'DM Serif Display', serif; font-size: 4rem; color: #63b3ed; }
.end-label { font-size: 0.95rem; color: #666; margin: 0.5rem 0 1.5rem; }
.end-grade { font-family: 'DM Serif Display', serif; font-size: 1.3rem; color: #fff; }

.cat-badge {
    display: inline-block;
    background: rgba(99,179,237,0.1);
    color: #63b3ed;
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2rem 0.8rem;
    margin-bottom: 0.8rem;
}

.section-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #444;
    max-width: 860px;
    margin: 0 auto 0.6rem;
}

.corr-val { font-family: monospace; font-size: 0.85rem; padding: 0.4rem 0; }

hr { border-color: #1f2233 !important; margin: 0.15rem 0 !important; }
</style>
""", unsafe_allow_html=True)


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
        libelle_s = st.session_state.get(f"l_{idx}_{i}", "")
        debit_s   = st.session_state.get(f"d_{idx}_{i}", "")
        credit_s  = st.session_state.get(f"cr_{idx}_{i}", "")

        cle = norm_compte(compte_s)

        if cle in attendus and cle not in resultats_map:
            ligne = attendus[cle]
            ok_compte  = True
            ok_libelle = libelle_ok(libelle_s, ligne["libelle"])
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
    <p class="hero-label">Entraînement pratique</p>
    <h1 class="hero-title">Écritures Comptables</h1>
    <p class="hero-sub">Lisez l'énoncé — remplissez le journal de A à Z</p>
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
        <div style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:14px;padding:1.8rem 2rem;margin-bottom:1.5rem;">
            <p style="color:#888;font-size:0.88rem;line-height:1.9;margin:0;">
                Un énoncé décrit une opération. Le journal est <strong style="color:#e0e0e0">entièrement vide</strong>.<br>
                Pour chaque ligne saisissez :<br>
                &nbsp;&nbsp;🔵 <span style="color:#63b3ed;font-family:monospace">N° de compte</span><br>
                &nbsp;&nbsp;📝 <span style="color:#ccc;font-family:monospace">Libellé</span><br>
                &nbsp;&nbsp;🟢 <span style="color:#68d391;font-family:monospace">Débit €</span> (laisser vide si rien)<br>
                &nbsp;&nbsp;🔴 <span style="color:#fc8181;font-family:monospace">Crédit €</span> (laisser vide si rien)
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
            st.text_input("_", key=f"c_{idx}_{i}",  placeholder="ex: 607")
        with c2:
            st.text_input("_", key=f"l_{idx}_{i}",  placeholder="Libellé du compte")
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
        st.markdown('<div class="feedback correct">✅ &nbsp;<strong>Parfait !</strong> Toutes les lignes sont correctes.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="feedback wrong">❌ &nbsp;<strong>Des erreurs sont présentes.</strong> Consultez la correction ci-dessous.</div>', unsafe_allow_html=True)

    st.markdown('<p class="section-title" style="margin-top:1.2rem">✅  Correction complète</p>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns([1.4, 3, 1.4, 1.4])
    h1.markdown('<div class="col-header">N° Compte</div>', unsafe_allow_html=True)
    h2.markdown('<div class="col-header">Libellé</div>', unsafe_allow_html=True)
    h3.markdown('<div class="col-header">Débit (€)</div>', unsafe_allow_html=True)
    h4.markdown('<div class="col-header">Crédit (€)</div>', unsafe_allow_html=True)

    for i, (ligne, res) in enumerate(zip(ex["lignes"], corr["resultats"])):
        c1, c2, c3, c4 = st.columns([1.4, 3, 1.4, 1.4])
        cc = "#68d391" if res["ok_compte"]  else "#fc8181"
        lc = "#68d391" if res["ok_libelle"] else "#f6e05e"   # jaune si libellé approché
        dc = "#68d391" if res["ok_debit"]   else "#fc8181"
        rc = "#68d391" if res["ok_credit"]  else "#fc8181"
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