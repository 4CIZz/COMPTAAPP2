"""
Génération CLI — Annale DCG via Ollama
Usage : python ia/generate.py
"""

import json
import re
import sys
import requests
from pathlib import Path
from datetime import datetime

CACHE_FILE  = Path("annales_cache.json")
OUTPUT_DIR  = Path("annales_generees")
OLLAMA_URL  = "http://localhost:11434"
MODELE      = "llama3.1:8b"
MAX_CHARS   = 8000


def log(msg, level="info"):
    icons = {"info": "  →", "ok": "  ✓", "warn": "  ⚠", "step": "\n▶"}
    print(f"{icons.get(level, '  ')} {msg}")


def load_cache() -> dict:
    if not CACHE_FILE.exists():
        log("Cache introuvable. Lance d'abord le scanner dans l'app Streamlit.", "warn")
        sys.exit(1)
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def check_ollama() -> list:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        log("Ollama n'est pas démarré. Lance : python ia/setup.py", "warn")
        sys.exit(1)


def generer(modele: str, system: str, prompt: str) -> str:
    payload = {
        "model": modele,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
        "stream": True,
    }
    texte = ""
    print("\n" + "="*55)
    with requests.post(f"{OLLAMA_URL}/api/chat", json=payload, stream=True, timeout=300) as r:
        for line in r.iter_lines():
            if line:
                chunk = json.loads(line)
                token = chunk.get("message", {}).get("content", "")
                if token:
                    print(token, end="", flush=True)
                    texte += token
    print("\n" + "="*55)
    return texte


def main():
    print("\n" + "="*55)
    print("  GÉNÉRATEUR D'ANNALES DCG — Mode CLI")
    print("="*55)

    cache  = load_cache()
    modeles = check_ollama()
    years  = sorted(k for k in cache if not k.startswith("_"))

    if not years:
        log("Aucune annale en cache. Scanne les PDFs depuis l'app Streamlit.", "warn")
        sys.exit(1)

    log(f"Modèle : {MODELE}", "ok")
    log(f"Annales disponibles : {', '.join(years)}", "ok")

    # Vérifier que le modèle est disponible
    modele = MODELE
    if not any(MODELE.split(":")[0] in m for m in modeles):
        if modeles:
            modele = modeles[0]
            log(f"Modèle {MODELE} non trouvé, utilisation de : {modele}", "warn")
        else:
            log("Aucun modèle Ollama disponible. Lance : python ia/setup.py", "warn")
            sys.exit(1)

    # Corpus
    corpus = ""
    for year in years:
        yd = cache[year]
        corpus += f"\n\n{'='*50}\nANNÉE {year}\n{'='*50}"
        if "sujet" in yd:
            corpus += f"\n\n[SUJET {year}]\n{yd['sujet']['text'][:MAX_CHARS]}"
        if "corrige" in yd:
            corpus += f"\n\n[CORRIGÉ {year}]\n{yd['corrige']['text'][:MAX_CHARS]}"

    system = (
        "Tu es un inspecteur de l'Éducation Nationale, expert DCG UE9. "
        "Tu crées des sujets d'examen officiels et leurs corrigés. "
        "Tu maîtrises le Plan Comptable Général, la fiscalité, les sociétés. "
        "Réponds uniquement en français."
    )

    user = f"""Tu as analysé {len(years)} annales officielles DCG UE9 :
{corpus}

{'='*55}
Génère une annale INÉDITE avec :
- En-tête officiel (UE9, 4h, coefficient, matériel)
- Entreprise et montants inventés
- 3 dossiers numérotés avec sous-questions
- Calculs conformes au PCG, barème 100 pts
- Puis le CORRIGÉ DÉTAILLÉ avec écritures et calculs"""

    log("Génération en cours…", "step")
    texte = generer(modele, system, user)

    # Sauvegarde TXT
    OUTPUT_DIR.mkdir(exist_ok=True)
    nom = f"annale_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    txt_path = OUTPUT_DIR / f"{nom}.txt"
    txt_path.write_text(texte, encoding="utf-8")
    log(f"Texte sauvegardé : {txt_path}", "ok")

    # Sauvegarde PDF
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from genere_pdf import generer_pdf
        pdf_path = OUTPUT_DIR / f"{nom}.pdf"
        generer_pdf(texte, pdf_path)
        log(f"PDF sauvegardé : {pdf_path}", "ok")
    except Exception as e:
        log(f"PDF non généré : {e}", "warn")

    print(f"\n{'='*55}")
    print("  Génération terminée.")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
