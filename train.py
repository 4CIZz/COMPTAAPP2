"""
Script d'entraînement — DCG UE9
--------------------------------
Lance ce script une seule fois pour entraîner l'IA sur tes annales.
Il va :
  1. Scanner les PDFs dans annales_dcg/
  2. Analyser chaque paire sujet+corrigé avec Claude
  3. Créer une synthèse globale (mémoire de l'épreuve)
  4. Tout sauvegarder dans annales_cache.json

Usage :
  python train.py
  ou avec la clé directement :
  python train.py --key sk-ant-...
"""

import anthropic
import json
import re
import sys
import argparse
import pdfplumber
from pathlib import Path

ANNALES_DIR = Path("annales_dcg")
CACHE_FILE  = Path("annales_cache.json")
MAX_CHARS   = 6000


# ─────────────────────────────────────────────
#  UTILITAIRES
# ─────────────────────────────────────────────

def log(msg: str, level: str = "info"):
    icons = {"info": "  →", "ok": "  ✓", "warn": "  ⚠", "step": "\n▶"}
    print(f"{icons.get(level, '  ')} {msg}")

def load_cache() -> dict:
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache: dict):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def extract_year(text: str) -> str:
    match = re.search(r"20\d{2}", text)
    return match.group(0) if match else "inconnue"

def is_corrige(filename: str) -> bool:
    name = filename.lower()
    return any(k in name for k in ["corrig", "correction", "reponse", "solution"])

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


# ─────────────────────────────────────────────
#  ÉTAPE 1 — SCANNER
# ─────────────────────────────────────────────

def step_scanner(cache: dict) -> dict:
    log("SCANNER LES PDFs", "step")
    ANNALES_DIR.mkdir(exist_ok=True)

    cached_files = set()
    for key, val in cache.items():
        if key.startswith("_"):
            continue
        for doc in val.values():
            if isinstance(doc, dict) and "filename" in doc:
                cached_files.add(doc["filename"])

    pdfs = sorted(ANNALES_DIR.glob("*.pdf"))
    if not pdfs:
        log(f"Aucun PDF trouvé dans {ANNALES_DIR}/", "warn")
        log("Dépose tes annales DCG dans ce dossier puis relance le script.", "warn")
        sys.exit(1)

    new_count = 0
    for pdf in pdfs:
        if pdf.name in cached_files:
            log(f"{pdf.name} — déjà en cache, ignoré")
            continue
        log(f"Extraction de {pdf.name}…")
        text, year = extract_text(pdf)
        doc_type = "corrige" if is_corrige(pdf.name) else "sujet"
        if year not in cache:
            cache[year] = {}
        cache[year][doc_type] = {"filename": pdf.name, "text": text}
        log(f"{pdf.name} → année {year}, type : {doc_type}", "ok")
        new_count += 1

    if new_count > 0:
        save_cache(cache)
        log(f"{new_count} fichier(s) extrait(s) et sauvegardés.", "ok")
    else:
        log("Tous les PDFs sont déjà en cache.", "ok")

    years = sorted(k for k in cache if not k.startswith("_"))
    print(f"\n  Années détectées : {', '.join(years)}")
    for year in years:
        yd = cache[year]
        has_s = "✓" if "sujet"   in yd else "✗"
        has_c = "✓" if "corrige" in yd else "✗"
        print(f"    {year}  sujet {has_s}  corrigé {has_c}")

    return cache


# ─────────────────────────────────────────────
#  ÉTAPE 2 — ANALYSER
# ─────────────────────────────────────────────

PROMPT_ANALYSE = """Tu es un expert DCG (Diplôme de Comptabilité et de Gestion) chargé d'analyser une annale officielle.

Voici le sujet de l'année {year} :
{sujet}

Voici le corrigé de l'année {year} :
{corrige}

Produis une analyse structurée et précise couvrant :
1. STRUCTURE DU SUJET : nombre de dossiers, organisation, répartition des points
2. THÈMES & COMPÉTENCES : liste des notions comptables évaluées (PCG, amortissements, provisions, sociétés, fiscalité, etc.)
3. TYPES DE QUESTIONS : nature des exercices (journal, bilan, calcul IS, consolidation, etc.)
4. MÉTHODES DE CALCUL : formules et raisonnements clés utilisés dans le corrigé
5. STYLE RÉDACTIONNEL : ton, formulation des énoncés, complexité des données chiffrées
6. POINTS DISTINCTIFS : ce qui rend cette annale originale par rapport à une annale standard

Sois précis et technique. Cette analyse sera utilisée pour générer de nouvelles annales."""


def step_analyser(client: anthropic.Anthropic, cache: dict) -> dict:
    log("ANALYSER LES ANNALES (apprentissage par année)", "step")
    years = sorted(k for k in cache if not k.startswith("_"))
    to_analyse = [y for y in years if "analyse" not in cache.get(y, {})]

    if not to_analyse:
        log("Toutes les annales sont déjà analysées.", "ok")
        return cache

    for year in to_analyse:
        log(f"Analyse de l'annale {year}…")
        yd = cache[year]
        sujet_text   = yd.get("sujet",   {}).get("text", "Non disponible")[:MAX_CHARS]
        corrige_text = yd.get("corrige", {}).get("text", "Non disponible")[:MAX_CHARS]

        prompt = PROMPT_ANALYSE.format(year=year, sujet=sujet_text, corrige=corrige_text)
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        cache[year]["analyse"] = response.content[0].text
        save_cache(cache)
        log(f"Annale {year} analysée et sauvegardée.", "ok")

    return cache


# ─────────────────────────────────────────────
#  ÉTAPE 3 — SYNTHÉTISER
# ─────────────────────────────────────────────

PROMPT_SYNTHESE = """Tu es un expert DCG chargé de créer un profil complet de l'épreuve DCG UE9 à partir des analyses individuelles de plusieurs annales.

Voici les analyses des annales {years} :

{analyses}

À partir de ces analyses, produis une SYNTHÈSE GLOBALE structurée couvrant :

1. STRUCTURE TYPE DE L'ÉPREUVE : format récurrent, nombre moyen de dossiers, répartition habituelle des points
2. THÈMES RÉCURRENTS : notions évaluées chaque année vs notions ponctuelles
3. ÉVOLUTION : comment l'épreuve a évolué entre les années (difficulté, thèmes, style)
4. PATTERNS DE QUESTIONS : formulations et types d'exercices qui reviennent
5. MÉTHODES INCONTOURNABLES : les calculs et raisonnements à maîtriser absolument
6. CALIBRAGE : niveau de difficulté, longueur typique des calculs, pièges fréquents
7. RECOMMANDATIONS POUR GÉNÉRER UNE ANNALE INÉDITE : ce qu'il faut absolument inclure, les équilibres à respecter

Cette synthèse est la mémoire centrale du générateur. Elle doit être exhaustive et opérationnelle."""


def step_synthesiser(client: anthropic.Anthropic, cache: dict) -> dict:
    log("SYNTHÉTISER (mémoire globale de l'épreuve)", "step")

    years = sorted(k for k in cache if not k.startswith("_"))
    non_analyses = [y for y in years if "analyse" not in cache.get(y, {})]
    if non_analyses:
        log(f"Annales non analysées : {', '.join(non_analyses)} — lance d'abord l'étape 2.", "warn")
        sys.exit(1)

    analyses = ""
    for year in years:
        analyses += f"\n\n{'='*50}\nANALYSE {year}\n{'='*50}\n{cache[year]['analyse']}"

    prompt = PROMPT_SYNTHESE.format(years=", ".join(years), analyses=analyses)

    log("Claude construit la mémoire globale de l'épreuve…")
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )
    cache["_synthese"] = response.content[0].text
    save_cache(cache)
    log("Synthèse globale créée et sauvegardée.", "ok")
    return cache


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Entraînement IA — DCG UE9")
    parser.add_argument("--key", help="Clé API Anthropic (sk-ant-...)")
    parser.add_argument("--step", choices=["scan", "analyse", "synthese", "all"], default="all",
                        help="Étape à exécuter (défaut : all)")
    args = parser.parse_args()

    # Clé API
    import os
    api_key = args.key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        api_key = input("\n  Clé API Anthropic (sk-ant-...) : ").strip()
    if not api_key:
        print("  Clé API manquante. Abandon.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print("\n" + "="*50)
    print("  ENTRAÎNEMENT IA — DCG UE9")
    print("="*50)

    cache = load_cache()

    if args.step in ("scan", "all"):
        cache = step_scanner(cache)

    if args.step in ("analyse", "all"):
        cache = step_analyser(client, cache)

    if args.step in ("synthese", "all"):
        cache = step_synthesiser(client, cache)

    print("\n" + "="*50)
    print("  ENTRAÎNEMENT TERMINÉ")
    print("  Lance maintenant : streamlit run annales_dcg.py")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
