"""
Étape 1 — Préparer les données d'entraînement
Extrait le texte des PDFs et crée un fichier texte pour l'entraînement.
"""

import pdfplumber
import re
from pathlib import Path

ANNALES_DIR = Path("..") / "annales_dcg"
OUTPUT_FILE = Path("data_entrainement.txt")

SEPARATEUR = "\n\n<|NOUVELLE_ANNALE|>\n\n"


def extract_text(path: Path) -> str:
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                pages.append(t.strip())
    return "\n\n".join(pages)


def nettoyer(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def main():
    print("\n▶ PRÉPARATION DES DONNÉES\n")

    ANNALES_DIR.mkdir(exist_ok=True)
    pdfs = sorted(ANNALES_DIR.glob("*.pdf"))

    if not pdfs:
        print(f"  ⚠ Aucun PDF trouvé dans {ANNALES_DIR}/")
        return

    blocs = []
    for pdf in pdfs:
        print(f"  → Extraction de {pdf.name}…")
        text = extract_text(pdf)
        text = nettoyer(text)
        blocs.append(text)
        print(f"  ✓ {len(text):,} caractères extraits")

    corpus = SEPARATEUR.join(blocs)
    OUTPUT_FILE.write_text(corpus, encoding="utf-8")

    print(f"\n  ✓ Fichier créé : {OUTPUT_FILE}")
    print(f"  ✓ Total : {len(corpus):,} caractères / {len(blocs)} documents")
    print("\n  Lance maintenant : python train.py\n")


if __name__ == "__main__":
    main()
