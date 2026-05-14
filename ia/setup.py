"""
Setup Ollama — À lancer une seule fois
---------------------------------------
1. Vérifie si Ollama est installé
2. Vérifie si le modèle est téléchargé
3. Télécharge le modèle si besoin (~5 Go)

Usage : python ia/setup.py
"""

import sys
import subprocess
import requests

MODELE = "llama3.1:8b"
OLLAMA_URL = "http://localhost:11434"


def log(msg, level="info"):
    icons = {"info": "  →", "ok": "  ✓", "warn": "  ⚠", "step": "\n▶", "err": "  ✗"}
    print(f"{icons.get(level, '  ')} {msg}")


def ollama_tourne() -> bool:
    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return True
    except Exception:
        return False


def modele_disponible(modele: str) -> bool:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        modeles = [m["name"] for m in r.json().get("models", [])]
        return any(modele.split(":")[0] in m for m in modeles)
    except Exception:
        return False


def main():
    print("\n" + "="*55)
    print("  SETUP OLLAMA — Générateur d'Annales DCG")
    print("="*55)

    # ── Étape 1 : Ollama installé ? ──
    log("Vérification d'Ollama…", "step")
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            log(f"Ollama installé : {result.stdout.strip()}", "ok")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        log("Ollama n'est pas installé.", "err")
        print("""
  ─────────────────────────────────────────────
  Installe Ollama en 2 étapes :

  1. Va sur https://ollama.com/download
  2. Télécharge et installe la version Windows
  3. Relance ce script

  ─────────────────────────────────────────────
""")
        sys.exit(1)

    # ── Étape 2 : Ollama tourne ? ──
    log("Vérification du service Ollama…", "step")
    if not ollama_tourne():
        log("Ollama est installé mais pas démarré.", "warn")
        log("Lancement d'Ollama…")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time
        time.sleep(3)
        if not ollama_tourne():
            log("Impossible de démarrer Ollama. Lance-le manuellement.", "err")
            sys.exit(1)
    log("Service Ollama actif", "ok")

    # ── Étape 3 : Modèle disponible ? ──
    log(f"Vérification du modèle {MODELE}…", "step")
    if modele_disponible(MODELE):
        log(f"Modèle {MODELE} déjà téléchargé", "ok")
    else:
        log(f"Téléchargement de {MODELE} (~5 Go)…", "info")
        print("  (Cela peut prendre 10-20 min selon ta connexion)\n")
        result = subprocess.run(["ollama", "pull", MODELE])
        if result.returncode == 0:
            log(f"Modèle {MODELE} téléchargé avec succès", "ok")
        else:
            log("Erreur lors du téléchargement.", "err")
            sys.exit(1)

    # ── Résumé ──
    print(f"\n{'='*55}")
    print("  SETUP TERMINÉ — Tout est prêt !")
    print(f"\n  Lance maintenant :")
    print(f"  streamlit run annales_dcg.py")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
