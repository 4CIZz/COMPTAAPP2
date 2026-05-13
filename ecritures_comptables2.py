import streamlit as st
import random
import re
import unicodedata


st.set_page_config(
    page_title="Écritures Comptables",
    page_icon="📒",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0,1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f8fbff 0%, #eef4fb 100%) !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent;
}

[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

html, body, p, span, div, label {
    font-family: 'DM Sans', sans-serif;
    color: #253041;
}

.hero {
    text-align: center;
    padding: 2.8rem 1rem 1.6rem;
    position: relative;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 700px;
    height: 280px;
    background: radial-gradient(ellipse at center, rgba(99,179,237,0.16) 0%, transparent 70%);
    pointer-events: none;
}

.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #3182ce;
    margin-bottom: 0.6rem;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    font-weight: 400;
    color: #1a202c;
    line-height: 1.15;
    margin: 0 0 0.4rem;
}

.hero-sub {
    font-size: 0.95rem;
    color: #64748b;
    margin: 0;
}

.enonce-card,
.score-bar,
.end-card,
.feedback {
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 10px 30px rgba(15,23,42,0.06);
    backdrop-filter: blur(10px);
}

.enonce-card {
    border-left: 4px solid #63b3ed;
    border-radius: 16px;
    padding: 1.4rem 1.8rem;
    margin: 0 auto 1.5rem;
    max-width: 860px;
    font-size: 1rem;
    line-height: 1.7;
    color: #334155;
}

.enonce-label,
.col-header,
.section-title {
    font-family: 'DM Mono', monospace;
    text-transform: uppercase;
}

.enonce-label {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #3182ce;
    margin-bottom: 0.5rem;
}

.col-header {
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    color: #64748b;
    padding: 0.4rem 0;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 0.4rem;
}

.feedback {
    max-width: 860px;
    margin: 0 auto 1.2rem;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    font-size: 0.9rem;
}

.feedback.correct {
    background: #f0fdf4;
    border-color: #bbf7d0;
    color: #15803d;
}

.feedback.wrong {
    background: #fff1f2;
    border-color: #fecdd3;
    color: #be123c;
}

.score-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    border-radius: 16px;
    padding: 1rem 2rem;
    margin: 0 auto 1.5rem;
    max-width: 860px;
}

.score-item { text-align: center; }

.score-num {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: #2563eb;
    line-height: 1;
}

.score-num.green { color: #16a34a; }
.score-num.red   { color: #dc2626; }

.score-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #64748b;
    margin-top: 0.2rem;
}

.score-divider {
    width: 1px;
    height: 36px;
    background: #e2e8f0;
}

[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #dbe4f0 !important;
    border-radius: 10px !important;
    color: #1e293b !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 0.6rem !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #63b3ed !important;
    box-shadow: 0 0 0 2px rgba(99,179,237,0.14) !important;
}

[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stButton"] > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    background: linear-gradient(135deg, #63b3ed, #4299e1) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 10px 22px rgba(66,153,225,0.22) !important;
}

.btn-secondary [data-testid="stButton"] > button {
    background: #ffffff !important;
    color: #475569 !important;
    border: 1px solid #dbe4f0 !important;
}

.btn-secondary [data-testid="stButton"] > button:hover {
    background: #f8fafc !important;
    box-shadow: none !important;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #63b3ed, #4299e1) !important;
    border-radius: 4px !important;
}

[data-testid="stProgress"] > div {
    background: #dbe4f0 !important;
    border-radius: 4px !important;
}

.end-card {
    text-align: center;
    border-radius: 24px;
    padding: 3rem 2rem;
    max-width: 520px;
    margin: 2rem auto;
}

.end-score {
    font-family: 'DM Serif Display', serif;
    font-size: 4rem;
    color: #2563eb;
}

.end-label {
    font-size: 0.95rem;
    color: #64748b;
    margin: 0.5rem 0 1.5rem;
}

.end-grade {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #1e293b;
}

.cat-badge {
    display: inline-block;
    background: rgba(99,179,237,0.12);
    color: #2563eb;
    border: 1px solid rgba(99,179,237,0.18);
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2rem 0.8rem;
    margin-bottom: 0.8rem;
}

.section-title {
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    color: #64748b;
    max-width: 860px;
    margin: 0 auto 0.6rem;
}

.corr-val {
    font-family: monospace;
    font-size: 0.85rem;
    padding: 0.4rem 0;
    color: #334155;
}

hr { border-color: #e2e8f0 !important; margin: 0.15rem 0 !important; }
</style>
""", unsafe_allow_html=True)


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
            {"compte": "607", "libelle": "Achats de marchandises", "debit": m, "credit": None},
            {"compte": "44566", "libelle": "TVA déductible sur ABS", "debit": tva, "credit": None},
            {"compte": "512", "libelle": "Banque", "debit": None, "credit": ttc},
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
            {"compte": "411", "libelle": "Clients", "debit": ttc, "credit": None},
            {"compte": "707", "libelle": "Ventes de marchandises", "debit": None, "credit": m},
            {"compte": "44571", "libelle": "TVA collectée", "debit": None, "credit": tva},
        ],
    })

    m = random.randint(1, 10) * 1200
    exercices.append({
        "categorie": "Trésorerie",
        "date": "05/04/N",
        "enonce": f"Règlement par chèque d'une dette fournisseur de <strong>{m:,} €</strong> (facture déjà comptabilisée).",
        "lignes": [
            {"compte": "401", "libelle": "Fournisseurs", "debit": m, "credit": None},
            {"compte": "512", "libelle": "Banque", "debit": None, "credit": m},
        ],
    })

    random.shuffle(exercices)
    return exercices


def norm_compte(txt):
    return re.sub(r"\s", "", (txt or "").strip().upper())


def norm_montant(txt):
    try:
        return int(float(re.sub(r"[^\d.]", "", (txt or "").strip())))
    except Exception:
        return None


def levenshtein(a, b):
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
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev[j - 1] + cost)
    return dp[n]


def libelle_ok(saisi, attendu):
    if not saisi.strip():
        return False
    dist = levenshtein(saisi, attendu)
    seuil = max(3, int(len(attendu) * 0.20))
    return dist <= seuil


def corriger(lignes, idx):
    attendus = {norm_compte(ligne["compte"]): ligne for ligne in lignes}
    resultats_map = {}

    for i in range(len(lignes)):
        compte_s = st.session_state.get(f"c_{idx}_{i}", "")
        libelle_s = st.session_state.get(f"l_{idx}_{i}", "")
        debit_s = st.session_state.get(f"d_{idx}_{i}", "")
        credit_s = st.session_state.get(f"cr_{idx}_{i}", "")
        cle = norm_compte(compte_s)

        if cle in attendus and cle not in resultats_map:
            ligne = attendus[cle]
            ok_libelle = libelle_ok(libelle_s, ligne["libelle"])
            ok_debit = norm_montant(debit_s) == ligne["debit"] if ligne["debit"] is not None else debit_s.strip() in ("", "0")
            ok_credit = norm_montant(credit_s) == ligne["credit"] if ligne["credit"] is not None else credit_s.strip() in ("", "0")
            resultats_map[cle] = {
                "ok_compte": True,
                "ok_libelle": ok_libelle,
                "ok_debit": ok_debit,
                "ok_credit": ok_credit,
                "tout_ok": True and ok_libelle and ok_debit and ok_credit,
                "saisi_row": i,
            }
        else:
            resultats_map[f"__inconnu_{i}"] = {
                "ok_compte": False,
                "ok_libelle": False,
                "ok_debit": False,
                "ok_credit": False,
                "tout_ok": False,
                "saisi_row": i,
            }

    resultats = []
    for ligne in lignes:
        cle = norm_compte(ligne["compte"])
        if cle in resultats_map:
            resultats.append(resultats_map[cle])
        else:
            resultats.append({
                "ok_compte": False,
                "ok_libelle": False,
                "ok_debit": False,
                "ok_credit": False,
                "tout_ok": False,
                "saisi_row": None,
            })

    return resultats


def init_state():
    for k, v in {
        "exercices": [],
        "ex_index": 0,
        "score": 0,
        "wrong": 0,
        "phase": "accueil",
        "total": 5,
        "correction": None,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()
s = st.session_state

st.markdown("""
<div class="hero">
    <p class="hero-label">Entraînement pratique</p>
    <h1 class="hero-title">Écritures Comptables</h1>
    <p class="hero-sub">Lisez l'énoncé — remplissez le journal de A à Z</p>
</div>
""", unsafe_allow_html=True)

if s["phase"] == "accueil":
    st.markdown("<br>", unsafe_allow_html=True)
    col = st.columns([1, 3, 1])[1]
    with col:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.88);border:1px solid rgba(148,163,184,0.18);border-radius:16px;padding:1.8rem 2rem;margin-bottom:1.5rem;box-shadow:0 10px 30px rgba(15,23,42,0.06);">
            <p style="color:#64748b;font-size:0.92rem;line-height:1.9;margin:0;">
                Un énoncé décrit une opération. Le journal est <strong style="color:#1e293b">entièrement vide</strong>.<br>
                Pour chaque ligne saisissez :<br>
                &nbsp;&nbsp;🔵 <span style="color:#2563eb;font-family:monospace">N° de compte</span><br>
                &nbsp;&nbsp;📝 <span style="color:#475569;font-family:monospace">Libellé</span><br>
                &nbsp;&nbsp;🟢 <span style="color:#16a34a;font-family:monospace">Débit €</span> (laisser vide si rien)<br>
                &nbsp;&nbsp;🔴 <span style="color:#dc2626;font-family:monospace">Crédit €</span> (laisser vide si rien)
            </p>
        </div>
        """, unsafe_allow_html=True)
        nb = st.slider("Nombre d'exercices", min_value=3, max_value=12, value=5, step=1)
        if st.button("▶  Commencer", use_container_width=True):
            s["exercices"] = generer_exercices()[:nb]
            s["total"] = nb
            s["ex_index"] = 0
            s["score"] = 0
            s["wrong"] = 0
            s["correction"] = None
            s["phase"] = "exercice"
            st.rerun()

elif s["phase"] == "exercice":
    idx = s["ex_index"]
    total = s["total"]
    ex = s["exercices"][idx]
    nb_lignes = len(ex["lignes"])

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

    st.markdown('<p class="section-title">✏️ Complétez le journal</p>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns([1.4, 3, 1.4, 1.4])
    h1.markdown('<div class="col-header">N° Compte</div>', unsafe_allow_html=True)
    h2.markdown('<div class="col-header">Libellé</div>', unsafe_allow_html=True)
    h3.markdown('<div class="col-header">Débit (€)</div>', unsafe_allow_html=True)
    h4.markdown('<div class="col-header">Crédit (€)</div>', unsafe_allow_html=True)

    for i in range(nb_lignes):
        c1, c2, c3, c4 = st.columns([1.4, 3, 1.4, 1.4])
        with c1:
            st.text_input("_", key=f"c_{idx}_{i}", placeholder="ex: 607")
        with c2:
            st.text_input("_", key=f"l_{idx}_{i}", placeholder="Libellé du compte")
        with c3:
            st.text_input("_", key=f"d_{idx}_{i}", placeholder="0")
        with c4:
            st.text_input("_", key=f"cr_{idx}_{i}", placeholder="0")
        st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✔  Valider mes réponses", use_container_width=True):
            resultats = corriger(ex["lignes"], idx)
            tout_ok = all(r["tout_ok"] for r in resultats)
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

elif s["phase"] == "correction":
    idx = s["ex_index"]
    total = s["total"]
    ex = s["exercices"][idx]
    corr = s["correction"]

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
        st.markdown('<div class="feedback correct">✅ <strong>Parfait !</strong> Toutes les lignes sont correctes.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="feedback wrong">❌ <strong>Des erreurs sont présentes.</strong> Consultez la correction ci-dessous.</div>', unsafe_allow_html=True)

    st.markdown('<p class="section-title" style="margin-top:1.2rem">✅ Correction complète</p>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns([1.4, 3, 1.4, 1.4])
    h1.markdown('<div class="col-header">N° Compte</div>', unsafe_allow_html=True)
    h2.markdown('<div class="col-header">Libellé</div>', unsafe_allow_html=True)
    h3.markdown('<div class="col-header">Débit (€)</div>', unsafe_allow_html=True)
    h4.markdown('<div class="col-header">Crédit (€)</div>', unsafe_allow_html=True)

    for i, (ligne, res) in enumerate(zip(ex["lignes"], corr["resultats"])):
        c1, c2, c3, c4 = st.columns([1.4, 3, 1.4, 1.4])
        cc = "#16a34a" if res["ok_compte"] else "#dc2626"
        lc = "#16a34a" if res["ok_libelle"] else "#ca8a04"
        dc = "#16a34a" if res["ok_debit"] else "#dc2626"
        rc = "#16a34a" if res["ok_credit"] else "#dc2626"
        mc = "✓" if res["ok_compte"] else "✗"
        ml = "✓" if res["ok_libelle"] else "~"
        with c1:
            st.markdown(f'<div class="corr-val" style="color:{cc};">{ligne["compte"]} {mc}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="corr-val" style="color:{lc};">{ligne["libelle"]} <span style="font-size:0.75rem;">{ml}</span></div>', unsafe_allow_html=True)
        with c3:
            if ligne["debit"] is not None:
                md = "✓" if res["ok_debit"] else "✗"
                st.markdown(f'<div class="corr-val" style="color:{dc};text-align:right;">{ligne["debit"]:,} € {md}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="corr-val" style="color:#cbd5e1;">—</div>', unsafe_allow_html=True)
        with c4:
            if ligne["credit"] is not None:
                mr = "✓" if res["ok_credit"] else "✗"
                st.markdown(f'<div class="corr-val" style="color:{rc};text-align:right;">{ligne["credit"]:,} € {mr}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="corr-val" style="color:#cbd5e1;">—</div>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        is_last = (idx + 1 >= total)
        if st.button("🏁  Voir mes résultats" if is_last else "→  Exercice suivant", use_container_width=True):
            s["ex_index"] += 1
            s["correction"] = None
            s["phase"] = "fin" if is_last else "exercice"
            st.rerun()

elif s["phase"] == "fin":
    total = s["total"]
    score = s["score"]
    pct = round(score / total * 100) if total else 0

    if pct >= 80:
        grade, emoji = "Excellent travail !", "🏆"
    elif pct >= 60:
        grade, emoji = "Bien joué !", "🎯"
    elif pct >= 40:
        grade, emoji = "Continuez à réviser.", "📚"
    else:
        grade, emoji = "À retravailler !", "💪"

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
            s["exercices"] = generer_exercices()[:total]
            s["ex_index"] = 0
            s["score"] = 0
            s["wrong"] = 0
            s["correction"] = None
            s["phase"] = "exercice"
            st.rerun()

    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↩  Retour à l'accueil", use_container_width=True):
            s["phase"] = "accueil"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)